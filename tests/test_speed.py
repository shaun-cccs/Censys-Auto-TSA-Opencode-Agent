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
import os
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

from tests.helpers import body, censys_cost_simulator, flat, load_util


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
        self.assertEqual(
            fields, set(censys_batch.PROBE_TREES) | set(censys_batch.PROBE_PROTOCOL)
        )
        self.assertIn("host.services.hardware.product", fields)

    def test_covers_the_decoded_protocol_layer(self):
        """Tagging and HTTP content are not the only evidence layers.

        A decoded protocol carries a structured sub-document (`any_connect.*`,
        `ike.*`) that outranks any banner or body regex. Measured cost of
        omitting it: an ASA/FTD run missed 1,661 hosts that
        `any_connect.groups="DefaultWEBVPNGroup"` alone would have found, most of
        them untagged in all three trees. A port aggregation is not this check,
        so the field must be `protocol`, not `port`.
        """
        fields = {item["field"] for item in self.plan() if item["op"] == "agg"}
        self.assertIn("host.services.protocol", fields)

    def test_is_five_calls(self):
        self.assertEqual(len(self.plan()), 5)

    def test_wide_adds_the_step_three_fields(self):
        items = self.plan(wide=True)
        self.assertEqual(len(items), 5 + len(censys_batch.PROBE_WIDE))

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

    def candidate_report(self, incremental, witness):
        """Render one candidate row, with the base count already in place."""
        result = {
            "wall_seconds": 1.0,
            "items": [
                {"op": "count", "label": "base", "total": 100, "error": None,
                 "buckets": [], "hits": [], "query": "base"},
                {"op": "count", "label": "cand", "total": incremental, "error": None,
                 "buckets": [], "hits": [], "query": "cand and not (base)"},
                {"op": "agg", "label": "cand", "total": incremental, "error": None,
                 "buckets": witness, "hits": [], "query": "cand and not (base)"},
            ],
        }
        return censys_batch.format_candidates(result, "base")

    def test_a_real_increment_with_no_titles_is_called_out(self):
        """Measured on a live port candidate: +100,448 hosts and zero titles.

        An empty witness on a real increment is evidence - non-HTTP, fronted, or
        simply not the product - and printing nothing beside the count read as
        "no problem found", which is the opposite of what it means.
        """
        report = self.candidate_report(100_448, [])
        self.assertIn("+100,448", report)
        self.assertRegex(report, r"(?i)no titles on the incremental hosts")

    def test_a_zero_increment_says_the_two_reasons_apart(self):
        report = self.candidate_report(0, [])
        self.assertIn("--totals", report)

    def test_witness_titles_are_shown_when_there_are_any(self):
        report = self.candidate_report(927, [{"key": "Log in to FishEye", "count": 901}])
        self.assertIn("Log in to FishEye", report)
        self.assertNotIn("no titles on the incremental", report)


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

    @unittest.skipIf(censys_batch is None, "censys-platform SDK not available")
    def test_the_probe_price_tracks_the_calls_the_probe_actually_makes(self):
        """A breaker that under-prices a command is a breaker with a hole in it.

        This caught a real drift: `host.services.protocol` was added to the probe,
        taking it from 4 calls to 5, while the plugin still charged 4. The bound is
        derived from the field tuples rather than written down twice, so adding a
        field to the sweep fails here until the price is updated.
        """
        plain = 1 + len(censys_batch.PROBE_TREES) + len(censys_batch.PROBE_PROTOCOL)
        wide = plain + len(censys_batch.PROBE_WIDE)
        self.assertGreaterEqual(
            self.cost("tsa probe 'x'"), plain,
            f"tsa probe issues {plain} requests; the plugin charges less",
        )
        self.assertGreaterEqual(
            self.cost("tsa probe 'x' --wide"), wide,
            f"tsa probe --wide issues {wide} requests; the plugin charges less",
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

    def test_timeline_and_limits_are_free(self):
        """Neither touches Censys, and pricing them would distort the breaker."""
        for command in ["tsa timeline --since 600", "tsa limits none"]:
            with self.subTest(command=command):
                self.assertEqual(self.cost(command), 0)


# ------------------------------------------------------------- rate-limit profiles


class Profiles(unittest.TestCase):
    """`tsa limits` - pacing as a session decision.

    The shipped defaults paced every request by a second and capped the rolling
    budget at 200/hour, while a real run issues 100-300 Censys actions. Every run
    therefore stalled itself, and the prose told the agent to wait it out.
    """

    def setUp(self):
        self.limits = load_util("censys_limits")
        self.tmp = tempfile.TemporaryDirectory()
        self.limits.LIMITS_FILE = Path(self.tmp.name) / "limits.json"
        self._env = dict(os.environ)
        for key in self.limits.ENV_KEYS.values():
            os.environ.pop(key, None)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._env)
        self.tmp.cleanup()

    def test_the_three_profiles_exist_and_are_ordered_by_speed(self):
        names = set(self.limits.PROFILES)
        self.assertEqual(names, {"none", "fast", "standard"})
        none, fast, standard = (self.limits.PROFILES[n] for n in ("none", "fast", "standard"))
        self.assertEqual(none["max_per_minute"], 0, "'none' must not cap per minute")
        self.assertEqual(none["budget_requests"], 0, "'none' must not have a budget")
        self.assertGreater(fast["budget_requests"], standard["budget_requests"])
        self.assertEqual(fast["min_interval"], 0.0)

    def test_none_still_caps_concurrency(self):
        """"No pacing" must not mean "unbounded sockets"."""
        self.assertGreater(self.limits.PROFILES["none"]["concurrency"], 1)
        self.assertLessEqual(self.limits.PROFILES["none"]["concurrency"], 32)

    def test_the_fallback_is_not_the_profile_that_stalls_runs(self):
        """Forgetting to choose must not reintroduce the original stall."""
        self.assertEqual(self.limits.FALLBACK_PROFILE, "fast")
        self.assertEqual(self.limits.profile_name(), "fast")
        settings = self.limits.effective()
        self.assertGreater(settings["budget_requests"], 300, "one run issues 100-300")

    def test_standard_reproduces_the_original_numbers(self):
        standard = self.limits.PROFILES["standard"]
        self.assertEqual(standard["min_interval"], 1.0)
        self.assertEqual(standard["max_per_minute"], 20)
        self.assertEqual(standard["budget_requests"], 200)

    def test_setting_a_profile_persists_it_for_other_processes(self):
        self.limits.write_state("none", by="test")
        self.assertEqual(self.limits.profile_name(), "none")
        self.assertEqual(self.limits.effective()["max_per_minute"], 0)

    def test_clearing_returns_to_the_fallback(self):
        self.limits.write_state("standard")
        self.limits.clear_state()
        self.assertEqual(self.limits.profile_name(), self.limits.FALLBACK_PROFILE)

    def test_an_unknown_profile_in_the_file_is_ignored(self):
        self.limits.LIMITS_FILE.write_text(json.dumps({"profile": "ludicrous"}))
        self.assertEqual(self.limits.profile_name(), self.limits.FALLBACK_PROFILE)

    def test_a_corrupt_file_is_ignored_rather_than_fatal(self):
        self.limits.LIMITS_FILE.write_text("{not json")
        self.assertEqual(self.limits.profile_name(), self.limits.FALLBACK_PROFILE)

    def test_environment_beats_the_profile(self):
        self.limits.write_state("standard")
        os.environ["CENSYS_MAX_PER_MINUTE"] = "77"
        settings, provenance = self.limits.resolve()
        self.assertEqual(settings["max_per_minute"], 77)
        self.assertIn("env", provenance["max_per_minute"])
        self.assertIn("profile", provenance["min_interval"])

    def test_a_junk_environment_value_falls_back_instead_of_crashing(self):
        os.environ["CENSYS_MAX_PER_MINUTE"] = "quickly"
        self.assertEqual(
            self.limits.effective()["max_per_minute"],
            self.limits.PROFILES[self.limits.FALLBACK_PROFILE]["max_per_minute"],
        )

    def test_status_says_what_is_in_force_and_why(self):
        self.limits.write_state("none", by="censys-tsa")
        text = self.limits.format_status()
        self.assertIn("none", text)
        self.assertIn("censys-tsa", text)
        self.assertIn("not a spend limit", text)

    def test_json_status_is_machine_readable(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.assertEqual(self.limits.main(["fast", "-f", "json"]), 0)
        payload = json.loads(buffer.getvalue())
        self.assertEqual(payload["profile"], "fast")
        self.assertIn("min_interval", payload["settings"])

    def test_setting_a_profile_from_the_cli_persists_it(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.limits.main(["none"])
        self.assertEqual(self.limits.profile_name(), "none")


@unittest.skipIf(censys_batch is None, "censys-platform SDK not available")
class ProfileDrivesTheTools(unittest.TestCase):
    """The profile has to reach the code that paces, or it is decoration."""

    def test_query_defaults_come_from_the_profile(self):
        settings = censys_query.censys_limits.effective()
        self.assertEqual(censys_query.DEFAULT_MIN_INTERVAL, settings["min_interval"])
        self.assertEqual(censys_query.DEFAULT_MAX_PER_MINUTE, settings["max_per_minute"])
        self.assertEqual(censys_query.DEFAULT_BUDGET_REQUESTS, settings["budget_requests"])
        self.assertEqual(censys_query.DEFAULT_CONCURRENCY, max(1, settings["concurrency"]))

    def test_nothing_hardcodes_the_old_pacing_defaults(self):
        """The 1s/20/200 numbers must live in the profile table, nowhere else."""
        source = (Path(__file__).resolve().parent.parent / "utils" / "censys_query.py").read_text()
        self.assertNotIn('os.environ.get("CENSYS_MIN_INTERVAL"', source)
        self.assertNotIn('os.environ.get("CENSYS_BUDGET_REQUESTS"', source)

    def test_the_budget_error_tells_the_agent_not_to_wait(self):
        """"Wait rather than raising the budget" is what made runs take an hour."""
        gateway = censys_query.RateLimitGateway(
            min_interval=0.0, max_per_minute=0, budget_requests=1, budget_window=3600,
            state_file=None,
        )
        with tempfile.TemporaryDirectory() as tmp:
            gateway.state_file = Path(tmp) / "state.json"
            gateway.acquire()
            with self.assertRaises(censys_query.RateLimitError) as caught:
                gateway.acquire()
        message = str(caught.exception)
        self.assertIn("Do NOT wait", message)
        self.assertIn("tsa limits", message)


class LedgersAreLocked(unittest.TestCase):
    """Parallel subagents share these files; a lost update loses spend."""

    def source(self) -> str:
        return (Path(__file__).resolve().parent.parent / "utils" / "censys_query.py").read_text()

    def test_a_lock_helper_exists_and_degrades_rather_than_failing(self):
        text = self.source()
        self.assertIn("def file_lock(", text)
        self.assertIn("import fcntl", text)
        self.assertRegex(text, r"except ImportError")

    def test_both_read_modify_write_paths_take_the_lock(self):
        text = self.source()
        for function in ("def charge_credits(", "def _record_budget_use("):
            with self.subTest(function=function):
                start = text.index(function)
                body = text[start:start + 1400]
                self.assertIn("file_lock(", body, f"{function} is unlocked")


class RateProfileIsACapability(unittest.TestCase):
    """It is carried in the capability set, and honestly labelled as unenforced."""

    def setUp(self):
        self.source = (
            Path(__file__).resolve().parent.parent
            / ".opencode" / "plugin" / "tsa-capabilities.ts"
        ).read_text()

    def test_the_plugin_carries_the_choice(self):
        self.assertIn("rateLimit", self.source)
        self.assertRegex(self.source, r'case "rate":')

    def test_the_plugin_default_matches_the_python_fallback(self):
        limits = load_util("censys_limits")
        self.assertRegex(self.source, rf'rateLimit: "{limits.FALLBACK_PROFILE}"')

    def test_the_plugin_says_it_cannot_enforce_pacing(self):
        """Pacing happens inside a Python process, not at the tool boundary."""
        self.assertRegex(self.source, r"cannot enforce|cannot apply")
        self.assertIn("tsa limits", self.source)

    def test_pacing_is_not_gated_like_a_network_capability(self):
        self.assertNotRegex(self.source, r'input\.tool === "\w+" && !caps\.rateLimit')


class UnattendedRunsChooseTheirPacing(unittest.TestCase):
    def setUp(self):
        self.tsa_run = load_util("tsa_run")

    def args(self, **overrides):
        base = dict(
            target="X", cve=None, product=None, allow_web=False,
            allow_endpoint_check=False, deep_dive=False, budget=None,
            version_breakdown=False, no_reports=False, print_spec=False, rate="fast",
        )
        base.update(overrides)
        return argparse.Namespace(**base)

    def test_the_capability_line_carries_the_rate(self):
        self.assertIn("rate=none", self.tsa_run.build_capabilities(self.args(rate="none")))
        self.assertIn("rate=fast", self.tsa_run.build_capabilities(self.args()))

    def test_the_wrapper_applies_the_profile_itself(self):
        """An unattended run has nobody to notice the agent skipped the step."""
        with mock.patch.object(self.tsa_run.subprocess, "run") as run:
            run.return_value = mock.Mock(returncode=0, stderr="", stdout="")
            self.tsa_run.apply_rate_profile("none")
        command = run.call_args[0][0]
        self.assertIn("limits", command)
        self.assertIn("none", command)

    def test_a_failure_to_set_pacing_is_reported_not_fatal(self):
        with mock.patch.object(self.tsa_run.subprocess, "run", side_effect=OSError("nope")):
            message = self.tsa_run.apply_rate_profile("fast")
        self.assertIn("could not set pacing", message)


class AgentsAreToldNotToWait(unittest.TestCase):
    """The instruction that cost the most: "wait rather than raising the budget"."""

    def text(self, name: str) -> str:
        return flat((Path(__file__).resolve().parent.parent / "references" / f"{name}.md").read_text())

    def test_the_old_wait_instruction_is_gone(self):
        self.assertNotIn("wait rather than raising the budget", self.text("workspace"))

    def test_never_sleep_is_stated_explicitly(self):
        workspace = self.text("workspace")
        self.assertRegex(workspace, r"(?i)never sleep")
        self.assertIn("tsa limits", workspace)

    def test_the_profiles_are_documented_for_the_agents(self):
        workspace = self.text("workspace")
        for profile in ("none", "fast", "standard"):
            with self.subTest(profile=profile):
                self.assertIn(f"`{profile}`", workspace)

    def test_the_interview_asks_about_pacing(self):
        prompt = flat(body("censys-tsa"))
        self.assertRegex(prompt, r"(?i)censys pacing")
        self.assertIn("tsa limits", prompt)
        self.assertRegex(prompt, r"(?i)no limits \(recommended\)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
