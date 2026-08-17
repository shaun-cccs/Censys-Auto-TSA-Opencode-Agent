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

import argparse
import contextlib
import io
import json
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import censys_cost_simulator, load_util


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


# --------------------------------------------------------------------- batching
#
#  These import the utils, so they need the Censys SDK and skip without it - the
#  same bargain test_censys_credits.py makes. utils/ is a directory of flat
#  scripts, not a package, so it goes on sys.path exactly as running one would.

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))

try:
    import censys_batch
    import censys_metrics as _metrics
    import censys_query
    from censys_aggregate import run_multi_aggregate
except ImportError as exc:  # pragma: no cover - environment, not logic
    censys_batch = None
    _IMPORT_ERROR = str(exc)


def free_gateway():
    """A gateway that neither paces nor persists.

    Every control off: the tests are about the batching engine, and a gateway
    with the shipped defaults would sleep a second between items and write to
    the real rate-state file in the user's home directory.
    """
    return censys_query.RateLimitGateway(
        min_interval=0.0, max_per_minute=0, budget_requests=0, state_file=None
    )


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def model_dump(self, **_kwargs):
        return self._payload


class FakeEnvelope:
    def __init__(self, payload):
        self.result = FakeResponse(payload)


class FakeGlobalData:
    """Counts overlap, so a test can prove requests really are concurrent."""

    def __init__(self, delay=0.0, fail_on=None):
        self.delay = delay
        self.fail_on = fail_on or set()
        self.calls = []
        self.max_in_flight = 0
        self._in_flight = 0
        self._lock = threading.Lock()

    def _enter(self, what):
        with self._lock:
            self.calls.append(what)
            self._in_flight += 1
            self.max_in_flight = max(self.max_in_flight, self._in_flight)

    def _exit(self):
        with self._lock:
            self._in_flight -= 1

    def search(self, search_query_input_body):
        query = search_query_input_body["query"]
        self._enter(("search", query))
        try:
            time.sleep(self.delay)
            if query in self.fail_on:
                raise RuntimeError("synthetic failure")
            #  A float, exactly as the real endpoint returns it.
            return FakeEnvelope({"total_hits": 7.0, "hits": [{"host_v1": {"resource": {"ip": "1.2.3.4"}}}]})
        finally:
            self._exit()

    def aggregate(self, search_aggregate_input_body):
        field = search_aggregate_input_body["field"]
        self._enter(("agg", field))
        try:
            time.sleep(self.delay)
            if field in self.fail_on:
                raise RuntimeError("synthetic failure")
            return FakeEnvelope({"total_count": 5, "buckets": [{"key": "a", "count": 3}]})
        finally:
            self._exit()


class FakeSDK:
    def __init__(self, global_data):
        self.global_data = global_data

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


@unittest.skipIf(censys_batch is None, "censys-platform SDK not available")
class BatchEngine(unittest.TestCase):
    """`tsa batch` - many independent calls, one turn."""

    def setUp(self):
        _metrics.ENABLED = False  # never write to the real history from a test
        self.api = FakeGlobalData()
        self.patches = [
            mock.patch.object(censys_batch, "SDK", lambda **_kw: FakeSDK(self.api)),
            mock.patch.object(censys_batch, "get_personal_access_token", lambda: "t"),
            mock.patch.object(censys_batch, "get_org_id", lambda org_id=None: "org"),
        ]
        for patch in self.patches:
            patch.start()

    def tearDown(self):
        for patch in self.patches:
            patch.stop()
        _metrics.ENABLED = True

    def run_items(self, items, **kwargs):
        return censys_batch.run_batch(items, free_gateway(), **kwargs)

    def test_results_keep_the_callers_order(self):
        """Completion order is arbitrary; report order must not be."""
        items = [
            censys_batch.make_item("count", f"q{i}", label=f"L{i}") for i in range(6)
        ]
        result = self.run_items(items, concurrency=6)
        self.assertEqual([item["label"] for item in result["items"]], [f"L{i}" for i in range(6)])

    def test_counts_are_normalised_to_integers(self):
        """total_hits arrives as a float; leaving it made counts render as "?"."""
        result = self.run_items([censys_batch.make_item("count", "q")])
        self.assertEqual(result["items"][0]["total"], 7)
        self.assertIsInstance(result["items"][0]["total"], int)

    def test_calls_actually_overlap(self):
        """The whole point. Serial execution would take 8 x the delay."""
        self.api.delay = 0.05
        items = [censys_batch.make_item("count", f"q{i}") for i in range(8)]
        started = time.perf_counter()
        self.run_items(items, concurrency=8)
        elapsed = time.perf_counter() - started
        self.assertGreater(self.api.max_in_flight, 1, "requests were issued serially")
        self.assertLess(elapsed, 0.05 * 8 * 0.6, "no useful parallelism")

    def test_concurrency_one_is_serial(self):
        self.api.delay = 0.01
        items = [censys_batch.make_item("count", f"q{i}") for i in range(4)]
        self.run_items(items, concurrency=1)
        self.assertEqual(self.api.max_in_flight, 1)

    def test_one_bad_item_does_not_sink_the_batch(self):
        """A heavy regex that times out must not cost the other nineteen answers."""
        self.api.fail_on = {"bad"}
        items = [
            censys_batch.make_item("count", "good"),
            censys_batch.make_item("count", "bad"),
            censys_batch.make_item("agg", "good", field="host.services.port"),
        ]
        result = self.run_items(items, concurrency=3)
        self.assertIsNone(result["items"][0]["error"])
        self.assertIsNotNone(result["items"][1]["error"])
        self.assertEqual(result["items"][2]["buckets"], [{"key": "a", "count": 3}])

    def test_an_empty_batch_is_not_an_error(self):
        result = self.run_items([])
        self.assertEqual(result["items"], [])

    def test_an_unknown_op_is_rejected_at_build_time(self):
        with self.assertRaises(ValueError):
            censys_batch.make_item("delete", "q")

    def test_an_aggregation_needs_a_field(self):
        with self.assertRaises(ValueError):
            censys_batch.make_item("agg", "q")


@unittest.skipIf(censys_batch is None, "censys-platform SDK not available")
class ProbePlan(unittest.TestCase):
    """`tsa probe` - step 1's mandated sweep, in one call."""

    def plan(self, seed="'x'", **overrides):
        args = argparse.Namespace(
            seed=seed, wide=False, max_results=3, buckets=10,
            count_by_level=None, raw_seed=False,
        )
        for key, value in overrides.items():
            setattr(args, key, value)
        return censys_batch.build_probe_items(args)

    def test_covers_all_three_tag_trees(self):
        """Second principle: checking one tree is how "untagged" goes wrong."""
        fields = {item["field"] for item in self.plan() if item["op"] == "agg"}
        self.assertEqual(fields, set(censys_batch.PROBE_TREES))
        self.assertIn("host.services.hardware.product", fields)

    def test_is_four_calls(self):
        self.assertEqual(len(self.plan()), 4)

    def test_wide_adds_the_step_three_fields(self):
        items = self.plan(wide=True)
        self.assertEqual(len(items), 4 + len(censys_batch.PROBE_WIDE))

    def test_the_sample_is_host_scoped(self):
        """A bare full-text seed also matches web properties and certificates."""
        sample = self.plan(seed='"MOVEit"')[0]
        self.assertEqual(sample["op"], "sample")
        self.assertIn(censys_batch.HOST_SCOPE_CLAUSE, sample["query"])

    def test_raw_seed_leaves_the_query_alone(self):
        sample = self.plan(seed='"MOVEit"', raw_seed=True)[0]
        self.assertEqual(sample["query"], '"MOVEit"')

    def test_aggregations_take_the_seed_unchanged(self):
        """They bucket host.* fields, so the field does the scoping."""
        for item in self.plan(seed='"MOVEit"'):
            if item["op"] == "agg":
                self.assertEqual(item["query"], '"MOVEit"')

    def test_host_scoping_is_idempotent(self):
        once = censys_batch.host_scoped("x")
        self.assertEqual(censys_batch.host_scoped(once), once)


@unittest.skipIf(censys_batch is None, "censys-platform SDK not available")
class CandidatePlan(unittest.TestCase):
    """`tsa candidates` - step 8b, with the evidence check built in."""

    def plan(self, base="base", candidates=("c1", "c2"), **overrides):
        args = argparse.Namespace(
            base=base, candidates=list(candidates), buckets=10,
            witness=True, witness_field=censys_batch.DEFAULT_WITNESS_FIELD, totals=False,
        )
        for key, value in overrides.items():
            setattr(args, key, value)
        return censys_batch.build_candidate_items(args)

    def test_shape_is_base_plus_two_per_candidate(self):
        self.assertEqual(len(self.plan()), 1 + 2 * 2)

    def test_every_candidate_subtracts_the_base(self):
        """Step 8b: the increment is the only interesting number."""
        for item in self.plan()[1:]:
            self.assertIn("and not (base)", item["query"])

    def test_the_witness_aggregation_counts_hosts(self):
        """"How many hosts carry this title", not how many occurrences."""
        aggs = [item for item in self.plan() if item["op"] == "agg"]
        self.assertTrue(aggs)
        for agg in aggs:
            self.assertEqual(agg["count_by_level"], censys_batch.COUNT_LEVEL_HOST)
            self.assertEqual(agg["field"], censys_batch.DEFAULT_WITNESS_FIELD)

    def test_no_titles_halves_the_cost_and_the_evidence(self):
        self.assertEqual(len(self.plan(witness=False)), 1 + 2)

    def test_totals_adds_a_standalone_count_per_candidate(self):
        """An increment of 0 is ambiguous without it."""
        self.assertEqual(len(self.plan(totals=True)), 1 + 3 * 2)

    def test_candidates_are_labelled_so_pairs_can_be_matched_up(self):
        labels = {item["label"] for item in self.plan()[1:]}
        self.assertEqual(labels, {"c1", "c2"})


@unittest.skipIf(censys_batch is None, "censys-platform SDK not available")
class Rendering(unittest.TestCase):
    def test_a_non_host_hit_is_named_not_hidden(self):
        """It used to print "?", which reads as a broken query."""
        line = censys_batch._host_line(
            {"webproperty_v1": {"resource": {"hostname": "dsldevice.lan", "port": 443}}}
        )
        self.assertIn("webproperty_v1", line)
        self.assertIn("dsldevice.lan", line)
        self.assertIn("not a host", line)

    def test_a_host_hit_renders_ip_country_and_ports(self):
        line = censys_batch._host_line(
            {"host_v1": {"resource": {
                "ip": "1.2.3.4",
                "location": {"country": "Canada"},
                "services": [{"port": 443}, {"port": 22}],
            }}}
        )
        self.assertIn("1.2.3.4", line)
        self.assertIn("Canada", line)
        self.assertIn("22,443", line)

    def test_plan_files_accept_json_and_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            array = Path(tmp) / "a.json"
            array.write_text(json.dumps([{"op": "count", "query": "x"}]))
            lines = Path(tmp) / "b.jsonl"
            lines.write_text('{"op":"count","query":"x"}\n{"op":"agg","field":"f","query":"y"}\n')
            self.assertEqual(len(censys_batch.load_plan(str(array))), 1)
            self.assertEqual(len(censys_batch.load_plan(str(lines))), 2)


@unittest.skipIf(censys_batch is None, "censys-platform SDK not available")
class TimeoutPolicy(unittest.TestCase):
    """A timeout is the backend giving up, not network weather.

    Retried four times with backoff, one unfinishable union query cost over four
    minutes and four credits before failing anyway. Saved specs in reports/
    record exactly that happening twice in a single run.
    """

    def setUp(self):
        _metrics.ENABLED = False

    def tearDown(self):
        _metrics.ENABLED = True

    def test_timeouts_are_recognised_however_they_surface(self):
        class ReadTimeout(Exception):
            pass

        self.assertTrue(censys_query.is_timeout(ReadTimeout()))
        self.assertTrue(censys_query.is_timeout(Exception("operation timed out")))
        self.assertFalse(censys_query.is_timeout(Exception("422 invalid character")))

    def test_a_timeout_stops_after_two_attempts_and_says_what_to_do(self):
        attempts = []

        class Api:
            def search(self, search_query_input_body):
                attempts.append(1)
                raise TimeoutError("read timeout")

        _, error = censys_query.censys_search_page(
            FakeSDK(Api()), "heavy", free_gateway(), max_retries=4, base_delay=0.0
        )
        self.assertEqual(len(attempts), censys_query.TIMEOUT_MAX_ATTEMPTS)
        self.assertIn("query_timeout", error)
        self.assertIn("simplify", error)

    def test_other_failures_still_get_the_full_retry_budget(self):
        attempts = []

        class Api:
            def search(self, search_query_input_body):
                attempts.append(1)
                raise ConnectionResetError("blip")

        censys_query.censys_search_page(
            FakeSDK(Api()), "q", free_gateway(), max_retries=4, base_delay=0.0
        )
        self.assertEqual(len(attempts), 4)


@unittest.skipIf(censys_batch is None, "censys-platform SDK not available")
class SuggestFieldsIsConcurrent(unittest.TestCase):
    """`--suggest-fields` was thirteen serial round trips."""

    def setUp(self):
        _metrics.ENABLED = False
        self.api = FakeGlobalData(delay=0.05)
        self.patches = [
            mock.patch("censys_aggregate.SDK", lambda **_kw: FakeSDK(self.api)),
            mock.patch("censys_aggregate.get_personal_access_token", lambda: "t"),
            mock.patch("censys_aggregate.get_org_id", lambda org_id=None: "org"),
        ]
        for patch in self.patches:
            patch.start()

    def tearDown(self):
        for patch in self.patches:
            patch.stop()
        _metrics.ENABLED = True

    def test_fields_are_aggregated_together_and_stay_in_order(self):
        fields = [f"f{i}" for i in range(8)]
        result = run_multi_aggregate(fields, "q", free_gateway(), concurrency=8)
        self.assertEqual([agg["field"] for agg in result["aggregations"]], fields)
        self.assertGreater(self.api.max_in_flight, 1)


class BatchCostsAreMetered(unittest.TestCase):
    """The circuit-breaker must price a batch above a single call.

    The item count is not knowable from a command line, so these are deliberate
    over-estimates - a batching loop has to trip the breaker, not slip under it.
    """

    @classmethod
    def setUpClass(cls):
        cls.cost = staticmethod(censys_cost_simulator())

    def test_probe_is_priced_as_a_sweep(self):
        self.assertGreaterEqual(self.cost("tsa probe '\"MOVEit\"'"), 4)
        self.assertGreater(
            self.cost("tsa probe 'x' --wide"), self.cost("tsa probe 'x'")
        )

    def test_candidates_is_priced_per_candidate(self):
        self.assertGreaterEqual(self.cost("tsa candidates 'base' 'c1' 'c2'"), 5)
        self.assertGreater(
            self.cost("tsa candidates 'b' 'c' --totals"),
            self.cost("tsa candidates 'b' 'c'"),
        )

    def test_batch_is_never_free(self):
        for command in ["tsa batch --count 'x'", "tsa batch -p plan.json"]:
            with self.subTest(command=command):
                self.assertGreater(self.cost(command), 1)

    def test_timeline_is_free(self):
        self.assertEqual(self.cost("tsa timeline --since 600"), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
