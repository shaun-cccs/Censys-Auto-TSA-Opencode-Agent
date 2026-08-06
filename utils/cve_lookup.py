#!/usr/bin/env python3
"""Retrieve a CVE record and hand it back as context.

Primary source is the CVE Program record shown at
``https://www.cve.org/CVERecord?id=<CVE-ID>``. That page is a JavaScript
application, so the record is fetched from the JSON API that backs it
(``https://cveawg.mitre.org/api/cve/<CVE-ID>``) and the human-readable
``cve.org`` URL is reported alongside it.

If cve.org fails, or returns a record with no usable content (many CNA records
are stubs - ``vendor: n/a``, ``product: n/a``, no versions), the lookup falls
back to NVD (``https://nvd.nist.gov/vuln/detail/<CVE-ID>``, fetched via the NVD
2.0 REST API), which usually carries CPE applicability data and CVSS scoring.
Both sources are fetched by default, since neither costs anything and they
complement each other.

Deliberately **not** a parser. Affected products and version ranges are quoted
as the source published them rather than normalized, because CNA and NVD data
shapes vary too much for parsing to be reliable. Read the output and decide
what the fingerprint should be.

Examples
--------
    python utils/cve_lookup.py CVE-2023-34362
    python utils/cve_lookup.py CVE-2024-21762 --single
    python utils/cve_lookup.py CVE-2023-34362 --format json -o cve.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

CVE_ID_RE = re.compile(r"^CVE-\d{4}-\d{4,}$", re.IGNORECASE)

# Human-facing pages, reported in output so findings can be cited.
CVE_ORG_URL = "https://www.cve.org/CVERecord?id={cve_id}"
NVD_URL = "https://nvd.nist.gov/vuln/detail/{cve_id}"

# JSON APIs backing those pages.
CVE_ORG_API = "https://cveawg.mitre.org/api/cve/{cve_id}"
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"

DEFAULT_TIMEOUT = 30.0
USER_AGENT = "censys-auto-tsa/1.0 (+cve-lookup)"

SOURCES = ("cve.org", "nvd")


class CVELookupError(RuntimeError):
    """Raised when no source can supply a record for a CVE."""


def normalize_cve_id(value: str) -> str:
    """Validate and upper-case a CVE identifier."""
    cve_id = str(value).strip().upper()
    if not CVE_ID_RE.match(cve_id):
        raise ValueError(f"not a valid CVE ID: {value!r} (expected CVE-YYYY-NNNN)")
    return cve_id


def _fetch_json(
    url: str, timeout: float = DEFAULT_TIMEOUT, max_retries: int = 3
) -> Dict[str, Any]:
    """GET a JSON document, retrying transient failures with backoff."""
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    last: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # 404 means the source genuinely lacks the record; do not retry.
            if e.code == 404:
                raise CVELookupError(f"not found (HTTP 404): {url}") from e
            last = e
        except Exception as e:  # noqa: BLE001 - network/parse
            last = e
        if attempt < max_retries - 1:
            time.sleep(1.0 * (2**attempt))
    raise CVELookupError(f"{type(last).__name__}: {str(last)[:200]} ({url})")


def _english(entries: Any) -> Optional[str]:
    """First English description in a CVE/NVD ``descriptions[]`` list."""
    for entry in entries or []:
        if entry.get("value") and str(entry.get("lang", "en")).lower().startswith("en"):
            return entry["value"]
    return None


# -- sources -----------------------------------------------------------------


def fetch_from_cve_org(cve_id: str, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """Fetch the CVE Program record. Returns metadata plus the raw record."""
    raw = _fetch_json(CVE_ORG_API.format(cve_id=cve_id), timeout=timeout)
    cna = (raw.get("containers") or {}).get("cna") or {}
    metadata = raw.get("cveMetadata") or {}

    return {
        "source": "cve.org",
        "source_url": CVE_ORG_URL.format(cve_id=cve_id),
        "api_url": CVE_ORG_API.format(cve_id=cve_id),
        "cve_id": metadata.get("cveId", cve_id),
        "state": metadata.get("state"),
        "published": metadata.get("datePublished"),
        "modified": metadata.get("dateUpdated"),
        "assigner": metadata.get("assignerShortName"),
        "description": _english(cna.get("descriptions")),
        "cvss": extract_cvss(raw),
        "kev": False,
        "raw": raw,
    }


def fetch_from_nvd(cve_id: str, timeout: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """Fetch the NVD record. Returns metadata plus the raw record."""
    raw = _fetch_json(NVD_API.format(cve_id=cve_id), timeout=timeout)
    entries = raw.get("vulnerabilities") or []
    if not entries:
        raise CVELookupError(f"NVD returned no record for {cve_id}")
    cve = entries[0].get("cve") or {}

    return {
        "source": "nvd",
        "source_url": NVD_URL.format(cve_id=cve_id),
        "api_url": NVD_API.format(cve_id=cve_id),
        "cve_id": cve.get("id", cve_id),
        "state": cve.get("vulnStatus"),
        "published": cve.get("published"),
        "modified": cve.get("lastModified"),
        "assigner": cve.get("sourceIdentifier"),
        "description": _english(cve.get("descriptions")),
        "cvss": extract_cvss(cve),
        "kev": bool(cve.get("cisaExploitAdd")),
        "kev_added": cve.get("cisaExploitAdd"),
        "raw": cve,
    }


FETCHERS = {"cve.org": fetch_from_cve_org, "nvd": fetch_from_nvd}


# -- shallow enrichment ------------------------------------------------------
#
# Only single scalar fields are extracted, for the TSA report header. Anything
# structural (affected products, version ranges) is left to the reader.


def extract_cvss(record: Any) -> Dict[str, Any]:
    """Find the highest-version CVSS base metric anywhere in a record.

    Walks the whole document rather than assuming a path, so it works on both
    the CVE 5.x containers layout and the NVD metrics layout.
    """
    best: Dict[str, Any] = {}
    best_rank = -1
    ranks = {"4.0": 4, "3.1": 3, "3.0": 2, "2.0": 1}

    def visit(node: Any) -> None:
        nonlocal best, best_rank
        if isinstance(node, list):
            for item in node:
                visit(item)
            return
        if not isinstance(node, dict):
            return
        vector = node.get("vectorString")
        score = node.get("baseScore")
        if isinstance(vector, str) and score is not None:
            version = str(node.get("version") or "")
            if not version:
                match = re.match(r"CVSS:(\d+\.\d+)", vector)
                version = match.group(1) if match else "3.1"
            rank = ranks.get(version, 0)
            if rank > best_rank:
                best_rank = rank
                best = {
                    "version": version,
                    "score": score,
                    "severity": node.get("baseSeverity"),
                    "vector": vector,
                }
        for value in node.values():
            visit(value)

    visit(record)
    return best


def _is_stub(record: Dict[str, Any]) -> bool:
    """True when a record carries no usable content worth reading.

    A stub is a record with no description and no CVSS - the case where the
    other source is worth trying. This is intentionally a crude check on two
    scalar fields, not an assessment of the affected-product data.
    """
    return not record.get("description") and not record.get("cvss")


def lookup_cve(
    cve_id: str,
    prefer: str = "cve.org",
    both: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Retrieve a CVE record, falling back across sources.

    cve.org is the primary source and NVD the fallback. Both are fetched by
    default: they are free, and a cve.org record can carry a good description
    while naming no affected product at all (``vendor: n/a``), in which case
    NVD's CPE applicability data and CISA KEV status are what make the record
    usable. Pass ``both=False`` to stop at the first source that returns
    anything.
    """
    cve_id = normalize_cve_id(cve_id)
    order = list(SOURCES) if prefer == "cve.org" else list(reversed(SOURCES))

    attempts: List[Dict[str, Any]] = []
    records: Dict[str, Dict[str, Any]] = {}

    for name in order:
        try:
            records[name] = FETCHERS[name](cve_id, timeout=timeout)
            attempts.append({"source": name, "ok": True})
            if verbose:
                print(f"[cve] {name}: ok", file=sys.stderr)
        except (CVELookupError, ValueError) as e:
            attempts.append({"source": name, "ok": False, "error": str(e)})
            if verbose:
                print(f"[cve] {name}: {e}", file=sys.stderr)
            continue
        if not both and not _is_stub(records[name]):
            break
        if verbose and _is_stub(records[name]):
            print(f"[cve] {name}: record is a stub, trying next source", file=sys.stderr)

    if not records:
        raise CVELookupError(
            f"no source could supply {cve_id}: "
            + "; ".join(f"{a['source']}={a.get('error')}" for a in attempts)
        )

    primary_name = next(
        (n for n in order if n in records and not _is_stub(records[n])),
        next(n for n in order if n in records),
    )
    result = dict(records[primary_name])

    other_name = next((n for n in order if n != primary_name and n in records), None)
    if other_name:
        other = records[other_name]
        result["secondary"] = other
        result["secondary_source"] = other_name
        result["secondary_source_url"] = other.get("source_url")
        for field in ("description", "cvss", "published", "modified", "state"):
            if not result.get(field) and other.get(field):
                result[field] = other[field]
        if not result.get("kev") and other.get("kev"):
            result["kev"] = True
            result["kev_added"] = other.get("kev_added")

    result["sources_tried"] = attempts
    result["urls"] = {
        "cve.org": CVE_ORG_URL.format(cve_id=cve_id),
        "nvd": NVD_URL.format(cve_id=cve_id),
    }
    result["vuln_tag_query"] = f'host.services.vulns.id="{cve_id}"'
    return result


# -- rendering ---------------------------------------------------------------


def _record_context(record: Dict[str, Any], indent: str = "  ") -> List[str]:
    """Render one source's raw record as pretty JSON context lines."""
    text = json.dumps(record.get("raw") or {}, indent=2, sort_keys=False)
    return [f"{indent}{line}" for line in text.splitlines()]


def format_report(result: Dict[str, Any], max_context: int = 400) -> str:
    """Render the lookup as readable context.

    The header carries the few scalars worth quoting directly; everything below
    it is the record as published, for the reader to interpret.
    """
    cvss = result.get("cvss") or {}
    lines = [
        f"CVE            : {result['cve_id']}",
        f"Source         : {result['source']} - {result['source_url']}",
    ]
    if result.get("secondary_source"):
        lines.append(
            f"Also retrieved : {result['secondary_source']} - "
            f"{result.get('secondary_source_url')}"
        )
    lines += [
        f"State          : {result.get('state') or 'unknown'}",
        f"Published      : {str(result.get('published') or 'unknown')[:10]}",
    ]
    if cvss:
        lines.append(
            f"CVSS           : {cvss.get('score')} {cvss.get('severity') or ''} "
            f"(v{cvss.get('version')}) {cvss.get('vector') or ''}".rstrip()
        )
    if result.get("kev"):
        lines.append(
            f"CISA KEV       : yes (added {str(result.get('kev_added'))[:10]})"
        )
    lines.append(f"Censys tag     : {result['vuln_tag_query']}")

    if result.get("description"):
        lines += ["", "Description", f"  {result['description']}"]

    lines += ["", f"Record - {result['source']} ({result['api_url']})"]
    context = _record_context(result)
    lines += context[:max_context]
    if len(context) > max_context:
        lines.append(f"  ... {len(context) - max_context} more lines (use -f json)")

    secondary = result.get("secondary")
    if secondary:
        lines += ["", f"Record - {secondary['source']} ({secondary['api_url']})"]
        context = _record_context(secondary)
        lines += context[:max_context]
        if len(context) > max_context:
            lines.append(f"  ... {len(context) - max_context} more lines (use -f json)")

    failed = [a for a in result.get("sources_tried") or [] if not a.get("ok")]
    if failed:
        lines += ["", "Source failures"]
        lines += [f"  ! {a['source']}: {a.get('error')}" for a in failed]

    lines += [
        "",
        "Read the affected-product and version data above yourself - it is not",
        "parsed, and vendor/product strings rarely match Censys software tags",
        "verbatim. Confirm the tag in Censys before counting.",
    ]
    return "\n".join(lines)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve a CVE record from cve.org, falling back to NVD, and "
            "print it as context for building a Censys fingerprint."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("cve_id", help="CVE identifier, e.g. CVE-2023-34362")
    parser.add_argument(
        "--single",
        dest="both",
        action="store_false",
        help="Stop at the first source that returns a record instead of fetching both",
    )
    parser.add_argument(
        "--prefer",
        choices=SOURCES,
        default="cve.org",
        help="Which source to consult first",
    )
    parser.add_argument(
        "--max-context",
        type=int,
        default=400,
        help="Max record lines to print per source in report format",
    )
    parser.add_argument(
        "--timeout", type=float, default=DEFAULT_TIMEOUT, help="Per-request timeout"
    )
    parser.add_argument(
        "-f", "--format", choices=("report", "json"), default="report",
        help="Output rendering for stdout",
    )
    parser.add_argument("-o", "--output", help="Write full JSON results to this file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Log progress")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    try:
        result = lookup_cve(
            args.cve_id,
            prefer=args.prefer,
            both=args.both,
            timeout=args.timeout,
            verbose=args.verbose,
        )
    except (CVELookupError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))
        if args.verbose:
            print(f"[cve] wrote {args.output}", file=sys.stderr)

    print(
        json.dumps(result, indent=2)
        if args.format == "json"
        else format_report(result, max_context=args.max_context)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
