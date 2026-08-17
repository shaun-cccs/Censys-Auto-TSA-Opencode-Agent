#!/usr/bin/env python3
"""Wall-clock accounting for Censys calls. Reached as `tsa timeline`.

WHY THIS EXISTS
---------------
A TSA that takes an hour invites the wrong diagnosis. Measured on this kit, a
single Censys API action - including process start, uv dispatch and the round
trip - costs well under a second, while a full assessment issues on the order of
a hundred of them. The hour is therefore not spent in Censys or in Python; it is
spent between calls, in agent turns.

This module records every Censys request as it happens, and `tsa timeline`
reports the one number that settles the argument:

    idle gap = run span - time actually spent inside Censys calls

A large idle gap means the workflow is turn-bound, and the fix is fewer, wider
turns (`tsa batch`, `tsa probe`, `tsa candidates`, parallel subagents) rather
than faster queries. A small idle gap would mean the opposite. Optimising
without this number is guesswork.

STANDARD LIBRARY ONLY, ON PURPOSE
---------------------------------
``censys_query`` and ``censys_aggregate`` import this module, so it must not
import them back, must not import the Censys SDK, and must never raise: metrics
are a bystander to the query, and a broken recorder must never break a run.
`tsa timeline` therefore also runs without uv or the SDK installed.

    tsa timeline
    tsa timeline --since 600
    tsa timeline --all --format json
    tsa timeline --reset
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

#  Outside any workspace, like the rate and credit ledgers, because a run is
#  started from wherever the user happens to be working and the history should
#  survive that. Agents reach it only through `tsa timeline`, never by path.
METRICS_FILE = Path(
    os.environ.get(
        "CENSYS_TSA_METRICS_FILE",
        Path.home() / ".censys_tsa_metrics.jsonl",
    )
)

#  Recording is opt-out rather than opt-in: a timing history nobody switched on
#  is a timing history nobody has when the run turns out to be slow.
ENABLED = os.environ.get("CENSYS_TSA_METRICS", "1").strip().lower() not in {
    "0",
    "off",
    "false",
    "no",
}

#  Keep the file small enough to parse instantly. One line is ~150 bytes, so
#  this is roughly the last two thousand calls - far more than any single run.
MAX_BYTES = 2_000_000
KEEP_LINES = 2_000

#  A gap longer than this is treated as the boundary between two runs, so
#  `tsa timeline` can report "this run" without being told when it started.
RUN_GAP_SECONDS = 300.0


def record(
    op: str,
    wall_ms: float,
    ok: bool = True,
    query: str = "",
    field: str = "",
    detail: str = "",
) -> None:
    """Append one call record. Never raises, never blocks a query.

    ``wall_ms`` is the time inside the SDK call alone - not the rate-limit
    sleep that preceded it, which is accounted for by the run span instead.
    Conflating the two would hide exactly the stall this tool exists to find.
    """
    if not ENABLED:
        return
    line = json.dumps(
        {
            "ts": round(time.time(), 3),
            "op": op,
            "ms": round(float(wall_ms), 1),
            "ok": bool(ok),
            "q": (query or "")[:120],
            "field": field or None,
            "detail": (detail or "")[:80] or None,
        },
        separators=(",", ":"),
    )
    try:
        _prune_if_large()
        #  O_APPEND with a single short write is atomic on POSIX, so concurrent
        #  subagents interleave lines rather than corrupting them. No lock.
        with open(METRICS_FILE, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def _prune_if_large() -> None:
    try:
        if METRICS_FILE.stat().st_size <= MAX_BYTES:
            return
        kept = METRICS_FILE.read_text(encoding="utf-8").splitlines()[-KEEP_LINES:]
        METRICS_FILE.write_text("\n".join(kept) + "\n", encoding="utf-8")
    except (OSError, ValueError):
        pass


class timed:
    """Context manager that records one call, however it ends.

    Usage::

        with timed("search", query=q) as t:
            res = sdk.global_data.search(...)
        # t.failed("timeout") to mark it unsuccessful

    The point of a context manager rather than a decorator is that the callers
    are retry loops: each *attempt* is a real HTTP request that consumed real
    time and a real credit, so each attempt is recorded separately.
    """

    __slots__ = ("op", "query", "field", "_start", "_ok", "_detail")

    def __init__(self, op: str, query: str = "", field: str = "") -> None:
        self.op = op
        self.query = query
        self.field = field
        self._ok = True
        self._detail = ""
        self._start = 0.0

    def failed(self, detail: str = "") -> None:
        self._ok = False
        self._detail = detail

    def __enter__(self) -> "timed":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None:
            self._ok = False
            self._detail = self._detail or exc_type.__name__
        record(
            self.op,
            (time.perf_counter() - self._start) * 1000.0,
            ok=self._ok,
            query=self.query,
            field=self.field,
            detail=self._detail,
        )
        return False  # never swallow


# ----------------------------------------------------------------- reporting


def read_records(since: Optional[float] = None) -> List[Dict[str, Any]]:
    """Load records, newest last. Malformed lines are skipped, not fatal."""
    try:
        raw = METRICS_FILE.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    cutoff = (time.time() - since) if since else None
    out = []
    for line in raw:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if not isinstance(rec, dict) or "ts" not in rec:
            continue
        if cutoff is not None and float(rec["ts"]) < cutoff:
            continue
        out.append(rec)
    return out


def latest_run(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Trim to the most recent contiguous burst of activity.

    Runs are separated by idle time, not labelled, because nothing tells these
    scripts when an agent decided to start. A gap of RUN_GAP_SECONDS is a
    generous boundary: within a run the agent is thinking, not sleeping for
    five minutes.
    """
    if not records:
        return []
    start = 0
    for i in range(len(records) - 1, 0, -1):
        if float(records[i]["ts"]) - float(records[i - 1]["ts"]) > RUN_GAP_SECONDS:
            start = i
            break
    return records[start:]


def summarise(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Turn call records into the numbers that explain a slow run."""
    if not records:
        return {"calls": 0}
    times = sorted(float(r.get("ms", 0.0)) for r in records)
    tool_ms = sum(times)
    #  Records are written when a call FINISHES, so the first record's timestamp
    #  is the end of the first call, not the start of the run. Without adding its
    #  duration back, a two-call run reports less span than time spent in Censys
    #  and the idle figure clamps to zero - which is exactly wrong for the one
    #  number this tool exists to produce.
    first_ms = float(records[0].get("ms", 0.0))
    span = (float(records[-1]["ts"]) - float(records[0]["ts"])) + first_ms / 1000.0
    by_op: Dict[str, int] = {}
    for r in records:
        by_op[str(r.get("op", "?"))] = by_op.get(str(r.get("op", "?")), 0) + 1
    idle = max(0.0, span - tool_ms / 1000.0)
    return {
        "calls": len(records),
        "by_op": by_op,
        "failed": sum(1 for r in records if not r.get("ok", True)),
        "tool_seconds": round(tool_ms / 1000.0, 1),
        "mean_ms": round(tool_ms / len(records), 0),
        "p95_ms": round(times[min(len(times) - 1, int(len(times) * 0.95))], 0),
        "max_ms": round(times[-1], 0),
        "span_seconds": round(span, 1),
        "idle_seconds": round(idle, 1),
        "idle_percent": round(100.0 * idle / span, 1) if span > 0 else 0.0,
        "started_at": records[0]["ts"],
        "ended_at": records[-1]["ts"],
    }


def format_report(records: List[Dict[str, Any]], label: str) -> str:
    s = summarise(records)
    if not s["calls"]:
        return (
            f"No Censys calls recorded ({label}).\n"
            "Nothing has run yet, or recording is off (CENSYS_TSA_METRICS=0)."
        )
    ops = ", ".join(f"{k} {v}" for k, v in sorted(s["by_op"].items()))
    lines = [
        f"Window         : {label}",
        f"Censys calls   : {s['calls']}  ({ops})"
        + (f"  [{s['failed']} failed]" if s["failed"] else ""),
        f"Time in Censys : {s['tool_seconds']}s"
        f"  (mean {s['mean_ms']:.0f}ms, p95 {s['p95_ms']:.0f}ms, max {s['max_ms']:.0f}ms)",
        f"Run span       : {s['span_seconds']:.0f}s",
        f"Idle gap       : {s['idle_seconds']:.0f}s ({s['idle_percent']}%)"
        "   <- not Censys: agent turns, rate-limit sleep, model latency",
        "",
    ]
    slowest = sorted(records, key=lambda r: -float(r.get("ms", 0)))[:5]
    if slowest and float(slowest[0].get("ms", 0)) > 0:
        lines.append("Slowest calls:")
        for r in slowest:
            what = r.get("field") or r.get("q") or ""
            flag = "" if r.get("ok", True) else f" !{r.get('detail') or 'failed'}"
            lines.append(f"  {float(r.get('ms', 0)) / 1000.0:6.2f}s {r.get('op', '?'):8} {str(what)[:70]}{flag}")
        lines.append("")
    if s["idle_percent"] >= 80.0:
        lines.append(
            "Verdict: turn-bound. Censys is not the bottleneck - the run is waiting on\n"
            "agent turns. Batch independent calls into one `tsa batch`/`tsa probe`/\n"
            "`tsa candidates`, and fan work out across parallel subagents."
        )
    elif s["idle_percent"] > 0:
        lines.append(
            "Verdict: a meaningful share of the run is real Censys time. Check the\n"
            "slowest calls above for heavy regex or union queries before batching."
        )
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa timeline"), not this file, which is not on their PATH.
    parser = argparse.ArgumentParser(
        prog=os.environ.get("CENSYS_TSA_PROG"),
        description="Report where a TSA's wall-clock time went.",
    )
    parser.add_argument(
        "--since", type=float, metavar="SECONDS",
        help="Only calls from the last N seconds (default: the most recent run)",
    )
    parser.add_argument("--all", action="store_true", help="Every recorded call")
    parser.add_argument("-f", "--format", choices=("table", "json"), default="table")
    parser.add_argument("--reset", action="store_true", help="Discard the history")
    args = parser.parse_args(argv)

    if args.reset:
        try:
            METRICS_FILE.unlink()
        except FileNotFoundError:
            pass
        except OSError as exc:
            print(f"could not reset metrics: {exc}", file=sys.stderr)
            return 1
        print("Call timing history cleared.")
        return 0

    if args.all:
        records, label = read_records(), "all recorded calls"
    elif args.since:
        records, label = read_records(args.since), f"last {int(args.since)}s"
    else:
        records, label = latest_run(read_records()), "most recent run"

    if args.format == "json":
        print(json.dumps({"summary": summarise(records), "calls": records}, indent=2))
    else:
        print(format_report(records, label))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
