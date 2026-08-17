#!/usr/bin/env python3
"""Fan-out topology: leads, waves, call caps, and the completion signal.

Discovery used to be one subagent doing 15-25 probes serially while the
orchestrator waited, and the deep dive one more doing 25-40. Wall-clock time in
this workflow is very nearly the number of *serial turns*, so the fix is to run
independent hypotheses concurrently and to give every worker a hard stop.

These tests guard the four things that make that safe rather than merely fast:

  1. parallel task calls are issued in ONE message - sequential task calls are
     sequential waits, which is the thing being fixed;
  2. every worker has a call cap, so fan-out cannot multiply spend without bound;
  3. every worker ends with a STATUS line, so "is it done" is never inferred;
  4. nothing anywhere is told to sleep, poll or wait.

Run::

    python -m unittest tests.test_fanout -v
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from tests.helpers import AGENTS, ORCHESTRATORS, REFERENCES, SUBAGENTS, body, flat, tsa

#  Workers that hunt. censys-report writes files and has no lead of its own.
WORKERS = ["censys-fingerprint", "censys-deepdive"]

#  Every agent returns a message the orchestrator has to interpret.
RETURNING_AGENTS = SUBAGENTS


def reference(name: str) -> str:
    return (REFERENCES / f"{name}.md").read_text()


class LeadProtocol(unittest.TestCase):
    """`tsa ref leads` is the contract both orchestrators are bound by."""

    def setUp(self):
        self.text = reference("leads")
        self.flat = flat(self.text)

    def test_the_reference_exists_and_is_printable(self):
        proc = tsa("ref", "leads")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("lead", proc.stdout.lower())

    def test_both_orchestrators_are_pointed_at_it(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertIn("tsa ref leads", body(agent))

    def test_it_states_the_cost_model_that_justifies_fan_out(self):
        """Without the numbers, "go faster" is just an instruction to hurry."""
        self.assertRegex(self.flat, r"(?i)call (takes|costs) about a second")
        self.assertRegex(self.flat, r"(?i)turn (takes|costs) tens of seconds")

    def test_it_caps_width_and_waves(self):
        self.assertRegex(self.flat, r"(?i)workers per wave \| 4")
        self.assertRegex(self.flat, r"(?i)waves per phase \| 3")

    def test_it_caps_calls_per_worker(self):
        for role in ("lead worker", "recon worker", "deep-dive family worker"):
            with self.subTest(role=role):
                self.assertIn(role, self.flat)

    def test_a_lead_has_a_testable_shape(self):
        for key in ("hypothesis", "seed_query", "why", "call_cap"):
            with self.subTest(key=key):
                self.assertIn(key, self.text)

    def test_it_rejects_one_worker_per_query(self):
        """A worker costs a turn to start; a query costs a second."""
        self.assertRegex(self.flat, r"(?i)per-query parallelism belongs in `tsa batch`")

    def test_it_keeps_judgement_with_the_orchestrator(self):
        """Splitting the work must not split the rules that need the whole view."""
        self.assertRegex(self.flat, r"(?i)does \*\*not\*\* distribute the judgement")
        self.assertRegex(self.flat, r"(?i)a worker reports; the orchestrator decides")

    def test_it_is_honest_about_cost(self):
        self.assertRegex(self.flat, r"(?i)fan-out spends more")


class OrchestratorsFanOut(unittest.TestCase):
    def test_they_recon_with_one_call_before_fanning_out(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertIn("tsa probe", body(agent))

    def test_parallel_task_calls_must_be_in_one_message(self):
        """Sequential task calls are sequential waits."""
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertRegex(
                    flat(body(agent)),
                    r"(?i)(in a single message|all in a single message)",
                    f"{agent} must say the parallel task calls go in ONE message",
                )

    def test_they_state_the_fan_out_width_and_wave_limit(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                text = flat(body(agent))
                self.assertRegex(text, r"(?i)(four|4) (workers|is the default)")
                self.assertRegex(text, r"(?i)(three waves|3 waves|three)")

    def test_they_hand_each_worker_a_mode_and_a_cap(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                text = body(agent)
                self.assertIn("MODE:", text)
                self.assertRegex(flat(text), r"(?i)call cap|cap of \d+")

    def test_they_own_the_union_and_the_count_when_the_hunt_fans_out(self):
        """Several family workers cannot each run their own tsa assess."""
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertRegex(flat(body(agent)), r"(?i)MODE: family")

    def test_a_missing_status_line_is_handled_rather_than_retried(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertRegex(
                    flat(body(agent)),
                    r"(?i)without (its|the) `?STATUS",
                    f"{agent} must say what to do with a worker that returns no status",
                )


class WorkersHaveHardStops(unittest.TestCase):
    def test_every_worker_declares_its_modes(self):
        for agent in WORKERS:
            with self.subTest(agent=agent):
                self.assertRegex(body(agent), r"##.*[Mm]ode", f"{agent} has no MODE section")

    def test_every_worker_has_a_call_cap(self):
        for agent in WORKERS:
            with self.subTest(agent=agent):
                text = flat(body(agent))
                self.assertRegex(text, r"(?i)\d+ calls")
                self.assertRegex(
                    text, r"(?i)cap is a limit, not a target",
                    f"{agent} must treat the cap as a ceiling, not a quota",
                )

    def test_every_worker_returns_partial_rather_than_overrunning(self):
        for agent in WORKERS:
            with self.subTest(agent=agent):
                self.assertIn("STATUS: PARTIAL", body(agent))

    def test_every_worker_reports_what_it_did_not_pursue(self):
        """The leads a worker declines are how the next wave gets planned."""
        for agent in WORKERS:
            with self.subTest(agent=agent):
                self.assertIn('"leads"', body(agent))

    def test_every_worker_reports_its_call_count(self):
        for agent in WORKERS:
            with self.subTest(agent=agent):
                self.assertIn("calls_made", body(agent))

    def test_the_fingerprint_worker_returns_a_verdict_and_examples(self):
        text = body("censys-fingerprint")
        self.assertIn('"verdict"', text)
        self.assertIn('"examples"', text)
        self.assertRegex(flat(text), r"(?i)confirmed.*rejected.*inconclusive")

    def test_workers_are_told_to_stay_in_their_lane(self):
        """Two workers answering the same question is a wasted wave."""
        for agent in WORKERS:
            with self.subTest(agent=agent):
                self.assertRegex(flat(body(agent)), r"(?i)stay in (your|its) (lane|family)")


class CompletionIsSignalled(unittest.TestCase):
    """"Is it finished" must never be inferred from the shape of a message."""

    def test_every_returning_agent_ends_with_a_status_line(self):
        for agent in RETURNING_AGENTS:
            with self.subTest(agent=agent):
                text = body(agent)
                self.assertIn("STATUS: DONE", text)
                self.assertRegex(
                    flat(text), r"(?i)last line",
                    f"{agent} must put the status line last, where it can be found",
                )

    def test_the_marker_is_spelled_the_same_way_everywhere(self):
        """A marker the orchestrator cannot match is not a marker."""
        for agent in RETURNING_AGENTS:
            with self.subTest(agent=agent):
                self.assertRegex(body(agent), r"STATUS: (DONE|PARTIAL|BLOCKED)")

    def test_blocked_is_distinguishable_from_finished(self):
        for agent in WORKERS:
            with self.subTest(agent=agent):
                self.assertIn("STATUS: BLOCKED", body(agent))


class NobodyWaits(unittest.TestCase):
    """The observed failure: agents sleeping to "let queries finish".

    Nothing in this workflow runs in the background. A task call returns when the
    worker is done and a bash call returns when the command exits, so a wait is
    pure dead time - and a `sleep` inside a subagent is invisible dead time.
    """

    def test_every_agent_is_told_not_to_sleep_or_poll(self):
        for agent in AGENTS:
            with self.subTest(agent=agent):
                self.assertRegex(
                    flat(body(agent)),
                    r"(?i)never sleep|do not sleep|never sleep, never poll",
                    f"{agent} is not told never to sleep",
                )

    def test_no_agent_is_told_to_wait_for_a_limit(self):
        for agent in AGENTS:
            with self.subTest(agent=agent):
                self.assertNotRegex(
                    flat(body(agent)),
                    r"(?i)wait (it out|rather than raising)",
                    f"{agent} still tells the model to wait out a rate limit",
                )

    def test_no_shipped_prose_suggests_a_sleep_command(self):
        for path in sorted(REFERENCES.glob("*.md")):
            with self.subTest(reference=path.stem):
                self.assertNotRegex(
                    path.read_text(),
                    r"^\s*sleep \d",
                    f"{path.name} contains a sleep command",
                )


class QuickCards(unittest.TestCase):
    """`--brief` exists so a worker with one hypothesis does not load 25KB.

    Each worker used to read four to six full references before its first query.
    That is both turns and context: the whole text is then re-processed on every
    later turn of that worker.
    """

    CARDED = ["leads", "workspace", "fingerprinting", "deep-dive", "cenql-rules",
              "aggregation-semantics", "cve-workflow", "counting-and-report"]

    def test_the_references_workers_read_have_a_quick_card(self):
        for name in self.CARDED:
            with self.subTest(reference=name):
                self.assertIn("## Quick card", reference(name))

    def test_every_reference_an_agent_is_told_to_read_briefly_has_a_card(self):
        """`--brief` falls back to the full text, silently costing the saving."""
        for agent in AGENTS:
            for name in re.findall(r"tsa ref ([a-z][a-z-]*) --brief", body(agent)):
                with self.subTest(agent=agent, reference=name):
                    self.assertIn(
                        "## Quick card", reference(name),
                        f"{agent} reads {name} --brief but it has no card",
                    )

    def test_a_card_is_a_fraction_of_the_full_text(self):
        for name in self.CARDED:
            with self.subTest(reference=name):
                brief = tsa("ref", name, "--brief").stdout
                full = tsa("ref", name).stdout
                self.assertGreater(len(brief), 400, "a card that says nothing is not a card")
                self.assertLess(
                    len(brief), len(full) * 0.5,
                    f"{name}'s card is not meaningfully shorter than the reference",
                )

    def test_a_card_points_back_at_the_full_reference(self):
        for name in self.CARDED:
            with self.subTest(reference=name):
                self.assertIn(f"tsa ref {name}", tsa("ref", name, "--brief").stdout)

    def test_brief_falls_back_to_the_whole_reference(self):
        """A reference with no card must print in full, not print nothing."""
        uncarded = [
            path.stem for path in REFERENCES.glob("*.md")
            if "## Quick card" not in path.read_text()
        ]
        if not uncarded:
            self.skipTest("every reference has a card")
        proc = tsa("ref", uncarded[0], "--brief")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertGreater(len(proc.stdout), 400)
        self.assertIn("no quick card", proc.stderr)

    def test_an_unknown_ref_flag_fails_loudly(self):
        proc = tsa("ref", "leads", "--verbose")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unexpected argument", proc.stderr)

    def test_workers_are_told_to_read_cards_first_and_in_one_call(self):
        for agent in WORKERS:
            with self.subTest(agent=agent):
                text = body(agent)
                self.assertIn("--brief", text)
                self.assertRegex(
                    flat(text), r"(?i)one bash call",
                    f"{agent} must batch its reference reads",
                )


class BatchingIsMandatory(unittest.TestCase):
    """One call per turn is the shape that made a TSA take an hour."""

    def test_every_censys_agent_is_told_not_to_serialise_calls(self):
        for agent in [*ORCHESTRATORS, *WORKERS]:
            with self.subTest(agent=agent):
                self.assertRegex(
                    flat(body(agent)),
                    r"(?i)two independent Censys calls in consecutive turns",
                    f"{agent} is not told to batch independent calls",
                )

    def test_the_batching_tools_are_named_where_they_are_used(self):
        self.assertIn("tsa probe", body("censys-fingerprint"))
        self.assertIn("tsa candidates", body("censys-deepdive"))
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertIn("tsa batch", body(agent))

    def test_the_references_teach_the_batched_form_first(self):
        #  "not five" tracks the probe's call count: seed sample, three tag
        #  trees, and the decoded-protocol bucket.
        self.assertRegex(flat(reference("fingerprinting")), r"(?i)one call, not five")
        self.assertRegex(
            flat(reference("deep-dive")), r"(?i)test every candidate in one call"
        )


class EvidenceLayersAreNotJustHttp(unittest.TestCase):
    """The deep-dive family list must not be a partition of HTTP evidence only.

    Measured failure this guards: an ASA/FTD hunt spawned five family workers
    covering favicon, title, certificate, JARM, path, header, cookie, redirect
    and release evidence. Five of five are HTTP/TLS/certificate layers, so the
    fan-out was blind in the same direction five times and every worker missed
    `host.services.protocol="ANYCONNECT"` - whose `any_connect.groups` field was
    worth 1,661 hosts the published query did not have, ~1,500 of them untagged
    in all three trees. Breadth of families is not breadth of *layers*.
    """

    def test_both_orchestrators_offer_the_protocol_family(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertRegex(
                    flat(body(agent)),
                    r"(?i)structured protocol",
                    f"{agent} does not name the structured-protocol signal family",
                )

    def test_both_orchestrators_say_the_family_list_is_not_exhaustive(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertRegex(
                    flat(body(agent)),
                    r"(?i)starting set, not a partition of signal space",
                    f"{agent} presents the family list as complete",
                )

    def test_the_deepdive_worker_knows_the_family(self):
        self.assertRegex(flat(body("censys-deepdive")), r"(?i)host\.services\.protocol")

    def test_the_deep_dive_reference_puts_the_protocol_layer_before_content(self):
        text = flat(reference("deep-dive"))
        self.assertRegex(text, r"(?i)host\.services\.protocol")
        self.assertRegex(
            text,
            #  One leading (?i) only: Python 3.12 rejects a global flag that is
            #  not at the start of the pattern, which is the same trap CenQL has.
            #  Bold markers are left out so the assertion survives re-wording.
            r"(?i)(aggregating ports|a port aggregation) is not this check",
            "the reference does not warn that ports are not protocols",
        )

    def test_the_probe_covers_the_protocol_layer(self):
        """Step 1's own sweep, so no worker has to remember to ask."""
        self.assertRegex(flat(reference("fingerprinting")), r"(?i)host\.services\.protocol")


class ConvergentLeadsAreADirective(unittest.TestCase):
    """Three independent workers naming the same lead is the strongest routing
    signal a fan-out produces, because workers share no context.

    Measured failure this guards: on the ASA/FTD hunt, three of five deep-dive
    workers independently returned "the VPN control plane / IKE" as their top
    unexplored lead. The orchestrator merged all three into its notes, judged
    that no lead could still change the base query, and published. The layer they
    pointed at held 1,661 missing hosts.
    """

    def test_the_reference_states_the_rule(self):
        text = flat(reference("leads"))
        self.assertRegex(
            text,
            r"(?i)(three or more|3\+) workers is a directive",
            "leads.md does not make convergent leads a directive",
        )

    def test_it_outranks_the_cannot_change_the_query_test(self):
        """Otherwise the older rule silently wins, which is what happened."""
        self.assertRegex(
            flat(reference("leads")),
            r"(?i)outranks|overrides",
        )

    def test_both_orchestrators_carry_it(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertRegex(
                    flat(body(agent)),
                    r"(?i)(three or more|3\+) workers is a directive, not a note",
                    f"{agent} may drop a lead three workers agreed on",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
