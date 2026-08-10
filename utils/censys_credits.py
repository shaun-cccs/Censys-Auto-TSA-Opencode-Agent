#!/usr/bin/env python3
"""Track Censys credit (token) usage.

Wraps two Censys Platform account-management endpoints, neither of which costs
any credits to call:

* ``GET /v3/accounts/organizations/{org}/credits`` - current credit balance.
* ``GET /v3/accounts/organizations/{org}/credits/usage`` - a credit usage
  report over a date range, bucketed daily or monthly.
  https://docs.censys.com/reference/v3-accountmanagement-org-credits-usage

:class:`CreditTracker` uses both to measure what a block of work (e.g. a TSA
run) actually consumed: it snapshots the balance and the day's usage report
before and after, and reports the deltas.

Examples
--------
    python utils/censys_credits.py balance
    python utils/censys_credits.py usage --start-date 2026-07-01
    python utils/censys_credits.py usage --granularity monthly --by-consumer -f json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, Iterator, List, Optional

from censys_platform import SDK, models

from censys_query import (
    CENSYS_ORG_ID,
    DEFAULT_TIMEOUT_MS,
    get_org_id,
    RETRYABLE_STATUS,
    get_personal_access_token,
)

# Censys does not serve credit usage reports for dates before this.
EARLIEST_USAGE_DATE = date(2025, 1, 1)

# The usage endpoint rejects ranges longer than a year.
MAX_USAGE_RANGE_DAYS = 365

GRANULARITIES = ("daily", "monthly")


class CreditsError(RuntimeError):
    """Raised when a credits endpoint cannot be read."""


def _call(fn, *, max_retries: int = 3, base_delay: float = 1.0) -> Any:
    """Invoke an SDK call, retrying transient failures with backoff."""
    for attempt in range(max_retries):
        try:
            return fn()
        except models.SDKBaseError as e:
            status = getattr(e, "status_code", None)
            if status in RETRYABLE_STATUS and attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt))
                continue
            raise CreditsError(
                f"censys_error status={status} "
                f"msg={str(getattr(e, 'message', e))[:160]}"
            ) from e
        except Exception as e:  # noqa: BLE001 - network/unexpected
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt))
                continue
            raise CreditsError(f"{type(e).__name__}: {str(e)[:160]}") from e
    raise CreditsError("max_retries_exceeded")


def _dump(model: Any) -> Dict[str, Any]:
    """Unwrap an SDK response envelope into a plain ``result`` dict."""
    payload = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    result = payload.get("result", payload) or {}
    return result.get("result", result) if isinstance(result, dict) else result


@contextmanager
def _sdk(org_id: str, token: Optional[str] = None) -> Iterator[SDK]:
    with SDK(
        organization_id=get_org_id(org_id),
        personal_access_token=token or get_personal_access_token(),
        timeout_ms=DEFAULT_TIMEOUT_MS,
    ) as sdk:
        yield sdk


def _as_date(value: Any, default: date) -> date:
    if value is None:
        return default
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def today_utc() -> date:
    """Today's date in UTC, which is what Censys buckets usage against."""
    return datetime.now(timezone.utc).date()


def get_credit_balance(
    org_id: str = CENSYS_ORG_ID,
    token: Optional[str] = None,
    sdk: Optional[SDK] = None,
) -> Dict[str, Any]:
    """Return the organization's current credit balance and expirations."""
    def fetch(client: SDK) -> Dict[str, Any]:
        return _dump(
            _call(
                lambda: client.account_management.get_organization_credits(
                    organization_id=get_org_id(org_id)
                )
            )
        )

    if sdk is not None:
        return fetch(sdk)
    with _sdk(org_id, token) as client:
        return fetch(client)


def get_credit_usage(
    start_date: Optional[Any] = None,
    end_date: Optional[Any] = None,
    granularity: str = "daily",
    include_consumer_breakdown: bool = False,
    org_id: str = CENSYS_ORG_ID,
    token: Optional[str] = None,
    sdk: Optional[SDK] = None,
) -> Dict[str, Any]:
    """Return a credit usage report for a date range.

    ``start_date`` defaults to today (UTC) and ``end_date`` to today. Dates may
    be ``date`` objects or ``YYYY-MM-DD`` strings.
    """
    if granularity not in GRANULARITIES:
        raise ValueError(f"granularity must be one of {GRANULARITIES}")

    today = today_utc()
    start = _as_date(start_date, today)
    end = _as_date(end_date, today)

    if start < EARLIEST_USAGE_DATE:
        raise ValueError(
            f"start_date must be on or after {EARLIEST_USAGE_DATE.isoformat()}"
        )
    if end < start:
        raise ValueError("end_date must not precede start_date")
    if (end - start).days > MAX_USAGE_RANGE_DAYS:
        raise ValueError(
            f"date range must not exceed {MAX_USAGE_RANGE_DAYS} days"
        )

    request: Dict[str, Any] = {
        "organization_id": get_org_id(org_id),
        "start_date": start,
        "end_date": end,
        "granularity": granularity,
        "include_consumer_breakdown": include_consumer_breakdown,
    }

    def fetch(client: SDK) -> Dict[str, Any]:
        return _dump(
            _call(
                lambda: client.account_management.get_organization_credit_usage(
                    request=request
                )
            )
        )

    if sdk is not None:
        return fetch(sdk)
    with _sdk(org_id, token) as client:
        return fetch(client)


class CreditTracker:
    """Measure the credits consumed by a block of Censys work.

    Snapshots the credit balance and today's usage report before and after the
    tracked work. ``consumed`` prefers the balance delta (which updates
    immediately); ``consumed_reported`` is the usage-report delta, which is
    authoritative but may lag by a short interval.

    Usage::

        tracker = CreditTracker(org_id)
        tracker.start()
        ...  # run queries
        summary = tracker.stop()
    """

    def __init__(
        self,
        org_id: str = CENSYS_ORG_ID,
        token: Optional[str] = None,
        include_consumer_breakdown: bool = False,
        verbose: bool = False,
    ) -> None:
        self.org_id = org_id
        self.token = token
        self.include_consumer_breakdown = include_consumer_breakdown
        self.verbose = verbose
        self.errors: List[str] = []
        self.before: Optional[Dict[str, Any]] = None
        self.after: Optional[Dict[str, Any]] = None

    # -- snapshots -----------------------------------------------------------

    def _snapshot(self, label: str) -> Optional[Dict[str, Any]]:
        try:
            with _sdk(self.org_id, self.token) as client:
                balance = get_credit_balance(self.org_id, sdk=client)
                usage = get_credit_usage(
                    include_consumer_breakdown=self.include_consumer_breakdown,
                    org_id=self.org_id,
                    sdk=client,
                )
        except Exception as e:  # noqa: BLE001
            # Credit tracking is observability; it must never break a TSA run.
            self.errors.append(f"{label}_snapshot: {e}")
            if self.verbose:
                print(f"[credits] {label} snapshot failed: {e}", file=sys.stderr)
            return None

        snapshot = {
            "at": datetime.now(timezone.utc).isoformat(),
            "balance": balance.get("balance"),
            "total_consumed": usage.get("total_consumed"),
            "transaction_count": usage.get("transaction_count"),
            "usage": usage,
        }
        if self.verbose:
            print(
                f"[credits] {label}: balance={snapshot['balance']} "
                f"consumed_today={snapshot['total_consumed']}",
                file=sys.stderr,
            )
        return snapshot

    def start(self) -> Optional[Dict[str, Any]]:
        self.before = self._snapshot("before")
        return self.before

    def stop(self) -> Dict[str, Any]:
        self.after = self._snapshot("after")
        return self.summary()

    def __enter__(self) -> "CreditTracker":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

    # -- results -------------------------------------------------------------

    @staticmethod
    def _delta(before: Optional[Any], after: Optional[Any]) -> Optional[int]:
        if isinstance(before, int) and isinstance(after, int):
            return after - before
        return None

    def summary(self) -> Dict[str, Any]:
        """Return the credit deltas measured across the tracked block."""
        before = self.before or {}
        after = self.after or {}

        balance_before = before.get("balance")
        balance_after = after.get("balance")
        spent = self._delta(balance_after, balance_before)  # balance goes down
        reported = self._delta(
            before.get("total_consumed"), after.get("total_consumed")
        )

        return {
            "consumed": spent if spent is not None else reported,
            "consumed_by_balance": spent,
            "consumed_reported": reported,
            "transactions": self._delta(
                before.get("transaction_count"), after.get("transaction_count")
            ),
            "balance_before": balance_before,
            "balance_after": balance_after,
            "usage_after": after.get("usage"),
            "errors": list(self.errors),
        }


def format_usage(report: Dict[str, Any]) -> str:
    """Render a credit usage report as a human-readable summary."""
    def num(value: Any) -> str:
        return f"{value:,}" if isinstance(value, int) else "unknown"

    by_source = report.get("credits_consumed_by_source") or {}
    lines = [
        f"Window       : {str(report.get('start_time'))[:10]} "
        f"-> {str(report.get('end_time'))[:10]} "
        f"({report.get('granularity', 'daily')})",
        f"Consumed     : {num(report.get('total_consumed'))} credits",
        f"Added        : {num(report.get('total_added'))}",
        f"Expired      : {num(report.get('total_expired'))}",
        f"Transactions : {num(report.get('transaction_count'))}",
    ]
    if by_source:
        parts = ", ".join(f"{k}={num(v)}" for k, v in sorted(by_source.items()))
        lines.append(f"By source    : {parts}")

    by_consumer = report.get("credits_consumed_by_consumer") or {}
    if by_consumer:
        lines.append("By consumer  :")
        for who, amount in sorted(
            by_consumer.items(), key=lambda kv: -kv[1]
        ):
            lines.append(f"  {who:<40} {num(amount)}")

    periods = report.get("periods") or []
    if periods:
        lines += ["", f"{'Period':<12} {'Consumed':>10} {'Txns':>8}"]
        for period in periods:
            lines.append(
                f"{str(period.get('start_date'))[:10]:<12} "
                f"{num(period.get('credits_consumed')):>10} "
                f"{num(period.get('transaction_count')):>8}"
            )
    return "\n".join(lines)


def format_tracker_summary(summary: Dict[str, Any]) -> str:
    """Render a one-block summary of credits spent by a tracked run."""
    def num(value: Any) -> str:
        return f"{value:,}" if isinstance(value, int) else "unknown"

    lines = [f"Credits used   : {num(summary.get('consumed'))}"]
    if summary.get("balance_before") is not None:
        lines.append(
            f"  balance      : {num(summary.get('balance_before'))} -> "
            f"{num(summary.get('balance_after'))}"
        )
    if summary.get("consumed_reported") is not None:
        lines.append(f"  reported     : {num(summary['consumed_reported'])}")
    if summary.get("transactions") is not None:
        lines.append(f"  transactions : {num(summary['transactions'])}")
    for err in summary.get("errors") or []:
        lines.append(f"  ! {err}")
    return "\n".join(lines)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa assess"), not this file, which is not on their PATH.
    parser = argparse.ArgumentParser(
        prog=os.environ.get("CENSYS_TSA_PROG"),
        description="Inspect Censys credit balance and usage.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--org-id", default=CENSYS_ORG_ID, help="Censys organization ID")
    parser.add_argument(
        "-f", "--format", choices=("report", "json"), default="report",
        help="Output rendering for stdout",
    )
    parser.add_argument("-o", "--output", help="Write full JSON results to this file")

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("balance", help="Show the current credit balance")

    usage = sub.add_parser("usage", help="Show a credit usage report")
    usage.add_argument(
        "--start-date",
        help="Report start date, YYYY-MM-DD (default: 30 days ago)",
    )
    usage.add_argument("--end-date", help="Report end date, YYYY-MM-DD (default: today)")
    usage.add_argument(
        "--granularity", choices=GRANULARITIES, default="daily",
        help="Bucket size for the report periods",
    )
    usage.add_argument(
        "--by-consumer", action="store_true",
        help="Include a per-user consumption breakdown (admins only)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    try:
        if args.command == "balance":
            result = get_credit_balance(org_id=args.org_id)
            rendered = (
                f"Balance      : {result.get('balance'):,} credits"
                if isinstance(result.get("balance"), int)
                else "Balance      : unknown"
            )
        else:
            start = args.start_date or (today_utc() - timedelta(days=30)).isoformat()
            result = get_credit_usage(
                start_date=start,
                end_date=args.end_date,
                granularity=args.granularity,
                include_consumer_breakdown=args.by_consumer,
                org_id=args.org_id,
            )
            rendered = format_usage(result)
    except (CreditsError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.output:
        from pathlib import Path

        Path(args.output).write_text(json.dumps(result, indent=2))

    print(json.dumps(result, indent=2) if args.format == "json" else rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
