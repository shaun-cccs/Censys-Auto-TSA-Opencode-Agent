#!/usr/bin/env python3
"""Aggregate Censys Platform results into buckets for fingerprint discovery.

Censys does not fingerprint every product, so a ``host.services.software``
query often under-counts or returns nothing. Aggregations let you take a broad
seed query (full-text, banner regex, CVE) and see which field values actually
characterize the matching hosts - ports, labels, HTML titles, favicon hashes,
certificate subjects - so you can build a precise host query.

Bucket counts are not host counts by default. The API counts documents at the
deepest nested level containing the field, so a host with several matching
services contributes several times - aggregating ``host.services.software.vendor``
over a 16,134-host population returned ``cisco: 35,774``. Pass ``--count-hosts``
(``count_by_level="."``) to count root documents instead and get real host
counts. Even then, buckets overlap: one host holds several ports, so the buckets
legitimately sum to more than the population.

``--count-hosts`` combined with the default ``filter_by_query=true`` is the
cheapest way to ask "how many hosts carry this value **on the same service** as
the query matched" - it reproduces a ``host.services:(<constraint> and
<field>=<value>)`` search for every bucket key at once.

Examples
--------
    python utils/censys_aggregate.py host.services.port '"MOVEit Transfer"'
    python utils/censys_aggregate.py host.services.labels.value 'host.services.vulns.id="CVE-2024-21762"'
    python utils/censys_aggregate.py host.services.endpoints.http.html_title '"Cisco ASA"' -k 25
    python utils/censys_aggregate.py host.services.software.vendor '<query>' --count-hosts
    python utils/censys_aggregate.py host.services.software.vendor '<query>' --compare-levels
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from censys_platform import SDK, models

from censys_query import (
    API_REQUEST_COST,
    CENSYS_ORG_ID,
    get_org_id,
    DEFAULT_BUDGET_REQUESTS,
    DEFAULT_BUDGET_WINDOW,
    DEFAULT_MAX_PER_MINUTE,
    DEFAULT_MIN_INTERVAL,
    DEFAULT_STATE_FILE,
    DEFAULT_TIMEOUT_MS,
    RETRYABLE_STATUS,
    CreditCeilingError,
    RateLimitError,
    RateLimitGateway,
    charge_credits,
    get_personal_access_token,
)

# Censys caps aggregation buckets at 2000.
MAX_BUCKETS = 2000
DEFAULT_BUCKETS = MAX_BUCKETS

# ``count_by_level`` chooses which document level a bucket count refers to.
# This is the API's "Count By" dropdown from the Report Builder UI.
#   ""              deepest level containing the field - counts service (or
#                   endpoint, or software) occurrences, so a host with several
#                   matching services contributes several times
#   "."             root documents - counts HOSTS, deduplicated
#   "host.services" a named intermediate level - counts services
# Buckets at any level may still overlap across bucket keys: one host can hold
# two different ports, so the buckets sum to more than the population.
COUNT_LEVEL_DEEPEST = ""
COUNT_LEVEL_HOST = "."
COUNT_LEVEL_SERVICE = "host.services"

# Fields worth aggregating on when hunting for a product fingerprint.
SUGGESTED_FIELDS = (
    "host.services.port",
    "host.services.protocol",
    "host.services.labels.value",
    "host.services.software.product",
    "host.services.software.vendor",
    "host.services.software.cpe",
    "host.services.endpoints.http.html_title",
    "host.services.endpoints.http.favicons.hash_shodan",
    "host.services.cert.parsed.subject.organization",
    "host.services.cert.parsed.subject.common_name",
    "host.services.jarm.fingerprint",
    "host.location.country",
    "host.autonomous_system.organization",
)


def censys_aggregate(
    sdk: SDK,
    field: str,
    query: str,
    gateway: RateLimitGateway,
    number_of_buckets: int = DEFAULT_BUCKETS,
    filter_by_query: bool = True,
    count_by_level: Optional[str] = None,
    max_retries: int = 4,
    base_delay: float = 1.0,
) -> Tuple[Optional[Any], Optional[str]]:
    """Run one aggregation, retrying transient failures.

    ``count_by_level`` selects the document level the bucket counts refer to;
    pass ``COUNT_LEVEL_HOST`` ("." ) to count hosts rather than the nested
    occurrences the API returns by default. ``None`` omits the field and takes
    the API default (deepest level containing ``field``).

    Costs 1 credit per call - an aggregation is an ordinary API action, not a
    free one - so it is charged against the session ledger like a search page.

    Returns ``(result, error)``; exactly one is non-None.
    """
    body: Dict[str, Any] = {
        "field": field,
        "number_of_buckets": min(number_of_buckets, MAX_BUCKETS),
        "query": query,
        "filter_by_query": filter_by_query,
    }
    if count_by_level is not None:
        body["count_by_level"] = count_by_level

    for attempt in range(max_retries):
        try:
            charge_credits(API_REQUEST_COST, query)
            gateway.acquire()
            res = sdk.global_data.aggregate(search_aggregate_input_body=body)
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


def _normalize_buckets(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Pull the bucket list out of an aggregation payload, whatever its shape."""
    node: Any = payload.get("result", payload) or {}
    for key in ("buckets", "aggregation", "aggregations"):
        if isinstance(node, dict) and key in node:
            node = node[key]
            if key == "buckets":
                break
    if isinstance(node, dict):
        node = node.get("buckets", [])
    if not isinstance(node, list):
        return []

    buckets = []
    for item in node:
        if not isinstance(item, dict):
            continue
        buckets.append(
            {
                "key": item.get("key", item.get("value")),
                "count": item.get("count", item.get("doc_count")),
            }
        )
    return buckets


def _summarize(
    payload: Dict[str, Any],
    field: str,
    query: str,
    count_by_level: Optional[str],
) -> Dict[str, Any]:
    """Build one aggregation result record from a raw payload.

    The aggregate endpoint returns ``total_count``, not the ``total_hits`` the
    search endpoint returns; reading the search field here yielded ``None`` on
    every aggregation. ``other_count`` is the tail beyond the requested buckets
    and is the only way to know a distribution was truncated.
    """
    node: Dict[str, Any] = (payload.get("result", payload) or {})
    buckets = _normalize_buckets(payload)
    total = node.get("total_count", node.get("total_hits"))
    return {
        "field": field,
        "query": query,
        "count_by_level": count_by_level,
        "total_count": total,
        # Kept so existing callers and saved JSON keep working.
        "total_hits": total,
        "other_count": node.get("other_count"),
        "is_more_than_total_hits": node.get("is_more_than_total_hits"),
        "bucket_sum": sum(b["count"] for b in buckets if isinstance(b["count"], int)),
        "bucket_count": len(buckets),
        "buckets": buckets,
        "errors": [],
    }


def run_aggregate(
    field: str,
    query: str,
    gateway: RateLimitGateway,
    number_of_buckets: int = DEFAULT_BUCKETS,
    filter_by_query: bool = True,
    count_by_level: Optional[str] = None,
    org_id: str = CENSYS_ORG_ID,
    token: Optional[str] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Aggregate a single field for a query."""
    token = token or get_personal_access_token()
    with SDK(
        organization_id=get_org_id(org_id),
        personal_access_token=token,
        timeout_ms=DEFAULT_TIMEOUT_MS,
    ) as sdk:
        response, error = censys_aggregate(
            sdk,
            field,
            query,
            gateway,
            number_of_buckets=number_of_buckets,
            filter_by_query=filter_by_query,
            count_by_level=count_by_level,
        )

    if error:
        return {"field": field, "query": query, "buckets": [], "errors": [error]}

    payload = response.model_dump(mode="json", by_alias=True, exclude_none=True)
    result = _summarize(payload, field, query, count_by_level)
    if verbose:
        print(f"[aggregate] {field}: {result['bucket_count']} buckets", file=sys.stderr)
        result["raw"] = payload
    return result


def run_multi_aggregate(
    fields: List[str],
    query: str,
    gateway: RateLimitGateway,
    number_of_buckets: int = DEFAULT_BUCKETS,
    filter_by_query: bool = True,
    count_by_level: Optional[str] = None,
    org_id: str = CENSYS_ORG_ID,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Aggregate several fields for the same query, reusing one SDK session."""
    token = get_personal_access_token()
    results: List[Dict[str, Any]] = []

    with SDK(
        organization_id=get_org_id(org_id),
        personal_access_token=token,
        timeout_ms=DEFAULT_TIMEOUT_MS,
    ) as sdk:
        for fld in fields:
            response, error = censys_aggregate(
                sdk,
                fld,
                query,
                gateway,
                number_of_buckets=number_of_buckets,
                filter_by_query=filter_by_query,
                count_by_level=count_by_level,
            )
            if error:
                results.append(
                    {"field": fld, "query": query, "buckets": [], "errors": [error]}
                )
                continue
            payload = response.model_dump(mode="json", by_alias=True, exclude_none=True)
            record = _summarize(payload, fld, query, count_by_level)
            if verbose:
                print(
                    f"[aggregate] {fld}: {record['bucket_count']} buckets",
                    file=sys.stderr,
                )
            results.append(record)

    return {
        "query": query,
        "count_by_level": count_by_level,
        "requests_made": gateway.calls_made,
        "aggregations": results,
    }


_LEVEL_LABEL = {
    COUNT_LEVEL_DEEPEST: "deepest nested level (API default)",
    COUNT_LEVEL_HOST: "host (root documents)",
}


def format_buckets(result: Dict[str, Any], top: int = 25) -> str:
    """Render one aggregation as a ranked list."""
    level = result.get("count_by_level")
    label = _LEVEL_LABEL.get(level, level) if level is not None else _LEVEL_LABEL[""]
    total = result.get("total_count", result.get("total_hits"))
    lines = [
        f"field      : {result['field']}",
        f"query      : {result['query']}",
        f"counting   : {label}",
        f"total      : {total}",
        f"buckets    : {result.get('bucket_count', len(result['buckets']))}"
        f"  (sum {result.get('bucket_sum')}, other {result.get('other_count')})",
        "",
    ]
    for i, bucket in enumerate(result["buckets"][:top], start=1):
        count = bucket["count"]
        count_str = f"{count:,}" if isinstance(count, int) else str(count)
        lines.append(f"{i:>3}. {count_str:>12}  {bucket['key']}")
    remaining = len(result["buckets"]) - top
    if remaining > 0:
        lines.append(f"     ... {remaining} more buckets")
    for err in result.get("errors", []):
        lines.append(f"  ! {err}")
    return "\n".join(lines)


def compare_levels(
    default_aggs: List[Dict[str, Any]],
    host_aggs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Pair each field's default-level buckets against its host-level buckets.

    ``inflation`` is default count / host count for one bucket key. A value of
    1.0 means every host contributed exactly one occurrence of that value, so
    the default count happens to be a host count. Anything above 1.0 means the
    default count is an occurrence count and must not be quoted as hosts.
    """
    by_field = {agg["field"]: agg for agg in host_aggs}
    rows: List[Dict[str, Any]] = []

    for agg in default_aggs:
        host_agg = by_field.get(agg["field"])
        if not host_agg or agg.get("errors") or host_agg.get("errors"):
            continue
        host_counts = {b["key"]: b["count"] for b in host_agg["buckets"]}
        keys = []
        for bucket in agg["buckets"]:
            hosts = host_counts.get(bucket["key"])
            inflation = None
            if isinstance(hosts, int) and hosts:
                inflation = bucket["count"] / hosts
            keys.append(
                {
                    "key": bucket["key"],
                    "default_count": bucket["count"],
                    "host_count": hosts,
                    "inflation": inflation,
                }
            )
        ratios = [k["inflation"] for k in keys if k["inflation"] is not None]
        rows.append(
            {
                "field": agg["field"],
                "default_total": agg.get("total_count"),
                "host_total": host_agg.get("total_count"),
                "default_bucket_sum": agg.get("bucket_sum"),
                "host_bucket_sum": host_agg.get("bucket_sum"),
                "max_inflation": max(ratios) if ratios else None,
                "keys": keys,
            }
        )
    return rows


def format_comparison(rows: List[Dict[str, Any]], top: int = 25) -> str:
    """Render the default-level vs host-level comparison."""
    lines = ["count level comparison (default vs count_by_level='.')", ""]
    for row in rows:
        lines.append(f"field      : {row['field']}")
        lines.append(
            f"total      : {row['default_total']} default"
            f"  /  {row['host_total']} hosts"
        )
        lines.append(
            f"bucket sum : {row['default_bucket_sum']} default"
            f"  /  {row['host_bucket_sum']} hosts"
        )
        max_inf = row["max_inflation"]
        lines.append(
            "max inflate: "
            + (f"{max_inf:.2f}x" if max_inf is not None else "n/a")
            + ("  - default counts are host counts" if max_inf == 1.0 else "")
        )
        lines.append("")
        lines.append(f"{'default':>12} {'hosts':>12} {'x':>7}  key")
        for entry in row["keys"][:top]:
            hosts = entry["host_count"]
            inf = entry["inflation"]
            lines.append(
                f"{entry['default_count']:>12,} "
                f"{hosts if hosts is not None else '-':>12} "
                f"{f'{inf:.2f}' if inf is not None else '-':>7}  {entry['key']}"
            )
        lines.append("")
    return "\n".join(lines)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa assess"), not this file, which is not on their PATH.
    parser = argparse.ArgumentParser(
        prog=os.environ.get("CENSYS_TSA_PROG"),
        description="Aggregate Censys results by field to discover product fingerprints.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "field",
        nargs="?",
        help="Field to bucket on, e.g. host.services.port. Omit with --suggest-fields.",
    )
    parser.add_argument("query", help="CenQL query to aggregate over")
    parser.add_argument(
        "--suggest-fields",
        action="store_true",
        help="Aggregate across a standard set of fingerprint-discovery fields",
    )
    parser.add_argument(
        "-b",
        "--buckets",
        type=int,
        default=DEFAULT_BUCKETS,
        help=f"Number of buckets to request (max {MAX_BUCKETS})",
    )
    parser.add_argument(
        "-k",
        "--top",
        type=int,
        default=25,
        help="Buckets to display per field in report format",
    )
    parser.add_argument(
        "--no-filter-by-query",
        action="store_true",
        help="Count all values on matching hosts instead of only query-matching ones",
    )

    level = parser.add_argument_group("count level (Report Builder 'Count By')")
    level.add_argument(
        "--count-by-level",
        metavar="LEVEL",
        default=None,
        help=(
            "Document level each bucket count refers to: '' deepest nested "
            "level (API default), '.' root/host documents, or a nested path "
            "such as host.services"
        ),
    )
    level.add_argument(
        "--count-hosts",
        dest="count_by_level",
        action="store_const",
        const=COUNT_LEVEL_HOST,
        help="Shorthand for --count-by-level '.' - bucket counts are host counts",
    )
    level.add_argument(
        "--count-services",
        dest="count_by_level",
        action="store_const",
        const=COUNT_LEVEL_SERVICE,
        help=f"Shorthand for --count-by-level {COUNT_LEVEL_SERVICE!r}",
    )
    level.add_argument(
        "--compare-levels",
        action="store_true",
        help=(
            "Run each field at both the default level and the host level and "
            "show the inflation factor. Doubles the credit cost."
        ),
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("report", "json"),
        default="report",
        help="Output rendering for stdout",
    )
    parser.add_argument("-o", "--output", help="Write full JSON results to this file")
    parser.add_argument("--org-id", default=CENSYS_ORG_ID, help="Censys organization ID")

    limits = parser.add_argument_group("rate limiting")
    limits.add_argument("--min-interval", type=float, default=DEFAULT_MIN_INTERVAL)
    limits.add_argument("--max-per-minute", type=int, default=DEFAULT_MAX_PER_MINUTE)
    limits.add_argument("--budget-requests", type=int, default=DEFAULT_BUDGET_REQUESTS)
    limits.add_argument("--budget-window", type=float, default=DEFAULT_BUDGET_WINDOW)
    limits.add_argument("--state-file", default=str(DEFAULT_STATE_FILE))
    limits.add_argument(
        "--no-wait",
        action="store_true",
        help="Fail instead of sleeping when a rate limit is hit",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Log progress")
    args = parser.parse_args(argv)

    if not args.suggest_fields and not args.field:
        parser.error("a field is required unless --suggest-fields is used")
    return args


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

    fields = list(SUGGESTED_FIELDS) if args.suggest_fields else [args.field]
    if args.suggest_fields and args.field:
        fields = [args.field] + [f for f in fields if f != args.field]

    try:
        result = run_multi_aggregate(
            fields,
            args.query,
            gateway,
            number_of_buckets=args.buckets,
            filter_by_query=not args.no_filter_by_query,
            count_by_level=args.count_by_level,
            org_id=args.org_id,
            verbose=args.verbose,
        )
        if args.compare_levels:
            host_level = run_multi_aggregate(
                fields,
                args.query,
                gateway,
                number_of_buckets=args.buckets,
                filter_by_query=not args.no_filter_by_query,
                count_by_level=COUNT_LEVEL_HOST,
                org_id=args.org_id,
                verbose=args.verbose,
            )
            result["host_level"] = host_level["aggregations"]
            result["level_comparison"] = compare_levels(
                result["aggregations"], host_level["aggregations"]
            )
            result["requests_made"] = gateway.calls_made
    except RateLimitError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))
        if args.verbose:
            print(f"[aggregate] wrote {args.output}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        blocks = [format_buckets(agg, top=args.top) for agg in result["aggregations"]]
        print(("\n" + "-" * 72 + "\n").join(blocks))
        if args.compare_levels:
            print("\n" + "-" * 72 + "\n")
            print(format_comparison(result["level_comparison"], top=args.top))

    if all(agg["errors"] for agg in result["aggregations"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
