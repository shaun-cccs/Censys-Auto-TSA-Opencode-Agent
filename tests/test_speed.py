#!/usr/bin/env python3
"""The speed subsystem: call timing, batching, and rate-limit profiles.

These three exist for one reason. Measured on this kit, a Censys API action
costs roughly 0.7-2.6s end to end, while a full TSA issues on the order of a
hundred of them and takes 30-60 minutes - so the time was never in Censys, it
was in serial agent turns and in a rate limiter whose default rolling budget
(200 requests/hour) was below what a single run needs.

``tsa timeline`` proves where the time goes, ``tsa batch`` collapses many calls
into one turn, and the rate-limit profiles stop the limiter from stalling a run
it should not have been pacing.

Run::

    python -m unittest tests.test_speed -v
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import time
import unittest
from pathlib import Path

from tests.helpers import load_util


class Metrics(unittest.TestCase):
    """`tsa timeline` - the number that settles "why is this slow"."""

    def setUp(self):
        self.metrics = load_util("censys_metrics")
        self.tmp = tempfile.TemporaryDirectory()
        self.metrics.METRICS_FILE = Path(self.tmp.name) / "m.jsonl"
        self.metrics.ENABLED = True

    def tearDown(self):
        self.tmp.cleanup()

    def test_records_round_trip(self):
        self.metrics.record("search", 120.0, query="x")
        self.metrics.record("agg", 80.0, query="x", field="host.services.port")
        records = self.metrics.read_records()
        self.assertEqual([r["op"] for r in records], ["search", "agg"])
        self.assertEqual(records[1]["field"], "host.services.port")

    def test_recording_never_raises(self):
        """Metrics are a bystander to the query and must never break a run."""
        self.metrics.METRICS_FILE = Path(self.tmp.name) / "nope" / "deeper" / "m.jsonl"
        self.metrics.record("search", 1.0)  # must not raise

    def test_disabled_writes_nothing(self):
        self.metrics.ENABLED = False
        self.metrics.record("search", 1.0)
        self.assertEqual(self.metrics.read_records(), [])

    def test_timed_records_duration_and_success(self):
        with self.metrics.timed("search", query="q"):
            time.sleep(0.01)
        record = self.metrics.read_records()[0]
        self.assertTrue(record["ok"])
        self.assertGreater(record["ms"], 5)

    def test_timed_marks_exceptions_as_failures_without_swallowing(self):
        with self.assertRaises(ValueError):
            with self.metrics.timed("search", query="q"):
                raise ValueError("boom")
        record = self.metrics.read_records()[0]
        self.assertFalse(record["ok"])
        self.assertEqual(record["detail"], "ValueError")

    def test_malformed_lines_are_skipped_not_fatal(self):
        self.metrics.record("search", 1.0)
        with open(self.metrics.METRICS_FILE, "a") as fh:
            fh.write("not json at all\n")
        self.assertEqual(len(self.metrics.read_records()), 1)

    def test_span_includes_the_first_calls_own_duration(self):
        """Records are written when a call ENDS.

        Without adding the first call's duration back, a short run reports less
        span than time spent in Censys and the idle gap clamps to zero - which
        inverts the one conclusion this tool exists to support.
        """
        now = time.time()
        records = [
            {"ts": now, "op": "search", "ms": 2000.0, "ok": True},
            {"ts": now + 3, "op": "agg", "ms": 2600.0, "ok": True},
        ]
        summary = self.metrics.summarise(records)
        self.assertAlmostEqual(summary["span_seconds"], 5, delta=0.6)
        self.assertGreater(summary["idle_seconds"], 0)

    def test_idle_gap_dominates_a_turn_bound_run(self):
        """The real shape of a TSA: ~100 fast calls spread over half an hour."""
        now = time.time()
        records = [
            {"ts": now + i * 20, "op": "search", "ms": 900.0, "ok": True}
            for i in range(90)
        ]
        summary = self.metrics.summarise(records)
        self.assertGreater(summary["idle_percent"], 90)
        self.assertIn("turn-bound", self.metrics.format_report(records, "test"))

    def test_latest_run_splits_on_an_idle_gap(self):
        now = time.time()
        records = [
            {"ts": now - 5000, "op": "search", "ms": 10.0, "ok": True},
            {"ts": now - 4999, "op": "search", "ms": 10.0, "ok": True},
            {"ts": now - 10, "op": "agg", "ms": 10.0, "ok": True},
            {"ts": now - 9, "op": "agg", "ms": 10.0, "ok": True},
        ]
        self.assertEqual(len(self.metrics.latest_run(records)), 2)

    def test_empty_history_reports_cleanly(self):
        self.assertEqual(self.metrics.summarise([])["calls"], 0)
        self.assertIn("No Censys calls", self.metrics.format_report([], "test"))

    def test_json_summary_is_machine_readable(self):
        self.metrics.record("search", 100.0)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.assertEqual(self.metrics.main(["-f", "json"]), 0)
        self.assertIn("summary", json.loads(buffer.getvalue()))

    def test_history_is_pruned_when_it_grows(self):
        self.metrics.MAX_BYTES = 200
        self.metrics.KEEP_LINES = 3
        for _ in range(40):
            self.metrics.record("search", 1.0, query="x" * 50)
        self.assertLessEqual(len(self.metrics.read_records()), 5)


class MetricsAreWiredIn(unittest.TestCase):
    """Instrumentation must sit at the chokepoints, inside the gateway.

    Timing the gateway *and* the request together would fold rate-limit sleep
    into "time in Censys" and hide the stall. The tests read the source because
    importing these modules needs the SDK, which the fast suite does without.
    """

    def source(self, name: str) -> str:
        return (Path(__file__).resolve().parent.parent / "utils" / f"{name}.py").read_text()

    def test_search_is_timed(self):
        text = self.source("censys_query")
        self.assertIn("import censys_metrics", text)
        self.assertRegex(text, r'censys_metrics\.timed\("search"')

    def test_aggregation_is_timed(self):
        text = self.source("censys_aggregate")
        self.assertIn("import censys_metrics", text)
        self.assertRegex(text, r'censys_metrics\.timed\("agg"')

    def test_timing_starts_after_the_gateway(self):
        """gateway.acquire() may sleep; that is span, not Censys time."""
        for name in ("censys_query", "censys_aggregate"):
            with self.subTest(module=name):
                text = self.source(name)
                acquire = text.index("gateway.acquire()")
                timed = text.index("censys_metrics.timed", acquire)
                self.assertGreater(
                    timed, acquire,
                    "the timer must start after the rate-limit wait, or sleep is "
                    "misreported as Censys latency",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
