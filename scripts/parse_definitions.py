"""Parse the Censys Data Definitions HTML export into a markdown reference.

Run with no arguments to regenerate every reference from
``docs/data_definition_raw_html`` into ``docs/queryable_fields``::

    python utils/parse_definitions.py
"""

import html
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = REPO_ROOT / "docs" / "data_definition_raw_html"
OUTPUT_DIR = REPO_ROOT / "docs" / "queryable_fields"

TAG_RE = re.compile(r"<[^>]+>")
ROW_RE = re.compile(r'<tr id="([^"]+)">(.*?)</tr>', re.S)
CELL_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.S)


def text(fragment: str) -> str:
    return html.unescape(TAG_RE.sub("", fragment)).strip()


def parse(path: str):
    raw = open(path, encoding="utf-8").read()
    datasets = OrderedDict()
    for row_id, body in ROW_RE.findall(raw):
        cells = [text(c) for c in CELL_RE.findall(body)]
        if len(cells) < 4:
            continue
        _, name, ftype, desc = cells[0], cells[1], cells[2], cells[3]
        if not name:
            continue
        dataset = row_id.split("-", 1)[0]
        fields = datasets.setdefault(dataset, OrderedDict())
        if name not in fields:
            fields[name] = (ftype, desc)
    return datasets


def to_markdown(datasets, src: str) -> str:
    total = sum(len(f) for f in datasets.values())
    lines = [
        "# Censys Platform Queryable Fields",
        "",
        f"Parsed from `{src}` (in-app data definitions, "
        "<https://platform.censys.io/home/definitions>).",
        "",
        f"**Total fields: {total}**",
        "",
        "| Dataset | Field count |",
        "| --- | --- |",
    ]
    for ds, fields in datasets.items():
        lines.append(f"| `{ds}` | {len(fields)} |")
    lines.append("")
    for ds, fields in datasets.items():
        lines += [
            f"## {ds} ({len(fields)} fields)",
            "",
            "| Field | Type | Description |",
            "| --- | --- | --- |",
        ]
        for name, (ftype, desc) in fields.items():
            desc = desc.replace("|", "\\|")
            lines.append(f"| `{name}` | {ftype} | {desc} |")
        lines.append("")
    return "\n".join(lines)


def out_name(src: str) -> str:
    stem = Path(src).stem.lower()
    stem = re.sub(r"\s*censys data definitions\s*", "", stem).strip()
    prefix = re.sub(r"[^a-z0-9]+", "_", stem).strip("_") or "host"
    return f"{prefix}_censys_queryable_fields.md"


if __name__ == "__main__":
    sources = sys.argv[1:] or sorted(str(p) for p in HTML_DIR.glob("*.html"))
    if not sources:
        sys.exit(f"no HTML sources found in {HTML_DIR}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for src in sources:
        data = parse(src)
        out = OUTPUT_DIR / out_name(src)
        for ds, fields in data.items():
            print(f"{Path(src).name} -> {ds}: {len(fields)} fields")
        out.write_text(to_markdown(data, Path(src).name), encoding="utf-8")
        print(f"wrote {out.relative_to(REPO_ROOT)}")
