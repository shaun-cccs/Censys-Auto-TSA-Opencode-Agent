#!/usr/bin/env python3
"""Render a Threat Surface Assessment investigation as a markdown report.

The skill's step 7 report and step 8 deep dive have a fixed shape: product
summary, fingerprint rationale, baseline query and counts, an optional widened
query with a delta table, the signals kept and rejected, credit consumption,
and caveats. This module turns that shape into a reusable renderer so every
investigation is written up identically.

A report is described by a JSON spec (see ``--template`` for a skeleton). Only
``product`` and ``baseline`` are required; every other section is omitted from
the output when absent, so a tag-based TSA with no deep dive renders cleanly.

Examples
--------
    python utils/tsa_report.py --template > /tmp/spec.json
    python utils/tsa_report.py /tmp/spec.json -o reports/centreon-mbi.md
    python utils/tsa_report.py /tmp/spec.json          # markdown to stdout

The renderer never calls Censys, so it costs no credits and no rate budget.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import quote

PLATFORM_SEARCH_URL = "https://platform.censys.io/search"

# Matches the default organization used by the other utils; overridable per spec.
DEFAULT_ORG_ID = "7c96b9ef-3e11-4577-ab6f-1067e5211d4f"

HONEYPOT_CLAUSE = 'not labels: "HONEYPOT"'


class ReportError(ValueError):
    """Raised when a spec cannot be rendered."""


def platform_url(query: str, org_id: Optional[str] = DEFAULT_ORG_ID) -> str:
    """Build a platform.censys.io search URL for a CenQL query."""
    url = f"{PLATFORM_SEARCH_URL}?q={quote(query, safe='')}"
    if org_id:
        url += f"&org={org_id}"
    return url


def scoped_query(base: str, country: Optional[str] = None) -> str:
    """Append the honeypot exclusion, and optionally a country, to a query."""
    query = f"{base} and {HONEYPOT_CLAUSE}"
    if country:
        query += f' and host.location.country="{country}"'
    return query


def _fmt_count(value: Any) -> str:
    return f"{value:,}" if isinstance(value, int) else str(value)


def _fmt_delta(new: Any, old: Any) -> str:
    if isinstance(new, int) and isinstance(old, int):
        diff = new - old
        return f"+{diff:,}" if diff > 0 else f"{diff:,}"
    return "-"


def _bullets(items: Optional[Iterable[Any]]) -> List[str]:
    """Render a list of strings, or of {name, evidence} mappings, as bullets."""
    lines: List[str] = []
    for item in items or []:
        if isinstance(item, dict):
            name = item.get("name", "")
            detail = item.get("evidence") or item.get("reason") or ""
            lines.append(f"- **{name}** — {detail}" if detail else f"- **{name}**")
        else:
            lines.append(f"- {item}")
    return lines


def _code_block(text: str) -> List[str]:
    return ["```", text.strip(), "```"]


def _query_section(title: str, query: str, org_id: Optional[str]) -> List[str]:
    return [
        f"### {title}",
        "",
        *_code_block(query),
        "",
        f"[Open in Censys]({platform_url(query, org_id)})",
        "",
    ]


def _count_query_sections(
    base: str, country: str, org_id: Optional[str]
) -> List[str]:
    """Render the two queries the counts were actually taken from.

    The base query is never counted directly - ``utils/censys_tsa.py`` appends
    the honeypot exclusion for the global count and the country filter on top of
    that for the national count. Both are spelled out here so the report is
    reproducible without rerunning the tool.
    """
    return [
        *_query_section(
            "Global count query (honeypots excluded)", scoped_query(base), org_id
        ),
        *_query_section(
            f"{country} count query (honeypots excluded)",
            scoped_query(base, country),
            org_id,
        ),
    ]


def _counts_table(
    counts: Dict[str, Any],
    country: str,
    baseline: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Render global/country counts, as a delta table when a baseline is given."""
    if baseline:
        rows = [
            "| Scope | Baseline | Widened | Delta |",
            "| --- | --- | --- | --- |",
        ]
        for scope, key in (("Global", "global"), (country, "country")):
            old, new = baseline.get(key), counts.get(key)
            rows.append(
                f"| {scope} | {_fmt_count(old)} | **{_fmt_count(new)}** "
                f"| {_fmt_delta(new, old)} |"
            )
        return rows

    return [
        "| Scope | Hosts (honeypots excluded) |",
        "| --- | --- |",
        f"| **Global** | **{_fmt_count(counts.get('global'))}** |",
        f"| **{country}** | **{_fmt_count(counts.get('country'))}** |",
    ]


def _credits_table(credits: Dict[str, Any]) -> List[str]:
    runs = credits.get("runs") or []
    lines = ["| Run | Credits | Balance |", "| --- | --- | --- |"]
    total = credits.get("total")
    for run in runs:
        before, after = run.get("balance_before"), run.get("balance_after")
        balance = (
            f"{_fmt_count(before)} → {_fmt_count(after)}"
            if before is not None and after is not None
            else "—"
        )
        lines.append(f"| {run.get('label', '?')} | {_fmt_count(run.get('used'))} | {balance} |")
    if total is None:
        total = sum(r.get("used", 0) for r in runs if isinstance(r.get("used"), int))
    lines.append(f"| **Session total** | **{_fmt_count(total)}** | — |")
    return lines


class _Counter:
    """Hands out sequential section numbers so omitted sections leave no gaps."""

    def __init__(self) -> None:
        self.n = 0

    def __call__(self) -> int:
        self.n += 1
        return self.n


def render_report(spec: Dict[str, Any]) -> str:
    """Render a TSA spec as a markdown document."""
    product = spec.get("product")
    baseline = spec.get("baseline")
    if not product or not baseline:
        raise ReportError("spec requires at least 'product' and 'baseline'")
    if "query" not in baseline or "counts" not in baseline:
        raise ReportError("'baseline' requires 'query' and 'counts'")

    org_id = spec.get("org_id", DEFAULT_ORG_ID)
    country = spec.get("country", "Canada")
    out: List[str] = [f"# Threat Surface Assessment — {product}", ""]
    section = _Counter()

    meta = [f"**Assessed:** {spec.get('date', date.today().isoformat())}"]
    if spec.get("vendor"):
        meta.append(f"**Vendor:** {spec['vendor']}")
    if spec.get("cve"):
        meta.append(f"**CVE:** {spec['cve']}")
    if spec.get("basis"):
        meta.append(f"**Counting basis:** {spec['basis']}")
    out += [" · ".join(meta), ""]

    if spec.get("summary"):
        out += [f"## {section()}. Product", "", spec["summary"].strip(), ""]

    rationale = spec.get("rationale") or {}
    if rationale:
        heading = rationale.get("heading", "Fingerprint rationale")
        out += [f"## {section()}. {heading}", ""]
        if rationale.get("intro"):
            out += [rationale["intro"].strip(), ""]
        out += _bullets(rationale.get("findings"))
        out += [""]

    out += [f"## {section()}. Baseline assessment", ""]
    out += _query_section("Base query", baseline["query"], org_id)
    out += _counts_table(baseline["counts"], country)
    out += [""]
    if baseline.get("notes"):
        out += [baseline["notes"].strip(), ""]
    out += _count_query_sections(baseline["query"], country, org_id)

    deep = spec.get("deep_dive")
    if deep:
        out += [f"## {section()}. Deep dive — widened query", ""]
        if deep.get("intro"):
            out += [deep["intro"].strip(), ""]
        out += _query_section("Widened base query", deep["query"], org_id)
        out += _counts_table(deep["counts"], country, baseline=baseline["counts"])
        out += [""]
        out += _count_query_sections(deep["query"], country, org_id)
        if deep.get("signals_added"):
            out += ["### Signals added", "", *_bullets(deep["signals_added"]), ""]
        if deep.get("signals_rejected"):
            out += ["### Candidates tested and rejected", "", *_bullets(deep["signals_rejected"]), ""]

    for extra in spec.get("extra_assessments") or []:
        out += [f"## {section()}. {extra.get('heading', 'Additional assessment')}", ""]
        if extra.get("intro"):
            out += [extra["intro"].strip(), ""]
        if extra.get("distribution"):
            cols = extra.get("distribution_columns") or ["Value", "Hosts"]
            out += ["| " + " | ".join(cols) + " |",
                    "| " + " | ".join("---" for _ in cols) + " |"]
            for row in extra["distribution"]:
                out += ["| " + " | ".join(str(c) for c in row) + " |"]
            out += [""]
        if extra.get("query"):
            out += _query_section(extra.get("query_label", "Query"), extra["query"], org_id)
            if extra.get("counts"):
                out += _counts_table(extra["counts"], country)
                out += [""]
            out += _count_query_sections(extra["query"], country, org_id)
        if extra.get("notes"):
            out += [extra["notes"].strip(), ""]

    credits = spec.get("credits")
    if credits:
        out += [f"## {section()}. Censys credit consumption", "", *_credits_table(credits), ""]
        if credits.get("notes"):
            out += [credits["notes"].strip(), ""]

    if spec.get("caveats"):
        out += [f"## {section()}. Caveats", "", *_bullets(spec["caveats"]), ""]

    if spec.get("sources"):
        out += [f"## {section()}. Sources", "", *_bullets(spec["sources"]), ""]

    return "\n".join(out).rstrip() + "\n"


TEMPLATE: Dict[str, Any] = {
    "product": "Vendor Product",
    "vendor": "Vendor",
    "cve": None,
    "basis": "product exposure (patch status unknown)",
    "country": "Canada",
    "summary": "What the product is and what it exposes.",
    "rationale": {
        "heading": "Fingerprint rationale — evidence-based (step 3)",
        "intro": "How the query was derived.",
        "findings": [
            {"name": "No Censys tagging", "evidence": "what the aggregation showed"},
            {"name": "Positive control", "evidence": "regex validated against a known population"},
        ],
    },
    "baseline": {
        "query": '(host.services.endpoints.http.html_title="Example")',
        "counts": {"global": 0, "country": 0},
        "notes": None,
    },
    "deep_dive": {
        "intro": None,
        "query": '(host.services.endpoints.http.html_title="Example" or ...)',
        "counts": {"global": 0, "country": 0},
        "signals_added": [{"name": "signal", "evidence": "+N incremental hosts, why it is sound"}],
        "signals_rejected": [{"name": "candidate", "reason": "why it was discarded"}],
    },
    "credits": {
        "runs": [
            {"label": "Baseline TSA", "used": 2, "balance_before": 0, "balance_after": 0},
        ],
        "total": None,
        "notes": "Aggregations and `cve_lookup.py` calls cost no credits.",
    },
    "caveats": ["What the number does and does not mean."],
    "sources": [],
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render a TSA investigation spec as a markdown report."
    )
    parser.add_argument("spec", nargs="?", help="path to a JSON spec, or '-' for stdin")
    parser.add_argument("-o", "--output", help="write markdown here instead of stdout")
    parser.add_argument(
        "--template",
        action="store_true",
        help="print a blank JSON spec skeleton and exit",
    )
    args = parser.parse_args(argv)

    if args.template:
        print(json.dumps(TEMPLATE, indent=2))
        return 0

    if not args.spec:
        parser.error("a spec path is required unless --template is given")

    raw = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text()
    try:
        markdown = render_report(json.loads(raw))
    except json.JSONDecodeError as e:
        print(f"error: spec is not valid JSON: {e}", file=sys.stderr)
        return 2
    except ReportError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown)
        print(f"wrote {path} ({len(markdown.splitlines())} lines)", file=sys.stderr)
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
