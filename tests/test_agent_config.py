#!/usr/bin/env python3
"""Agent and plugin configuration invariants.

These guard the two failure modes that actually bit during development:

  1. An `ask` permission inside a SUBAGENT hangs forever under `opencode run`,
     because --auto does not reach subagent sessions and there is no UI to
     prompt in. This was measured, not assumed. Any agent that regains an
     `ask` on a tool it routinely uses will silently hang an unattended run.

  2. Enforcement lives entirely in the plugin's tool.execute.before hook. If
     an agent's static permission drifts to `deny`, the plugin can no longer
     grant that capability; if the plugin's gate is removed, nothing enforces
     anything.

Static frontmatter and opencode's *resolved* view are both checked. The
resolved view is what catches a rule that loses to a higher-precedence one.

Run::

    python -m unittest tests.test_agent_config -v
"""

from __future__ import annotations

import re
import unittest

from tests.helpers import (
    AGENTS,
    censys_cost_simulator,
    ORCHESTRATORS,
    PLUGIN_TS,
    SUBAGENTS,
    body,
    frontmatter,
    flat,
    opencode_available,
    resolved_permissions,
    ts_regex,
)

# Agents that may legitimately reach the network, gated by the plugin.
NETWORK_AGENTS = ["censys-tsa", "censys-tsa-auto", "censys-fingerprint", "censys-deepdive"]


class Frontmatter(unittest.TestCase):
    def test_every_agent_declares_the_basics(self):
        for agent in AGENTS:
            with self.subTest(agent=agent):
                fm = frontmatter(agent)
                self.assertIn("description", fm)
                self.assertIn("mode", fm)
                self.assertIn(fm["mode"], {"primary", "subagent", "all"})

    def test_modes_match_the_topology(self):
        for agent in ORCHESTRATORS:
            self.assertEqual(frontmatter(agent)["mode"], "primary", agent)
        for agent in SUBAGENTS:
            self.assertEqual(frontmatter(agent)["mode"], "subagent", agent)

    def test_no_agent_uses_ask_for_network_tools(self):
        """`ask` on webfetch/websearch hangs a subagent under `opencode run`."""
        for agent in AGENTS:
            perms = frontmatter(agent).get("permission", {}) or {}
            for tool in ("webfetch", "websearch"):
                with self.subTest(agent=agent, tool=tool):
                    self.assertNotEqual(
                        perms.get(tool), "ask",
                        f"{agent}.{tool} is 'ask'. Under `opencode run` --auto does "
                        "not reach subagent sessions, so this hangs forever. Use "
                        "'allow' and let the plugin gate it, or 'deny'.",
                    )

    def test_network_agents_are_allow_so_the_plugin_can_gate(self):
        for agent in NETWORK_AGENTS:
            perms = frontmatter(agent).get("permission", {}) or {}
            for tool in ("webfetch", "websearch"):
                with self.subTest(agent=agent, tool=tool):
                    self.assertEqual(
                        perms.get(tool), "allow",
                        f"{agent}.{tool} must be 'allow'; the plugin is the gate. "
                        "'deny' would make a granted capability unusable.",
                    )

    def test_report_agent_is_off_the_network_entirely(self):
        perms = frontmatter("censys-report").get("permission", {}) or {}
        self.assertEqual(perms.get("webfetch"), "deny")
        self.assertEqual(perms.get("websearch"), "deny")

    def test_report_agent_bash_is_restricted_to_the_renderer(self):
        """This agent renders a file. It gets the renderer and nothing else.

        The patterns must also be interpreter-free: an allowlist naming
        `python` (as this one used to) denies itself on any machine where the
        binary is called something else, which is most of them.
        """
        bash = (frontmatter("censys-report").get("permission", {}) or {}).get("bash")
        self.assertIsInstance(bash, dict, "censys-report bash must be a pattern map")
        self.assertEqual(bash.get("*"), "deny", "must deny by default")
        allowed = [k for k, v in bash.items() if v == "allow"]
        self.assertTrue(allowed, "must allow the renderer")
        self.assertIn("tsa report*", allowed, "must be able to render a report")
        for pattern in allowed:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.startswith("tsa "),
                    f"{pattern!r} must invoke the kit's own command",
                )
                for word in ("python", "pip", "utils/", "/"):
                    self.assertNotIn(
                        word, pattern,
                        f"{pattern!r} must not name an interpreter or a path",
                    )

    def test_unattended_agents_cannot_ask_questions(self):
        """No UI exists under `opencode run`; a question there would hang."""
        for agent in ["censys-tsa-auto", "censys-deepdive", "censys-report"]:
            with self.subTest(agent=agent):
                perms = frontmatter(agent).get("permission", {}) or {}
                self.assertEqual(perms.get("question"), "deny")

    def test_only_the_interactive_orchestrator_asks(self):
        self.assertEqual(
            (frontmatter("censys-tsa").get("permission", {}) or {}).get("question"),
            "allow",
        )

    def test_task_delegation_is_scoped(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                task = (frontmatter(agent).get("permission", {}) or {}).get("task")
                self.assertIsInstance(task, dict)
                self.assertEqual(task.get("*"), "deny", "must deny by default")
                for name in task:
                    if name != "*":
                        self.assertIn(name, AGENTS, f"unknown subagent {name!r}")

    def test_subagents_cannot_spawn_subagents(self):
        for agent in SUBAGENTS:
            with self.subTest(agent=agent):
                self.assertEqual(
                    (frontmatter(agent).get("permission", {}) or {}).get("task"), "deny"
                )

    def test_deep_dive_is_reachable_from_both_orchestrators(self):
        """--deep-dive on the unattended path needs the delegation to exist."""
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                task = (frontmatter(agent).get("permission", {}) or {}).get("task", {})
                self.assertEqual(task.get("censys-deepdive"), "allow")

    def test_the_canonical_skill_is_suppressed(self):
        """Agents must use references/, not fall back to the original skill."""
        for agent in AGENTS:
            with self.subTest(agent=agent):
                self.assertEqual(
                    (frontmatter(agent).get("permission", {}) or {}).get("skill"), "deny"
                )


class Prompts(unittest.TestCase):
    def test_orchestrators_check_the_plugin_loaded(self):
        """The plugin is the only gate; if it is missing, nothing is enforced."""
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                self.assertIn("tsa_capabilities", body(agent))
                self.assertRegex(
                    body(agent),
                    r"(?i)if the `tsa_capabilities` tool does not exist",
                    f"{agent} must fail loudly when the plugin has not loaded",
                )

    def test_interactive_orchestrator_runs_the_interview(self):
        text = body("censys-tsa")
        self.assertIn("Step -1", text)
        for topic in ["Web research", "Version breakdown", "Credit budget",
                      "Report output", "Deep dive"]:
            with self.subTest(topic=topic):
                self.assertIn(topic, text)

    def test_slim_terminal_report_is_specified(self):
        for agent in ORCHESTRATORS:
            with self.subTest(agent=agent):
                text = body(agent)
                self.assertIn("Baseline query", text)
                self.assertIn("Widened query", text)
                self.assertIn("Caveats", text)

    def test_interview_offers_all_three_report_options(self):
        """Files only, summary only, or both."""
        text = flat(body("censys-tsa"))
        self.assertRegex(text, r"(?i)yes, write the files")
        self.assertRegex(text, r"(?i)no, just the summary")
        self.assertRegex(text, r"(?i)both - write the files and show me the spec")

    def test_write_and_print_are_independent_switches(self):
        text = flat(body("censys-tsa"))
        self.assertIn("printSpec", text)
        self.assertRegex(
            text, r"(?i)summary is printed in all four combinations",
            "the summary must survive every combination of the two switches",
        )

    def test_summary_is_printed_even_when_no_file_is_written(self):
        """writeReports controls the FILE, not the terminal format.

        An earlier version told the interactive orchestrator to dump raw spec
        JSON into the chat when report writing was off. Nothing reads JSON in a
        chat, and it buried the counts the user actually asked for.
        """
        text = flat(body("censys-tsa"))
        self.assertRegex(
            text, r"(?i)do not volunteer a raw json dump",
            "censys-tsa must not dump JSON unless printSpec was requested",
        )
        self.assertRegex(
            text, r"(?i)omit the `Full report:` line",
            "the no-file path should just drop the report line from the summary",
        )

    def test_unattended_path_appends_json_without_replacing_the_summary(self):
        """`tsa run` needs the JSON to parse, but a human still reads the summary."""
        text = flat(body("censys-tsa-auto"))
        self.assertRegex(
            text, r"(?i)never let the JSON replace the summary",
            "the spec JSON must accompany the summary, not replace it",
        )
        self.assertRegex(
            text, r"(?i)in addition to the summary, never instead of it"
        )

    def test_fingerprint_keeps_cve_version_scoping_mandatory(self):
        """The gate covers the distribution table, never the scoping."""
        text = body("censys-fingerprint")
        self.assertIn("versionBreakdown", text)
        self.assertRegex(text, r"(?i)version SCOPING, which is never optional")

    def test_agents_state_that_version_breakdown_is_not_enforced(self):
        self.assertRegex(body("censys-fingerprint"), r"(?i)not plugin-enforced")

    def test_subagents_are_told_the_safety_principles(self):
        """Subagents inherit no context, so principles 6 and 7 must be restated."""
        for agent in ["censys-fingerprint", "censys-deepdive"]:
            with self.subTest(agent=agent):
                self.assertRegex(
                    body(agent), r"(?i)never (send any network request to|contact)"
                )

    def test_subagents_define_a_return_contract(self):
        for agent in ["censys-fingerprint", "censys-deepdive"]:
            with self.subTest(agent=agent):
                self.assertIn("Return contract", body(agent))


class Plugin(unittest.TestCase):
    def setUp(self):
        self.source = PLUGIN_TS.read_text()

    def test_enforcement_hook_exists(self):
        self.assertIn('"tool.execute.before"', self.source)

    def test_permission_ask_hook_is_absent(self):
        """It can never fire with `allow` everywhere; keeping it would mislead."""
        self.assertNotIn(
            '"permission.ask": async', self.source,
            "permission.ask is dead code under the current design",
        )

    def test_defaults_are_fail_closed(self):
        defaults = re.search(r"const DEFAULTS: Caps = \{(.*?)\}", self.source, re.S).group(1)
        for field in ("webfetch", "websearch", "endpointValidation", "versionBreakdown"):
            with self.subTest(field=field):
                self.assertRegex(defaults, rf"{field}:\s*false")

    def test_network_tools_are_gated(self):
        for tool in ("webfetch", "websearch"):
            with self.subTest(tool=tool):
                self.assertRegex(
                    self.source,
                    rf'input\.tool === "{tool}" && !caps\.{tool}',
                    f"{tool} is no longer gated",
                )

    def test_child_sessions_resolve_to_their_root(self):
        """Capabilities set on the orchestrator must reach every subagent."""
        self.assertIn("parentID", self.source)

    def test_version_breakdown_is_documented_as_advisory(self):
        self.assertRegex(self.source, r"(?i)advisory")

    def test_version_breakdown_is_not_gated(self):
        """It cannot be: the aggregation is indistinguishable from any other."""
        self.assertNotRegex(
            self.source, r'input\.tool === "\w+" && !caps\.versionBreakdown'
        )


class BudgetCosts(unittest.TestCase):
    """The credit circuit-breaker, exercised as behaviour rather than as text.

    The rules are parsed out of the plugin and replayed in Python, so these
    assert what a real command would actually cost. Costs are deliberate
    over-estimates: their job is to stop a runaway loop, not to be an
    accountant. The orchestrator measures true spend separately.
    """

    @classmethod
    def setUpClass(cls):
        # staticmethod, or Python binds it as a method and passes the TestCase
        # in as the first argument.
        cls.cost = staticmethod(censys_cost_simulator())

    def test_non_censys_commands_are_free(self):
        for command in ["ls -la", "grep -n foo docs/x.md", "python -c 'print(1)'", ""]:
            with self.subTest(command=command):
                self.assertEqual(self.cost(command), 0)

    def test_free_censys_tools_cost_nothing(self):
        """cve_lookup, censys_credits and tsa_report never call the Censys API."""
        for command in [
            "python utils/cve_lookup.py CVE-2024-21762",
            "python utils/censys_credits.py balance",
            "python utils/tsa_report.py reports/x.spec.json -o reports/x.md",
        ]:
            with self.subTest(command=command):
                self.assertEqual(self.cost(command), 0)

    def test_a_search_costs_one(self):
        self.assertEqual(self.cost("python utils/censys_query.py 'x' -n 5"), 1)

    def test_a_tsa_costs_two(self):
        """Two counts: global and country."""
        self.assertEqual(self.cost("python utils/censys_tsa.py 'x' --product Y"), 2)

    def test_a_plain_aggregation_costs_one(self):
        self.assertEqual(
            self.cost("python utils/censys_aggregate.py host.services.port 'x'"), 1
        )

    def test_suggest_fields_is_priced_far_above_one(self):
        """It issues one request per field, so charging 1 would under-count badly."""
        cost = self.cost("python utils/censys_aggregate.py --suggest-fields 'x'")
        self.assertGreater(cost, 1)
        self.assertGreaterEqual(cost, 10, "should reflect a sweep, not a single call")

    def test_compare_levels_costs_double(self):
        plain = self.cost("python utils/censys_aggregate.py f 'x'")
        compared = self.cost("python utils/censys_aggregate.py f 'x' --compare-levels")
        self.assertEqual(compared, plain * 2)

    def test_every_metered_command_is_positive(self):
        for script in ("censys_query", "censys_aggregate", "censys_tsa"):
            with self.subTest(script=script):
                self.assertGreater(
                    self.cost(f"python utils/{script}.py 'x'"), 0,
                    f"{script}.py costs credits and must be metered",
                )


class EndpointProbeGate(unittest.TestCase):
    """The plugin blocks the step-0b probe request when it was not authorised.

    The pattern is read from the TypeScript source rather than duplicated, so
    editing the plugin changes what these cases are checked against.

    These cases are full `question` tool payloads, not bare sentences. That
    distinction is the entire point: the plugin sees `JSON.stringify` of the
    whole payload - header, option labels and descriptions included. An earlier
    version of this test checked only the question sentence, passed, and shipped
    a gate that blocked the startup interview's own "User-operated endpoint
    validation" question. Match tools, not talk.
    """

    def payload(self, header: str, question: str, *options: str) -> str:
        import json

        return json.dumps({
            "questions": [{
                "header": header,
                "question": question,
                "options": [{"label": o, "description": o} for o in options],
            }]
        }).lower()

    def setUp(self):
        self.pattern = re.compile(ts_regex("endpoint_probe"))

    def assert_allowed(self, text: str, why: str):
        self.assertIsNone(
            self.pattern.search(text),
            f"gate would wrongly block: {why}",
        )

    def assert_blocked(self, text: str, why: str):
        self.assertIsNotNone(self.pattern.search(text), f"gate failed to block: {why}")

    def test_the_startup_interview_is_not_blocked(self):
        """The regression that shipped: the gate blocked its own config question."""
        self.assert_allowed(
            self.payload(
                "User-operated endpoint validation",
                "If a version can only be confirmed by requesting an endpoint, may I "
                "ask you to run that request yourself against a host you own?",
                "No (Recommended)",
                "Yes, I may be asked. You would run the request and paste the response back.",
            ),
            "the interview question that configures this very capability",
        )

    def test_other_interview_questions_are_not_blocked(self):
        for header, question in [
            ("Web research", "May I use web research if Censys alone can't identify the product?"),
            ("Deep dive", "Should I run the deeper signature hunt?"),
            ("Credit budget", "Cap the Censys credits for this run?"),
            ("Version breakdown", "Break the exposed population down by version?"),
            ("Write report files", "Write reports/<slug>.spec.json and .md at the end?"),
        ]:
            with self.subTest(header=header):
                self.assert_allowed(self.payload(header, question, "Yes", "No"), header)

    def test_ordinary_questions_are_not_blocked(self):
        for question in [
            "Should I run the request for the Canada count as well?",
            "Which country should the second count use?",
            "Shall I paste the response into the report?",
        ]:
            with self.subTest(question=question[:40]):
                self.assert_allowed(self.payload("Question", question, "Yes"), question)

    def test_a_real_probe_instruction_is_blocked(self):
        for question in [
            "Please run: curl --include --max-time 10 https://1.2.3.4/status and paste the output back.",
            "Run `curl -sSI https://your-host/version` and paste what comes back.",
            "Use wget -S https://your-appliance/api/version and share the headers.",
        ]:
            with self.subTest(question=question[:40]):
                self.assert_blocked(
                    self.payload("Version check", question, "OK"), question
                )


class InterviewIsNotSelfBlocking(unittest.TestCase):
    """The interview runs before capabilities exist, so it must not be gated.

    Belt and braces alongside the narrowed regex: even if a future pattern
    over-matches, the gate is inert until `tsa_capabilities action=set` has run.
    """

    def setUp(self):
        self.source = PLUGIN_TS.read_text()

    def test_caps_track_whether_registration_happened(self):
        self.assertRegex(self.source, r"registered:\s*boolean")
        self.assertRegex(self.source, r"registered:\s*false", "defaults must be unregistered")

    def test_the_question_gate_requires_registration(self):
        self.assertRegex(
            self.source,
            r'input\.tool === "question" && caps\.registered',
            "the question gate must be inert before capabilities are registered, "
            "or it blocks the interview that sets them",
        )

    def test_setting_capabilities_marks_them_registered(self):
        self.assertRegex(self.source, r"caps\.registered = true")

    def test_the_env_var_counts_as_registration(self):
        """`tsa run` already made the choices; the unattended path has no interview."""
        self.assertRegex(self.source, r'TSA_CAPABILITIES env",\s*registered: true')


class ResolvedByOpencode(unittest.TestCase):
    """What opencode actually computed, not merely what we declared."""

    @classmethod
    def setUpClass(cls):
        if not opencode_available():
            raise unittest.SkipTest("opencode is not on PATH")
        cls.perms = resolved_permissions()

    def test_all_agents_load(self):
        for agent in AGENTS:
            with self.subTest(agent=agent):
                self.assertIn(agent, self.perms, f"{agent} failed to load")

    def test_resolved_network_permissions_are_not_ask(self):
        for agent in AGENTS:
            for tool in ("webfetch", "websearch"):
                with self.subTest(agent=agent, tool=tool):
                    self.assertNotEqual(
                        self.perms[agent].get(tool), "ask",
                        f"{agent}.{tool} resolved to 'ask' and will hang a subagent run",
                    )

    def test_resolved_skill_permission_suppresses_the_canonical_skill(self):
        for agent in AGENTS:
            with self.subTest(agent=agent):
                self.assertEqual(self.perms[agent].get("skill"), "deny")


if __name__ == "__main__":
    unittest.main(verbosity=2)
