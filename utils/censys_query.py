#!/usr/bin/env python3
"""Run a Censys Platform search query and return paginated results.

Because every returned result consumes downstream token budget, requests to
Censys pass through a :class:`RateLimitGateway` that enforces a minimum delay
between calls, a sliding-window requests-per-minute cap, and a persistent
rolling-window request budget shared across runs.

Examples
--------
    python utils/censys_query.py '51.161.8.88'
    python utils/censys_query.py 'host.services.port: 22' --max-results 30 --output ssh.json
    python utils/censys_query.py 'web.endpoints.http.headers.server: nginx' --format table
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

from censys_platform import SDK, models

import censys_metrics

# Organization ID for the Censys Platform tenant. No default: see get_org_id().
CENSYS_ORG_ID = os.environ.get("CENSYS_ORG_ID", "")

# Censys caps page_size at 100.
MAX_PAGE_SIZE = 100

# Rate-limit defaults (overridable via CLI flags or environment variables).
DEFAULT_MIN_INTERVAL = float(os.environ.get("CENSYS_MIN_INTERVAL", 1.0))
DEFAULT_MAX_PER_MINUTE = int(os.environ.get("CENSYS_MAX_PER_MINUTE", 20))
DEFAULT_BUDGET_REQUESTS = int(os.environ.get("CENSYS_BUDGET_REQUESTS", 200))
DEFAULT_BUDGET_WINDOW = float(os.environ.get("CENSYS_BUDGET_WINDOW", 3600))

# Per-request HTTP timeout, in milliseconds, passed to the SDK.
#
# This must be set explicitly. Without it the SDK's own default governs, and a
# heavy regex query that the Censys backend never finishes will hold the socket
# open for far longer than any interactive workflow can tolerate - then be
# retried, with backoff, three more times. Measured in practice: single queries
# consuming 130s of wall time inside a fingerprinting run.
#
# The ceiling interacts with the retry loop in fetch_page(): worst-case wall
# time for one logical query is roughly max_retries * timeout plus the backoff
# sum, so keep it well under the patience of a human watching a TSA run. 60s x 4
# attempts + 7s backoff is already about four minutes.
DEFAULT_TIMEOUT_MS = int(os.environ.get("CENSYS_TIMEOUT_MS", 60_000))
DEFAULT_STATE_FILE = Path(
    os.environ.get(
        "CENSYS_RATE_STATE_FILE",
        Path.home() / ".censys_query_rate_state.json",
    )
)

# Session credit ceiling. Rate limits govern request pacing; this governs spend.
# Censys enterprise metering (vendor docs, confirmed against the live balance
# endpoint on 2026-08-05): every API action costs 1 credit, there is no
# surcharge for regex ("advanced") queries, and each additional page of 100
# results costs 1 more. Charging per page here is exact, because this runs once
# per page request.
CREDIT_CEILING = float(os.environ.get("CENSYS_SESSION_CREDIT_CEILING", 0) or 0)
CREDIT_LEDGER_FILE = Path(
    os.environ.get(
        "CENSYS_CREDIT_LEDGER_FILE",
        Path.home() / ".censys_session_credits.json",
    )
)
REGEX_QUERY_COST = 1
PLAIN_QUERY_COST = 1
# One credit per API request/page. Named so bulk and Adversary Investigation
# endpoints, which are metered differently, can override it.
API_REQUEST_COST = 1


class CreditCeilingError(RuntimeError):
    """Raised when the session credit ceiling would be exceeded."""


class MissingCredentialError(RuntimeError):
    """Raised when a required Censys credential is not configured.

    Carries a full, actionable message: these scripts are driven by agents that
    cannot see the user's shell, so "unauthorized" from the API is not a useful
    failure mode. Fail before the request, and say exactly what to export.
    """


def estimate_query_cost(query: str) -> int:
    """Credits a single search request (one page) consumes.

    Always 1. Censys enterprise metering charges 1 credit per API action and
    makes **no distinction between standard and advanced (regex) queries** -
    both measured at 1 credit. An earlier version of this module assumed regex
    cost 8; that was a Starter-plan-era myth and is wrong on this plan.
    """
    return API_REQUEST_COST


def read_credit_ledger() -> Dict[str, Any]:
    """Return the persisted session credit ledger, or a fresh one."""
    try:
        data = json.loads(CREDIT_LEDGER_FILE.read_text())
        if isinstance(data, dict):
            data.setdefault("spent", 0.0)
            data.setdefault("requests", 0)
            return data
    except (OSError, ValueError, TypeError):
        pass
    return {"spent": 0.0, "requests": 0, "started_at": time.time()}


def charge_credits(cost: float, query: str = "") -> None:
    """Record estimated spend, refusing the charge past the ceiling.

    Raises ``CreditCeilingError`` *before* the request is issued so the ceiling
    is a spend limit rather than an after-the-fact report.
    """
    if CREDIT_CEILING <= 0:
        return
    ledger = read_credit_ledger()
    projected = float(ledger["spent"]) + float(cost)
    if projected > CREDIT_CEILING:
        raise CreditCeilingError(
            f"session credit ceiling reached: {ledger['spent']:.0f} spent, this "
            f"request costs {cost:.0f}, ceiling is {CREDIT_CEILING:.0f}. "
            f"Raise CENSYS_SESSION_CREDIT_CEILING to continue."
        )
    ledger["spent"] = projected
    ledger["requests"] = int(ledger["requests"]) + 1
    ledger["last_query"] = (query or "")[:200]
    try:
        CREDIT_LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
        CREDIT_LEDGER_FILE.write_text(json.dumps(ledger))
    except OSError:
        pass

RETRYABLE_STATUS = (429, 500, 502, 503, 504)


class RateLimitError(RuntimeError):
    """Raised when the gateway refuses a request outright."""


@dataclass
class RateLimitGateway:
    """Gate every outbound Censys call through a request budget.

    Three independent controls are applied, in order:

    1. ``min_interval`` - hard floor on the delay between two calls.
    2. ``max_per_minute`` - sliding 60s window cap; the caller sleeps until a
       slot frees up (or fails fast when ``block`` is False).
    3. ``budget_requests`` / ``budget_window`` - a rolling budget persisted to
       ``state_file`` so separate script runs share the same allowance. Hitting
       this limit always raises rather than sleeping, since the wait may be
       arbitrarily long.
    """

    min_interval: float = DEFAULT_MIN_INTERVAL
    max_per_minute: int = DEFAULT_MAX_PER_MINUTE
    budget_requests: int = DEFAULT_BUDGET_REQUESTS
    budget_window: float = DEFAULT_BUDGET_WINDOW
    state_file: Optional[Path] = DEFAULT_STATE_FILE
    block: bool = True
    verbose: bool = False

    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    _recent: Deque[float] = field(default_factory=deque, repr=False)
    _last_call: float = field(default=0.0, repr=False)
    _calls_made: int = field(default=0, repr=False)

    @property
    def calls_made(self) -> int:
        return self._calls_made

    def acquire(self) -> None:
        """Block until a request slot is available, or raise."""
        with self._lock:
            self._enforce_budget()
            self._enforce_per_minute()
            self._enforce_min_interval()

            now = time.monotonic()
            self._last_call = now
            self._recent.append(now)
            self._calls_made += 1
            self._record_budget_use()

            if self.verbose:
                print(
                    f"[rate-limit] request #{self._calls_made} released "
                    f"({len(self._recent)}/{self.max_per_minute} in last 60s)",
                    file=sys.stderr,
                )

    # -- individual controls -------------------------------------------------

    def _enforce_min_interval(self) -> None:
        if self.min_interval <= 0 or self._last_call == 0.0:
            return
        wait = self.min_interval - (time.monotonic() - self._last_call)
        if wait <= 0:
            return
        if not self.block:
            raise RateLimitError(
                f"min interval not elapsed; {wait:.2f}s remaining"
            )
        self._sleep(wait, "min interval")

    def _enforce_per_minute(self) -> None:
        if self.max_per_minute <= 0:
            return
        while True:
            self._prune(time.monotonic())
            if len(self._recent) < self.max_per_minute:
                return
            wait = 60.0 - (time.monotonic() - self._recent[0])
            if wait <= 0:
                continue
            if not self.block:
                raise RateLimitError(
                    f"per-minute cap of {self.max_per_minute} reached; "
                    f"retry in {wait:.1f}s"
                )
            self._sleep(wait, "per-minute cap")

    def _enforce_budget(self) -> None:
        if self.budget_requests <= 0 or self.state_file is None:
            return
        used, oldest = self._budget_state()
        if used < self.budget_requests:
            return
        retry_in = max(0.0, self.budget_window - (time.time() - oldest))
        raise RateLimitError(
            f"request budget exhausted: {used}/{self.budget_requests} requests "
            f"in the last {int(self.budget_window)}s. Retry in ~{int(retry_in)}s "
            f"or raise --budget-requests."
        )

    # -- helpers -------------------------------------------------------------

    def _sleep(self, seconds: float, reason: str) -> None:
        if self.verbose:
            print(f"[rate-limit] sleeping {seconds:.2f}s ({reason})", file=sys.stderr)
        time.sleep(seconds)

    def _prune(self, now: float) -> None:
        while self._recent and now - self._recent[0] >= 60.0:
            self._recent.popleft()

    def _load_state(self) -> List[float]:
        if self.state_file is None or not self.state_file.exists():
            return []
        try:
            raw = json.loads(self.state_file.read_text())
            stamps = [float(t) for t in raw.get("timestamps", [])]
        except (OSError, ValueError, TypeError, AttributeError):
            return []
        cutoff = time.time() - self.budget_window
        return [t for t in stamps if t >= cutoff]

    def _budget_state(self) -> Tuple[int, float]:
        stamps = self._load_state()
        return len(stamps), (stamps[0] if stamps else time.time())

    def _record_budget_use(self) -> None:
        if self.state_file is None or self.budget_requests <= 0:
            return
        stamps = self._load_state()
        stamps.append(time.time())
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            self.state_file.write_text(
                json.dumps({"window": self.budget_window, "timestamps": stamps})
            )
        except OSError as exc:  # budget tracking must never break the query
            if self.verbose:
                print(f"[rate-limit] could not persist state: {exc}", file=sys.stderr)


def get_personal_access_token() -> str:
    """Resolve the Censys Platform token.

    The environment is the only supported source. An optional private-vault
    fallback exists for the organisation this kit came from and is deliberately
    soft: if the vault client is not installed - which is the case for everyone
    else - the ImportError is swallowed and the user gets an actionable message
    instead of a traceback about a package they have never heard of.
    """
    token = os.environ.get("CENSYS_PERSONAL_ACCESS_TOKEN")
    if token:
        return token

    group = os.environ.get("CENSYS_VAULT_GROUP")
    secret_name = os.environ.get("CENSYS_VAULT_SECRET")
    if group and secret_name:
        try:
            from hogwarts.spellbook import SpellbookClient
        except ImportError:
            pass
        else:
            vault_client = SpellbookClient()
            secret = vault_client.secrets.groups.get_secret(group, secret_name)
            return secret["personal_access_token"]

    raise MissingCredentialError(
        "CENSYS_PERSONAL_ACCESS_TOKEN is not set.\n"
        "Create a personal access token in the Censys Platform UI and export it:\n"
        "    export CENSYS_PERSONAL_ACCESS_TOKEN=...\n"
        "    export CENSYS_ORG_ID=...\n"
        "Run `tsa doctor` to check both."
    )


def get_org_id(explicit: Optional[str] = None) -> str:
    """Resolve the Censys organization ID.

    There is no default. An earlier version of this module hardcoded the
    organization of the team that wrote it, which meant anyone else silently
    queried - and built platform URLs for - a tenant that was not theirs.
    """
    org = explicit or CENSYS_ORG_ID
    if org:
        return org
    raise MissingCredentialError(
        "CENSYS_ORG_ID is not set.\n"
        "It is the organization your token belongs to. Find it in the Censys\n"
        "Platform UI under organization settings, or in the `org=` parameter of\n"
        "any platform.censys.io URL, then export it:\n"
        "    export CENSYS_ORG_ID=...\n"
        "Run `tsa doctor` to check it."
    )


def censys_search_page(
    sdk: SDK,
    query: str,
    gateway: RateLimitGateway,
    page_size: int = 10,
    page_token: Optional[str] = None,
    max_retries: int = 4,
    base_delay: float = 1.0,
) -> Tuple[Optional[Any], Optional[str]]:
    """Fetch one page of Censys results.

    Returns ``(search_query_response, error)``; exactly one is non-None.
    Transient errors (HTTP 429/5xx, network blips) are retried with
    exponential backoff. Every attempt passes through the rate-limit gateway.
    """
    body: Dict[str, Any] = {"query": query, "page_size": page_size}
    if page_token:
        body["page_token"] = page_token

    for attempt in range(max_retries):
        try:
            # Charged per attempt, not per logical query, and that is deliberate.
            # A retried attempt issues a real HTTP request, and a read timeout in
            # particular means Censys most likely did execute the query and will
            # bill for it - so counting only the successful attempt would
            # under-report spend, which is the one direction a circuit breaker
            # must never err in. The cost of a slow query is therefore bounded by
            # DEFAULT_TIMEOUT_MS and max_retries, not by this ledger.
            charge_credits(estimate_query_cost(query), query)
            gateway.acquire()
            # Timed inside the gateway, so the recorded duration is the Censys
            # round trip alone and never the rate-limit sleep that preceded it.
            # `tsa timeline` relies on that split to tell a slow API apart from
            # a stalled workflow.
            with censys_metrics.timed("search", query=query):
                res = sdk.global_data.search(search_query_input_body=body)
            return res.result, None
        except CreditCeilingError as e:
            return None, f"credit_ceiling: {e}"
        except RateLimitError as e:
            return None, f"rate_limited: {e}"
        except models.SDKBaseError as e:
            status = getattr(e, "status_code", None)
            if status in RETRYABLE_STATUS and attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt))
                continue
            return None, (
                f"censys_error status={status} "
                f"msg={str(getattr(e, 'message', e))[:120]}"
            )
        except Exception as e:  # noqa: BLE001 - network/unexpected
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt))
                continue
            return None, f"{type(e).__name__}: {str(e)[:120]}"
    return None, "max_retries_exceeded"


def run_query(
    query: str,
    gateway: RateLimitGateway,
    max_results: int = 10,
    page_size: int = 10,
    org_id: str = CENSYS_ORG_ID,
    token: Optional[str] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Search Censys, paginating until ``max_results`` hits are collected."""
    if max_results <= 0:
        raise ValueError("max_results must be positive")
    page_size = max(1, min(page_size, MAX_PAGE_SIZE, max_results))
    token = token or get_personal_access_token()

    hits: List[Dict[str, Any]] = []
    total_hits: Optional[int] = None
    page_token: Optional[str] = None
    pages = 0
    errors: List[str] = []

    with SDK(
        organization_id=get_org_id(org_id),
        personal_access_token=token,
        timeout_ms=DEFAULT_TIMEOUT_MS,
    ) as sdk:
        while len(hits) < max_results:
            remaining = max_results - len(hits)
            response, error = censys_search_page(
                sdk,
                query,
                gateway,
                page_size=min(page_size, remaining),
                page_token=page_token,
            )
            if error:
                errors.append(error)
                break

            payload = response.model_dump(mode="json", by_alias=True, exclude_none=True)
            page = payload.get("result", payload) or {}
            pages += 1

            if total_hits is None and page.get("total_hits") is not None:
                total_hits = int(page["total_hits"])

            page_hits = page.get("hits") or []
            hits.extend(page_hits[:remaining])

            if verbose:
                print(
                    f"[censys] page {pages}: +{len(page_hits)} hits "
                    f"({len(hits)}/{max_results})",
                    file=sys.stderr,
                )

            page_token = page.get("next_page_token") or None
            if not page_token or not page_hits:
                break

    return {
        "query": query,
        "total_hits": total_hits,
        "returned_hits": len(hits),
        "pages_fetched": pages,
        "requests_made": gateway.calls_made,
        "errors": errors,
        "hits": hits,
    }


def format_table(result: Dict[str, Any]) -> str:
    """Render a compact one-line-per-host summary."""
    lines = [
        f"query          : {result['query']}",
        f"total hits     : {result['total_hits']}",
        f"returned hits  : {result['returned_hits']} "
        f"(pages: {result['pages_fetched']}, requests: {result['requests_made']})",
        "",
    ]
    for i, hit in enumerate(result["hits"], start=1):
        host = (
            hit.get("host")
            or (hit.get("host_v1") or {}).get("resource")
            or {}
        )
        ip = host.get("ip") or hit.get("resource_type") or "?"
        location = host.get("location") or {}
        country = location.get("country", "")
        ports = sorted(
            {
                str(svc.get("port"))
                for svc in (host.get("services") or [])
                if svc.get("port") is not None
            },
            key=lambda p: int(p),
        )
        lines.append(
            f"{i:>3}. {ip:<40} {country:<20} ports: {','.join(ports) or '-'}"
        )
    for err in result["errors"]:
        lines.append(f"  ! {err}")
    return "\n".join(lines)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa assess"), not this file, which is not on their PATH.
    parser = argparse.ArgumentParser(
        prog=os.environ.get("CENSYS_TSA_PROG"),
        description="Run a Censys Platform search query with rate limiting.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("query", help="CenQL query string, e.g. '51.161.8.88'")
    parser.add_argument(
        "-n",
        "--max-results",
        type=int,
        default=10,
        help="Total number of hits to collect across pages",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=10,
        help=f"Hits requested per page (max {MAX_PAGE_SIZE})",
    )
    parser.add_argument(
        "-o", "--output", help="Write full JSON results to this file"
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("json", "table", "none"),
        default="json",
        help="Output rendering for stdout",
    )
    parser.add_argument("--org-id", default=CENSYS_ORG_ID, help="Censys organization ID")

    limits = parser.add_argument_group("rate limiting")
    limits.add_argument(
        "--min-interval",
        type=float,
        default=DEFAULT_MIN_INTERVAL,
        help="Minimum seconds between Censys requests",
    )
    limits.add_argument(
        "--max-per-minute",
        type=int,
        default=DEFAULT_MAX_PER_MINUTE,
        help="Maximum Censys requests per rolling 60s window (0 disables)",
    )
    limits.add_argument(
        "--budget-requests",
        type=int,
        default=DEFAULT_BUDGET_REQUESTS,
        help="Requests allowed per budget window, shared across runs (0 disables)",
    )
    limits.add_argument(
        "--budget-window",
        type=float,
        default=DEFAULT_BUDGET_WINDOW,
        help="Length of the rolling budget window, in seconds",
    )
    limits.add_argument(
        "--state-file",
        default=str(DEFAULT_STATE_FILE),
        help="Where the cross-run request budget is persisted",
    )
    limits.add_argument(
        "--no-wait",
        action="store_true",
        help="Fail instead of sleeping when a rate limit is hit",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Log progress")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    gateway = RateLimitGateway(
        min_interval=args.min_interval,
        max_per_minute=args.max_per_minute,
        budget_requests=args.budget_requests,
        budget_window=args.budget_window,
        state_file=Path(args.state_file) if args.state_file else None,
        block=not args.no_wait,
        verbose=args.verbose,
    )

    try:
        result = run_query(
            args.query,
            gateway,
            max_results=args.max_results,
            page_size=args.page_size,
            org_id=args.org_id,
            verbose=args.verbose,
        )
    except RateLimitError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    if args.output:
        with open(args.output, "w") as fh:
            json.dump(result, fh, indent=4)
        if args.verbose:
            print(f"[censys] wrote {args.output}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    elif args.format == "table":
        print(format_table(result))

    if result["errors"] and not result["hits"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
