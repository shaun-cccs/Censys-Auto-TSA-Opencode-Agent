#!/usr/bin/env python3
"""Run many independent Censys calls in one process. Reached as `tsa batch`,
`tsa probe` and `tsa candidates`.

WHY THIS EXISTS
---------------
A TSA is turn-bound, not query-bound. One Censys action costs about a second
(`tsa timeline` measures it); a real assessment issues a hundred of them and
takes half an hour, because each one is a separate agent turn. The fix is not a
faster API, it is fewer turns: issue the independent calls together and read one
answer.

Three entrypoints, all the same engine:

``batch``
    An arbitrary set of counts, samples and aggregations. The general primitive.

``probe``
    Step 1 in a single call: the full-text seed sample, the product bucket in
    **all three** tag trees - software, hardware, operating_system - and the
    decoded-protocol bucket. The tag sweep is mandatory (second principle) and
    used to cost four turns; the protocol bucket is mandatory because tagging
    and HTTP content are not the only evidence layers, and a structured protocol
    document outranks any banner regex.

``candidates``
    Step 8b in a single call: for each candidate signal, how many hosts it adds
    over the base query (`<candidate> and not (<base>)`) *and* what those
    incremental hosts' HTML titles are. The count alone is not evidence - the
    buckets are what tell you the increment is coherently the product - so this
    always fetches both, because a tool that made the check optional would get
    it skipped.

WHAT IT DOES NOT DO
-------------------
Deep pagination. Batch items fetch a single page, because the point is
wide-and-shallow. Use `tsa search` when you need many results from one query.

Examples
--------
    python utils/censys_batch.py probe '"MOVEit Transfer"'
    python utils/censys_batch.py batch --count '<q1>' --count '<q2>' \
        --agg host.services.port '<q1>'
    python utils/censys_batch.py candidates '<base>' '<cand1>' '<cand2>'
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional

from censys_platform import SDK

from censys_aggregate import (
    COUNT_LEVEL_HOST,
    DEFAULT_BUCKETS,
    MAX_BUCKETS,
    censys_aggregate,
    summarize,
)
from censys_query import (
    CENSYS_ORG_ID,
    DEFAULT_BUDGET_REQUESTS,
    DEFAULT_BUDGET_WINDOW,
    DEFAULT_CONCURRENCY,
    DEFAULT_MAX_PER_MINUTE,
    DEFAULT_MIN_INTERVAL,
    DEFAULT_STATE_FILE,
    DEFAULT_TIMEOUT_MS,
    MAX_PAGE_SIZE,
    RateLimitError,
    RateLimitGateway,
    censys_search_page,
    get_org_id,
    get_personal_access_token,
)

#  Step 1's mandated sweep: the seed itself, then the product bucket in each of
#  the three tag trees. Censys keeps them separately and appliances are commonly
#  absent from `software` while fully tagged under `hardware`, so a probe that
#  checks one tree is the single most common way to conclude "untagged" wrongly.
PROBE_TREES = (
    "host.services.software.product",
    "host.services.hardware.product",
    "host.operating_system.product",
)

#  The fourth layer, and it is not a tag tree: what protocol did Censys actually
#  DECODE on these services?
#
#  Tagging and HTTP content are two layers, not all of them. Censys decodes a
#  set of named service protocols and stores a structured sub-document for each
#  - `any_connect`, `ike`, `kubernetes`, `mysql` and so on - and those documents
#  are better evidence than any banner regex, because they are parsed fields
#  rather than strings that anything may echo.
#
#  Measured, and the reason this is now mandatory: an ASA/FTD assessment ran
#  four fingerprint workers and five deep-dive workers over the three tag trees
#  and every HTTP/TLS content family, and every one of them missed
#  `host.services.protocol="ANYCONNECT"` with its `any_connect.groups` field.
#  The default tunnel-group name `DefaultWEBVPNGroup` alone identified 1,661
#  exposed Cisco VPN head-ends that carried no OS tag at all - roughly 1,500 of
#  them untagged in all three trees. Aggregating ports is not the same check:
#  the run did aggregate 443 and UDP 500 and still learned nothing, because a
#  port number is not a decoded protocol.
#
#  One credit, always on. The failure it prevents is concluding "not tagged, and
#  no content signal either" while a structured protocol document sits unread.
PROBE_PROTOCOL = ("host.services.protocol",)

#  --wide: the fields worth having when the tag trees come back empty and step 3
#  is where this is heading anyway. Vendors first, because step 2 needs the
#  vendor to build a nested query at all.
PROBE_WIDE = (
    "host.services.software.vendor",
    "host.services.hardware.vendor",
    "host.services.port",
    "host.services.endpoints.http.html_title",
    "host.services.endpoints.http.favicons.hash_shodan",
)

#  Scoping clause that turns a bare full-text seed into a host query.
#
#  Measured: `"MOVEit Transfer"` returns webproperty_v1 records - hostname and
#  port, no IP - mixed in with hosts, because a full-text query searches every
#  resource type. `"MOVEit Transfer" and host.ip: *` returns 2,657 hosts, which
#  is the same population the three tag-tree aggregations see (2,655). Since
#  every count in this workflow must come from a host query, the probe scopes its
#  sample and prints the query it actually ran.
HOST_SCOPE_CLAUSE = "host.ip: *"

#  Retry policy for a batch item, deliberately shorter than for a lone call.
#
#  A single `tsa search` can afford four attempts with exponential backoff: it is
#  the only thing the caller is waiting for. Inside a batch it is not - the whole
#  batch finishes when its slowest item does, so one failing query would hold
#  nineteen finished answers for seven seconds of backoff. A batch item that
#  fails twice is reported as failed, and re-running that one item costs one turn
#  and one credit.
BATCH_MAX_RETRIES = 2
BATCH_BASE_DELAY = 0.5

#  What `candidates` buckets over the incremental population. A title tells you
#  in one line whether the extra hosts are the product or a coincidence.
DEFAULT_WITNESS_FIELD = "host.services.endpoints.http.html_title"


def parenthesize(query: str) -> str:
    """Wrap a query so an appended clause binds to all of it, not its tail."""
    stripped = query.strip()
    if stripped.startswith("(") and stripped.endswith(")"):
        return stripped
    return f"({stripped})"


def host_scoped(seed: str) -> str:
    """Scope a seed to host records, unless it already says so itself."""
    if HOST_SCOPE_CLAUSE in seed:
        return seed
    return f"{parenthesize(seed)} and {HOST_SCOPE_CLAUSE}"


# ------------------------------------------------------------------ the engine


def make_item(
    op: str,
    query: str,
    field: str = "",
    label: str = "",
    max_results: int = 3,
    buckets: int = DEFAULT_BUCKETS,
    count_by_level: Optional[str] = None,
    filter_by_query: bool = True,
) -> Dict[str, Any]:
    """One unit of work. ``op`` is count, sample or agg."""
    if op not in {"count", "sample", "agg"}:
        raise ValueError(f"unknown op {op!r} (count, sample or agg)")
    if op == "agg" and not field:
        raise ValueError("an agg item needs a field")
    return {
        "op": op,
        "query": query,
        "field": field,
        "label": label,
        "max_results": max_results,
        "buckets": buckets,
        "count_by_level": count_by_level,
        "filter_by_query": filter_by_query,
    }


def _run_item(item: Dict[str, Any], sdk: SDK, gateway: RateLimitGateway) -> Dict[str, Any]:
    """Execute one item. Errors are returned, never raised.

    A batch of twenty must not lose nineteen answers because one query was
    malformed or the backend timed out on it - which is exactly what a heavy
    regex does. Each item carries its own error.
    """
    out: Dict[str, Any] = {
        "op": item["op"],
        "label": item.get("label") or "",
        "query": item["query"],
        "field": item.get("field") or None,
        "total": None,
        "hits": [],
        "buckets": [],
        "error": None,
    }
    started = time.perf_counter()
    try:
        if item["op"] == "agg":
            response, error = censys_aggregate(
                sdk,
                item["field"],
                item["query"],
                gateway,
                number_of_buckets=min(int(item["buckets"]), MAX_BUCKETS),
                filter_by_query=bool(item.get("filter_by_query", True)),
                count_by_level=item.get("count_by_level"),
                max_retries=BATCH_MAX_RETRIES,
                base_delay=BATCH_BASE_DELAY,
            )
            if error:
                out["error"] = error
            else:
                payload = response.model_dump(mode="json", by_alias=True, exclude_none=True)
                record = summarize(
                    payload, item["field"], item["query"], item.get("count_by_level")
                )
                out["total"] = _as_count(record.get("total_count"))
                out["buckets"] = record["buckets"]
                out["other_count"] = record.get("other_count")
        else:
            wanted = 1 if item["op"] == "count" else max(1, int(item["max_results"]))
            response, error = censys_search_page(
                sdk,
                item["query"],
                gateway,
                page_size=min(wanted, MAX_PAGE_SIZE),
                max_retries=BATCH_MAX_RETRIES,
                base_delay=BATCH_BASE_DELAY,
            )
            if error:
                out["error"] = error
            else:
                payload = response.model_dump(mode="json", by_alias=True, exclude_none=True)
                page = payload.get("result", payload) or {}
                out["total"] = _as_count(page.get("total_hits"))
                if item["op"] == "sample":
                    out["hits"] = (page.get("hits") or [])[:wanted]
    except Exception as exc:  # noqa: BLE001 - one bad item must not sink the batch
        out["error"] = f"{type(exc).__name__}: {str(exc)[:160]}"
    out["ms"] = round((time.perf_counter() - started) * 1000.0, 1)
    return out


def run_batch(
    items: List[Dict[str, Any]],
    gateway: RateLimitGateway,
    org_id: str = CENSYS_ORG_ID,
    concurrency: int = DEFAULT_CONCURRENCY,
    timeout_ms: int = DEFAULT_TIMEOUT_MS,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Run every item, concurrently, and return results in the caller's order.

    One SDK is shared: httpx.Client is thread-safe and pooling its connections
    is most of why this is faster than N processes. The gateway is shared too,
    so pacing and the credit ledger still see every request - a batch is not a
    way around them, only a way around the turn cost.
    """
    if not items:
        return {"items": [], "requests_made": 0, "wall_seconds": 0.0}

    token = get_personal_access_token()
    results: List[Optional[Dict[str, Any]]] = [None] * len(items)
    started = time.perf_counter()

    with SDK(
        organization_id=get_org_id(org_id),
        personal_access_token=token,
        timeout_ms=timeout_ms,
    ) as sdk:
        def one(index: int) -> None:
            if verbose:
                print(f"[batch] {index + 1}/{len(items)} {items[index]['op']}", file=sys.stderr)
            results[index] = _run_item(items[index], sdk, gateway)

        workers = max(1, min(int(concurrency), len(items)))
        if workers == 1:
            for index in range(len(items)):
                one(index)
        else:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                for future in [pool.submit(one, i) for i in range(len(items))]:
                    future.result()

    return {
        "items": [r for r in results if r is not None],
        "requests_made": gateway.calls_made,
        "wall_seconds": round(time.perf_counter() - started, 2),
        "concurrency": max(1, min(int(concurrency), len(items))),
    }


# ------------------------------------------------------------------- rendering


def _as_count(value: Any) -> Optional[int]:
    """Coerce a total to int, or None.

    The search endpoint returns ``total_hits`` as a float and the aggregate
    endpoint returns an int. Leaving the float in place made every renderer and
    every downstream `isinstance(x, int)` check treat a perfectly good count as
    missing data, which read as a failed query. Normalise once, here.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return int(value)


def _count(value: Any) -> str:
    """Render a count, or "?" when there genuinely is not one."""
    number = _as_count(value)
    return "?" if number is None else f"{number:,}"


def _host_line(hit: Dict[str, Any]) -> str:
    """One line describing a hit - and saying so when the hit is not a host.

    A bare full-text query is NOT host-scoped: `"MOVEit Transfer"` returns
    `webproperty_v1` records (hostname + port, no IP) alongside hosts. Rendering
    those as "?" - which is what the older table formatter did - hides the single
    most important fact about the result, because counts must come from host
    queries. Name the resource type instead.
    """
    host = hit.get("host") or (hit.get("host_v1") or {}).get("resource") or {}
    if host.get("ip"):
        ip = host["ip"]
        country = (host.get("location") or {}).get("country", "")
        ports = sorted(
            {str(s.get("port")) for s in (host.get("services") or []) if s.get("port")},
            key=lambda p: int(p),
        )
        return f"{ip} ({country}{', ' if country else ''}{','.join(ports[:6])})"

    kind = next((key for key in hit if key != "extensions"), "unknown")
    resource = (hit.get(kind) or {}).get("resource") or {}
    for key in ("hostname", "ip", "name", "fingerprint_sha256"):
        if resource.get(key):
            port = resource.get("port")
            suffix = f":{port}" if port else ""
            return f"[{kind}] {resource[key]}{suffix}   <- not a host record"
    return f"[{kind}] (no identifier)   <- not a host record"


def _non_host_hits(hits: List[Dict[str, Any]]) -> int:
    return sum(
        1
        for hit in hits
        if not (hit.get("host") or (hit.get("host_v1") or {}).get("resource") or {}).get("ip")
    )


def format_batch(result: Dict[str, Any], top: int = 10) -> str:
    lines = [
        f"batch: {len(result['items'])} calls · {result['wall_seconds']}s wall · "
        f"concurrency {result.get('concurrency', 1)} · "
        f"{result['requests_made']} requests charged",
        "",
    ]
    for index, item in enumerate(result["items"], start=1):
        head = f"[{index}] {item['op']:<7}"
        if item["error"]:
            lines.append(f"{head} ERROR  {item['error']}")
            lines.append(f"        query: {item['query'][:140]}")
            lines.append("")
            continue
        if item["op"] == "agg":
            lines.append(f"{head} {item['field']}  total {_count(item['total'])}")
            lines.append(f"        over: {item['query'][:140]}")
            for rank, bucket in enumerate(item["buckets"][:top], start=1):
                lines.append(
                    f"        {rank:>3}. {_count(bucket['count']):>12}  {bucket['key']}"
                )
            remaining = len(item["buckets"]) - top
            if remaining > 0:
                lines.append(f"             ... {remaining} more buckets")
        else:
            lines.append(f"{head} {_count(item['total'])} hosts   {item['query'][:120]}")
            for hit in item["hits"]:
                lines.append(f"        - {_host_line(hit)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_probe(result: Dict[str, Any], seed: str, top: int = 12) -> str:
    lines = [
        f"probe seed : {seed}",
        f"calls      : {len(result['items'])} · {result['wall_seconds']}s wall",
        "",
    ]
    for item in result["items"]:
        if item["op"] == "sample":
            lines.append(f"host sample    : {_count(item['total'])} hosts")
            if item["query"] != seed:
                lines.append(f"  query ran    : {item['query']}")
            for hit in item["hits"]:
                lines.append(f"  - {_host_line(hit)}")
            if item["error"]:
                lines.append(f"  ! {item['error']}")
            if _non_host_hits(item["hits"]):
                lines.append(
                    "  NOTE: some hits are not host records. A full-text seed searches\n"
                    "        every resource type, and counts must come from host queries."
                )
            lines.append("")
            continue
        tree = item["field"]
        if item["error"]:
            lines.append(f"{tree}\n  ! {item['error']}\n")
            continue
        if not item["buckets"]:
            lines.append(f"{tree}\n  (no buckets - nothing tagged in this tree)\n")
            continue
        lines.append(f"{tree}   total {_count(item['total'])}")
        for rank, bucket in enumerate(item["buckets"][:top], start=1):
            lines.append(f"  {rank:>3}. {_count(bucket['count']):>12}  {bucket['key']}")
        remaining = len(item["buckets"]) - top
        if remaining > 0:
            lines.append(f"       ... {remaining} more buckets")
        lines.append("")
    lines.append(
        "Read all three trees before concluding anything: a bucket naming the target\n"
        "in ANY tree means tagging exists (step 2). Appliances live in `hardware`.\n"
        "Bucket counts are occurrences at the deepest level unless --count-hosts.\n"
        "\n"
        "`host.services.protocol` is a FOURTH layer, not a tag tree. A named protocol\n"
        "here means Censys decoded it and stored a structured sub-document you can\n"
        "query - `any_connect.groups`, `ike.*` and so on - which beats any banner or\n"
        "body regex. Check it with `tsa doc host --grep <protocol>` before writing\n"
        "content patterns, and never treat a port aggregation as this check."
    )
    return "\n".join(lines)


def format_candidates(result: Dict[str, Any], base: str, top: int = 5) -> str:
    items = result["items"]
    base_item = items[0]
    rows: List[Dict[str, Any]] = []
    for item in items[1:]:
        candidate = item.get("label") or item["query"]
        row = next((r for r in rows if r["candidate"] == candidate), None)
        if row is None:
            row = {"candidate": candidate, "incremental": None, "witness": [], "errors": []}
            rows.append(row)
        if item["error"]:
            row["errors"].append(item["error"])
        elif item["op"] == "count":
            row["incremental"] = item["total"]
        elif item["op"] == "agg":
            row["witness"] = item["buckets"][:top]

    def sort_key(row: Dict[str, Any]):
        return -(row["incremental"] if isinstance(row["incremental"], int) else -1)

    lines = [
        f"base            : {base[:150]}",
        f"base population : {_count(base_item['total'])} hosts"
        + (f"   ! {base_item['error']}" if base_item["error"] else ""),
        f"calls           : {len(items)} · {result['wall_seconds']}s wall",
        "",
        "Incremental hosts each candidate adds, and what those hosts look like:",
        "",
    ]
    for row in sorted(rows, key=sort_key):
        gain = row["incremental"]
        marker = f"+{gain:,}" if isinstance(gain, int) else "ERR"
        lines.append(f"  {marker:>9}  {row['candidate'][:120]}")
        if row["witness"]:
            witness = " · ".join(
                f"{bucket['key']} {_count(bucket['count'])}" for bucket in row["witness"]
            )
            lines.append(f"             {witness[:150]}")
        elif isinstance(gain, int) and gain == 0:
            lines.append(
                "             nothing new - either the base already covers these hosts "
                "or the candidate matches nothing at all (--totals tells them apart)"
            )
        elif isinstance(gain, int) and gain > 0:
            #  An empty witness on a real increment is EVIDENCE, not silence: those
            #  hosts serve no HTML title at all, which is the signature of a
            #  non-HTTP service or a fronted deployment - and, for a bare port
            #  candidate, usually of a population that is not the product. Saying
            #  nothing here reads as "no problem found".
            lines.append(
                "             no titles on the incremental hosts - non-HTTP, fronted, "
                "or not the product. Read records before adding this one"
            )
        for error in row["errors"]:
            lines.append(f"             ! {error}")
    lines += [
        "",
        "Read the buckets, not just the counts. Keep a candidate only if its\n"
        "incremental population is coherently the target product; a generic token\n"
        "pulls in unrelated titles and must be discarded (step 8b).",
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------------- CLI


def load_plan(path: str) -> List[Dict[str, Any]]:
    """Read a plan from a JSON list, or from JSONL, or from stdin with `-`."""
    raw = sys.stdin.read() if path == "-" else Path(path).read_text()
    raw = raw.strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
        payload = parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        payload = [json.loads(line) for line in raw.splitlines() if line.strip()]
    return [
        make_item(
            entry.get("op", "count"),
            entry["query"],
            field=entry.get("field", ""),
            label=entry.get("label", ""),
            max_results=int(entry.get("max_results", 3)),
            buckets=int(entry.get("buckets", DEFAULT_BUCKETS)),
            count_by_level=(
                COUNT_LEVEL_HOST if entry.get("count_hosts") else entry.get("count_by_level")
            ),
            filter_by_query=bool(entry.get("filter_by_query", True)),
        )
        for entry in payload
    ]


def build_probe_items(args: argparse.Namespace) -> List[Dict[str, Any]]:
    fields = list(PROBE_TREES) + list(PROBE_PROTOCOL) + (
        list(PROBE_WIDE) if args.wide else []
    )
    sample_query = args.seed if args.raw_seed else host_scoped(args.seed)
    items = [
        make_item("sample", sample_query, max_results=args.max_results, label="seed sample")
    ]
    #  The aggregations bucket `host.*` fields, so they are host-scoped by the
    #  field itself and take the seed unchanged.
    items += [
        make_item(
            "agg", args.seed, field=field, buckets=args.buckets,
            count_by_level=args.count_by_level,
        )
        for field in fields
    ]
    return items


def build_candidate_items(args: argparse.Namespace) -> List[Dict[str, Any]]:
    base = parenthesize(args.base)
    items = [make_item("count", base, label="base")]
    for candidate in args.candidates:
        incremental = f"{parenthesize(candidate)} and not {base}"
        items.append(make_item("count", incremental, label=candidate))
        if args.witness:
            items.append(
                make_item(
                    "agg",
                    incremental,
                    field=args.witness_field,
                    label=candidate,
                    buckets=args.buckets,
                    # Host counts, always: "how many HOSTS carry this title" is
                    # the question, and occurrence counts would inflate it.
                    count_by_level=COUNT_LEVEL_HOST,
                )
            )
        if args.totals:
            items.append(make_item("count", parenthesize(candidate), label=f"{candidate} (total)"))
    return items


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-k", "--top", type=int, default=10, help="Buckets shown per field")
    parser.add_argument(
        "-b", "--buckets", type=int, default=DEFAULT_BUCKETS,
        help=f"Buckets requested per aggregation (max {MAX_BUCKETS})",
    )
    parser.add_argument("-f", "--format", choices=("table", "json"), default="table")
    parser.add_argument("-o", "--output", help="Write the full JSON result here")
    parser.add_argument("--org-id", default=CENSYS_ORG_ID, help="Censys organization ID")
    parser.add_argument(
        "--concurrency", type=int, default=DEFAULT_CONCURRENCY,
        help="Requests in flight. Capped in practice by the rate-limit profile",
    )
    parser.add_argument(
        "--timeout-ms", type=int, default=DEFAULT_TIMEOUT_MS,
        help="Per-request HTTP timeout; lower it when probing heavy queries",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Log progress")

    limits = parser.add_argument_group("rate limiting")
    limits.add_argument("--min-interval", type=float, default=DEFAULT_MIN_INTERVAL)
    limits.add_argument("--max-per-minute", type=int, default=DEFAULT_MAX_PER_MINUTE)
    limits.add_argument("--budget-requests", type=int, default=DEFAULT_BUDGET_REQUESTS)
    limits.add_argument("--budget-window", type=float, default=DEFAULT_BUDGET_WINDOW)
    limits.add_argument("--state-file", default=str(DEFAULT_STATE_FILE))
    limits.add_argument(
        "--no-wait", action="store_true",
        help="Fail instead of sleeping when a rate limit is hit",
    )


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa probe"), not this file, which is not on their PATH.
    # It already contains the mode word, and argparse appends the subparser name
    # too, so trim it back to "tsa" or the usage reads "tsa probe probe".
    exported = os.environ.get("CENSYS_TSA_PROG") or ""
    prog = exported.rsplit(" ", 1)[0] if " " in exported else (exported or None)
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Run many independent Censys calls in one turn.",
    )
    sub = parser.add_subparsers(dest="mode", required=True)

    batch = sub.add_parser("batch", help="An arbitrary set of counts, samples and aggregations")
    batch.add_argument(
        "--count", action="append", default=[], metavar="QUERY",
        help="Total host count for a query. Repeatable",
    )
    batch.add_argument(
        "--sample", action="append", default=[], metavar="QUERY",
        help="Total plus a few example hosts. Repeatable",
    )
    batch.add_argument(
        "--agg", action="append", default=[], nargs=2, metavar=("FIELD", "QUERY"),
        help="Bucket FIELD over QUERY. Repeatable",
    )
    batch.add_argument("-p", "--plan", help="JSON or JSONL plan file, or - for stdin")
    batch.add_argument(
        "--max-results", type=int, default=3, help="Example hosts per --sample"
    )
    batch.add_argument(
        "--count-hosts", dest="count_by_level", action="store_const",
        const=COUNT_LEVEL_HOST, default=None,
        help="Aggregation buckets count hosts, not nested occurrences",
    )
    batch.add_argument(
        "--no-filter-by-query", action="store_true",
        help="Count all values on matching hosts, not only query-matching ones",
    )
    add_common_arguments(batch)

    probe = sub.add_parser(
        "probe", help="Step 1 in one call: seed sample + all three tag trees"
    )
    probe.add_argument("seed", help="Full-text seed, e.g. '\"MOVEit Transfer\"'")
    probe.add_argument(
        "--wide", action="store_true",
        help="Also bucket vendors, ports, titles and favicon hashes (5 more calls)",
    )
    probe.add_argument("--max-results", type=int, default=3, help="Example hosts to show")
    probe.add_argument(
        "--raw-seed", action="store_true",
        help=f"Sample the seed exactly as given, without appending "
             f"`and {HOST_SCOPE_CLAUSE}`. A bare full-text seed is not "
             f"host-scoped and will also match web properties and certificates",
    )
    probe.add_argument(
        "--count-hosts", dest="count_by_level", action="store_const",
        const=COUNT_LEVEL_HOST, default=None,
        help="Bucket counts are host counts rather than nested occurrences",
    )
    add_common_arguments(probe)

    candidates = sub.add_parser(
        "candidates", help="Step 8b in one call: incremental hosts per candidate signal"
    )
    candidates.add_argument("base", help="The validated base query")
    candidates.add_argument("candidates", nargs="+", help="Candidate signals to test")
    candidates.add_argument(
        "--witness-field", default=DEFAULT_WITNESS_FIELD,
        help="Field bucketed over each incremental population",
    )
    candidates.add_argument(
        "--no-titles", dest="witness", action="store_false", default=True,
        help="Skip the witness aggregation (halves the cost, and the evidence)",
    )
    candidates.add_argument(
        "--totals", action="store_true",
        help="Also count each candidate on its own, not only its increment",
    )
    add_common_arguments(candidates)

    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if args.mode == "batch":
        items: List[Dict[str, Any]] = []
        if args.plan:
            items += load_plan(args.plan)
        items += [
            make_item("count", query, label="count") for query in args.count
        ]
        items += [
            make_item("sample", query, max_results=args.max_results, label="sample")
            for query in args.sample
        ]
        items += [
            make_item(
                "agg", query, field=field, buckets=args.buckets,
                count_by_level=args.count_by_level,
                filter_by_query=not args.no_filter_by_query,
            )
            for field, query in args.agg
        ]
        if not items:
            print(
                "error: nothing to do - pass --count/--sample/--agg or --plan",
                file=sys.stderr,
            )
            return 64
    elif args.mode == "probe":
        items = build_probe_items(args)
    else:
        items = build_candidate_items(args)

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
        result = run_batch(
            items,
            gateway,
            org_id=args.org_id,
            concurrency=args.concurrency,
            timeout_ms=args.timeout_ms,
            verbose=args.verbose,
        )
    except RateLimitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    result["mode"] = args.mode
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))

    if args.format == "json":
        print(json.dumps(result, indent=2))
    elif args.mode == "probe":
        print(format_probe(result, args.seed, top=args.top))
    elif args.mode == "candidates":
        print(format_candidates(result, args.base, top=args.top))
    else:
        print(format_batch(result, top=args.top))

    if result["items"] and all(item["error"] for item in result["items"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
