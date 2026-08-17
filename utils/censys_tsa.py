#!/usr/bin/env python3
"""Compute a Censys Threat Surface Assessment (TSA) for a product or CVE.

Given a base CenQL *host* query that identifies a product - or a CVE ID, or
both - this emits:

1. The Censys Platform search URL for the query.
2. The global TSA count (honeypots excluded).
3. The Canada TSA count (honeypots excluded).
4. The Censys credits (tokens) the run consumed, unless ``--no-credits``.

Only ``total_hits`` is needed for counts, so each query fetches a single hit.

Passing ``--cve`` looks the CVE up on cve.org (falling back to NVD) and adds
its severity and KEV status to the report. With no base query, the count is the
Censys vulnerability tag for that CVE. With a base query, the CVE narrows it to
the instances Censys flags as vulnerable - that is how you scope a CVE down to
one of the several products it affects.

Examples
--------
    python utils/censys_tsa.py 'host.services.software: (vendor="Fortinet" and product="FortiOS")'
    python utils/censys_tsa.py --cve CVE-2024-21762
    python utils/censys_tsa.py 'host.services.software:(vendor="fortinet" and product="fortios")' --cve CVE-2024-21762
    python utils/censys_tsa.py 'host.services.software.product="httpd"' --country Germany
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote

from censys_credits import CreditTracker, format_tracker_summary
from censys_query import (
    CENSYS_ORG_ID,
    DEFAULT_BUDGET_REQUESTS,
    DEFAULT_BUDGET_WINDOW,
    DEFAULT_MAX_PER_MINUTE,
    DEFAULT_MIN_INTERVAL,
    DEFAULT_STATE_FILE,
    RateLimitError,
    RateLimitGateway,
    run_query,
)
from cve_lookup import CVELookupError, lookup_cve, normalize_cve_id

PLATFORM_SEARCH_URL = "https://platform.censys.io/search"

# Honeypot exclusion applied to every TSA count.
HONEYPOT_EXCLUSION = 'not labels: "HONEYPOT"'
DEFAULT_COUNTRY = "Canada"


def platform_url(query: str, org_id: str = CENSYS_ORG_ID) -> str:
    """Build a shareable Censys Platform search URL for a query.

    The org is omitted rather than guessed when it is unknown: a URL carrying
    somebody else's organization looks authoritative and silently sends the
    reader to a tenant they cannot see.
    """
    url = f"{PLATFORM_SEARCH_URL}?q={quote(query, safe='')}"
    return f"{url}&org={org_id}" if org_id else url


def wrap(base_query: str) -> str:
    """Parenthesize a base query so appended clauses bind correctly."""
    stripped = base_query.strip()
    return stripped if stripped.startswith("(") and stripped.endswith(")") else f"({stripped})"


def build_queries(
    base_query: str, country: str = DEFAULT_COUNTRY
) -> Dict[str, str]:
    """Derive the platform, global TSA, and country TSA queries."""
    base = wrap(base_query)
    global_tsa = f"{base} and {HONEYPOT_EXCLUSION}"
    return {
        "platform": base_query.strip(),
        "global_tsa": global_tsa,
        "country_tsa": f'{global_tsa} and host.location.country="{country}"',
    }


def count_hits(
    query: str, gateway: RateLimitGateway, org_id: str, verbose: bool = False
) -> Dict[str, Any]:
    """Return ``total_hits`` for a query using a single-result request."""
    result = run_query(
        query,
        gateway,
        max_results=1,
        page_size=1,
        org_id=org_id,
        verbose=verbose,
    )
    return {
        "query": query,
        "url": platform_url(query, org_id),
        "total_hits": result["total_hits"],
        "errors": result["errors"],
    }


def run_tsa(
    base_query: str,
    gateway: RateLimitGateway,
    country: str = DEFAULT_COUNTRY,
    org_id: str = CENSYS_ORG_ID,
    product: Optional[str] = None,
    track_credits: bool = True,
    cve: Optional[Dict[str, Any]] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Run the platform, global, and country counts for a base query."""
    queries = build_queries(base_query, country)

    tracker: Optional[CreditTracker] = None
    if track_credits:
        tracker = CreditTracker(org_id=org_id, verbose=verbose)
        tracker.start()

    try:
        # The global and country counts are independent queries, so they go out
        # together. Serially they cost two round trips plus a pacing interval for
        # a number the user is waiting on; the gateway still applies whatever
        # pacing the profile asks for, so this is free when pacing is off and
        # harmless when it is not.
        with ThreadPoolExecutor(max_workers=2) as pool:
            global_future = pool.submit(
                count_hits, queries["global_tsa"], gateway, org_id, verbose
            )
            country_future = pool.submit(
                count_hits, queries["country_tsa"], gateway, org_id, verbose
            )
            global_count = global_future.result()
            country_count = country_future.result()
        result = {
            "product": product,
            "country": country,
            "platform": {
                "query": queries["platform"],
                "url": platform_url(queries["platform"], org_id),
            },
            "global_tsa": global_count,
            "country_tsa": country_count,
            "requests_made": gateway.calls_made,
        }
    finally:
        if tracker is not None:
            summary = tracker.stop()

    if cve is not None:
        result["cve"] = cve
    if tracker is not None:
        result["credits"] = summary
    return result


def format_cve_block(record: Dict[str, Any]) -> List[str]:
    """Render the CVE context lines shown above a CVE-driven TSA."""
    cvss = record.get("cvss") or {}
    lines = [f"CVE            : {record['cve_id']}"]
    if cvss:
        lines.append(
            f"  severity     : {cvss.get('score')} {cvss.get('severity') or ''} "
            f"(CVSS v{cvss.get('version')})".rstrip()
        )
    if record.get("kev"):
        lines.append(f"  CISA KEV     : yes (added {str(record.get('kev_added'))[:10]})")
    lines.append(f"  source       : {record.get('source')} - {record.get('source_url')}")
    if record.get("secondary_source"):
        lines.append(
            f"  also         : {record['secondary_source']} - "
            f"{record.get('secondary_source_url')}"
        )
    return lines


def format_report(result: Dict[str, Any]) -> str:
    """Render the TSA as a human-readable report."""
    def count(section: str) -> str:
        hits = result[section]["total_hits"]
        return f"{hits:,}" if isinstance(hits, int) else "unknown"

    lines: List[str] = []
    if result.get("product"):
        lines.append(f"Product        : {result['product']}")
    if result.get("cve"):
        lines += format_cve_block(result["cve"])
    country_label = f"{result['country']} TSA"
    lines += [
        "",
        "Platform query",
        f"  {result['platform']['query']}",
        f"  {result['platform']['url']}",
        "",
        f"{'Global TSA':<15}: {count('global_tsa')} hosts",
        f"  {result['global_tsa']['query']}",
        f"  {result['global_tsa']['url']}",
        "",
        f"{country_label:<15}: {count('country_tsa')} hosts",
        f"  {result['country_tsa']['query']}",
        f"  {result['country_tsa']['url']}",
    ]
    for section in ("global_tsa", "country_tsa"):
        for err in result[section]["errors"]:
            lines.append(f"  ! {section}: {err}")
    if result.get("credits"):
        lines += ["", format_tracker_summary(result["credits"])]
    return "\n".join(lines)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa assess"), not this file, which is not on their PATH.
    parser = argparse.ArgumentParser(
        prog=os.environ.get("CENSYS_TSA_PROG"),
        description="Compute a global and country-scoped Censys TSA for a product.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "query",
        nargs="?",
        help=(
            "Base CenQL host query identifying the product. Optional when "
            "--cve is given; combined with --cve it scopes the CVE to this "
            "product."
        ),
    )
    parser.add_argument(
        "--cve",
        help=(
            "CVE ID to scope or drive the TSA. Looked up on cve.org, falling "
            "back to NVD, and intersected with the base query if one is given."
        ),
    )
    parser.add_argument(
        "--product", help="Product name to label the report with"
    )
    parser.add_argument(
        "--country",
        default=DEFAULT_COUNTRY,
        help="Country to scope the second TSA count to",
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
    parser.add_argument(
        "--no-credits",
        dest="track_credits",
        action="store_false",
        help="Skip measuring the Censys credits consumed by this run",
    )

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
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if not args.query and not args.cve:
        print("error: provide a base query, a --cve, or both", file=sys.stderr)
        return 2

    cve_record: Optional[Dict[str, Any]] = None
    if args.cve:
        try:
            record = lookup_cve(args.cve, verbose=args.verbose)
            # Keep the TSA result compact: the full record is context for the
            # operator, not part of the assessment.
            cve_record = {
                k: v for k, v in record.items() if k not in ("raw", "secondary")
            }
        except (CVELookupError, ValueError) as e:
            print(f"error: CVE lookup failed: {e}", file=sys.stderr)
            # Without a query there is nothing left to count.
            if not args.query:
                return 1

    base_query = args.query
    vuln_tag = f'host.services.vulns.id="{normalize_cve_id(args.cve)}"' if args.cve else None
    if not base_query:
        base_query = vuln_tag
    elif vuln_tag:
        # An explicit query plus a CVE means "this product, but only the
        # instances Censys flags as vulnerable to this CVE".
        base_query = f"({base_query}) and {vuln_tag}"

    product_label = args.product or (normalize_cve_id(args.cve) if args.cve else None)

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
        result = run_tsa(
            base_query,
            gateway,
            country=args.country,
            org_id=args.org_id,
            product=product_label,
            track_credits=args.track_credits,
            cve=cve_record,
            verbose=args.verbose,
        )
    except RateLimitError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))
        if args.verbose:
            print(f"[tsa] wrote {args.output}", file=sys.stderr)

    print(json.dumps(result, indent=2) if args.format == "json" else format_report(result))

    if any(result[s]["errors"] for s in ("global_tsa", "country_tsa")):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
