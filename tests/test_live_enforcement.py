#!/usr/bin/env python3
"""Live plugin enforcement, exercised against real opencode agent runs.

OPT-IN. These spawn real agents and consume model tokens, so they are skipped
unless ``TSA_LIVE_TESTS=1`` is set. They consume **zero Censys credits**: every
prompt is shaped so the gated path throws before any Censys call executes, and
the one command that would cost credits is deliberately blocked by the budget.

They exist because the static tests cannot prove the thing that actually
matters - that a capability set on the orchestrator reaches a subagent running
in its own child session. That was the load-bearing assumption of the whole
design, and one earlier iteration passed every static check while hanging
forever in practice.

Run::

    TSA_LIVE_TESTS=1 python -m unittest tests.test_live_enforcement -v

Each case has a hard timeout. A hang is a failure, not a wait: an `ask`
permission inside a subagent never returns under `opencode run`, and the
timeout is what catches a regression to that state.
"""

from __future__ import annotations

import os
import unittest

from tests.helpers import BIN_TSA, opencode_available, run_agent

LIVE = os.environ.get("TSA_LIVE_TESTS") == "1"

ALL_OFF = (
    "webfetch=off websearch=off endpoint=off deepdive=never "
    "versionbreakdown=off reports=on budget=0"
)
WEB_ON = (
    "webfetch=on websearch=on endpoint=off deepdive=never "
    "versionbreakdown=off reports=on budget=0"
)

# A harmless, stable, non-assessed host. Principle six forbids contacting any
# host discovered in Censys; example.com is IANA's documentation domain and is
# never a TSA target.
PROBE = "https://example.com"


def probe_via_subagent(subagent: str) -> str:
    return (
        f"Invoke the {subagent} subagent via the task tool with exactly: "
        f"'Do no TSA work. Use webfetch on {PROBE} once, then reply with one "
        f"word: succeeded or blocked'. Report its one-word reply only."
    )


@unittest.skipUnless(LIVE, "set TSA_LIVE_TESTS=1 to run live agent tests")
@unittest.skipUnless(opencode_available(), "opencode is not on PATH")
class CapabilityEnforcement(unittest.TestCase):
    maxDiff = None

    def assert_blocked(self, output: str):
        self.assertIn(
            "blocked", output.lower(),
            f"expected the plugin to block the call.\n--- output ---\n{output[-1500:]}",
        )

    def assert_succeeded(self, output: str):
        lowered = output.lower()
        self.assertIn("succeeded", lowered, f"--- output ---\n{output[-1500:]}")
        self.assertNotIn("webfetch is disabled", lowered)

    # -- fail-closed defaults -------------------------------------------------

    def test_defaults_deny_web_with_no_capabilities_registered(self):
        """Fail-closed, in a session the plugin governs.

        Note the subagent hop: the gate is deliberately scoped to the censys-*
        agents, so a bare `build` session would - correctly - not be policed at
        all. See test_an_unrelated_agent_is_not_policed.
        """
        out = run_agent(probe_via_subagent("censys-fingerprint"), caps=None)
        self.assert_blocked(out)

    # -- the plugin is installed globally and must ignore everything else -----

    def test_an_unrelated_agent_is_not_policed(self):
        """THE most important test here.

        This plugin lives in ~/.config/opencode and its `tool.execute.before`
        hook fires for every tool call in every session on the machine, with
        fail-closed defaults. If it ever stops scoping itself to the censys-*
        agents, it silently breaks `webfetch` in every unrelated project the
        user opens - a far worse failure than anything it is guarding against.
        """
        out = run_agent(
            f"Use the webfetch tool on {PROBE} once, then reply with one word: "
            "succeeded or blocked.",
            agent="build",
            caps=None,
        )
        self.assertNotIn(
            "tsa-capabilities", out,
            "the TSA plugin policed a plain `build` session - it must only "
            "govern the censys-* agents",
        )
        self.assert_succeeded(out)

    def test_an_unrelated_agent_keeps_its_own_bash(self):
        """The budget gate must not count, or block, somebody else's commands."""
        out = run_agent(
            "Run exactly once: echo tsa assess pretend-query . "
            "Then reply with one word: ran or blocked.",
            agent="build",
            caps="budget=1",
        )
        self.assertNotIn("tsa-capabilities", out)
        self.assertIn("ran", out.lower(), f"--- output ---\n{out[-1500:]}")

    # -- propagation into subagent child sessions -----------------------------

    def test_denial_reaches_the_fingerprint_subagent(self):
        self.assert_blocked(
            run_agent(probe_via_subagent("censys-fingerprint"), caps=ALL_OFF)
        )

    def test_denial_reaches_the_deepdive_subagent(self):
        self.assert_blocked(
            run_agent(probe_via_subagent("censys-deepdive"), caps=ALL_OFF)
        )

    def test_grant_reaches_the_fingerprint_subagent(self):
        self.assert_succeeded(
            run_agent(probe_via_subagent("censys-fingerprint"), caps=WEB_ON)
        )

    def test_grant_reaches_the_deepdive_subagent(self):
        """Regression guard: this hung forever when the permission was `ask`."""
        self.assert_succeeded(
            run_agent(probe_via_subagent("censys-deepdive"), caps=WEB_ON)
        )

    # -- the capability tool --------------------------------------------------

    def test_capability_tool_is_registered(self):
        out = run_agent(
            "Call tsa_capabilities with action='get'. Reply with only its raw output."
        )
        self.assertIn("web research", out.lower(), f"--- output ---\n{out[-1500:]}")

    def test_env_var_is_honoured(self):
        out = run_agent(
            "Call tsa_capabilities action=get. Reply with only its raw output.",
            caps="webfetch=on websearch=off endpoint=off deepdive=always "
                 "versionbreakdown=on reports=off budget=42",
        )
        lowered = out.lower()
        self.assertIn("tsa_capabilities env", lowered, "env var was not picked up")
        self.assertIn("42", out, "budget did not round-trip")
        self.assertIn("always", lowered, "deepDive did not round-trip")

    def test_subagent_sees_the_orchestrators_capabilities(self):
        """Proves child-session -> root-session resolution, not a default fallback."""
        out = run_agent(
            "Step 1: call tsa_capabilities action=set with webfetch=true and "
            "callBudget=7. "
            "Step 2: invoke the general subagent via the task tool with exactly: "
            "'Call tsa_capabilities with action=get and report its raw output "
            "verbatim'. Report what the subagent said.",
        )
        self.assertIn("7", out, "the subagent did not see the orchestrator's budget")
        self.assertIn(
            "interview", out.lower(),
            "the subagent fell back to defaults instead of resolving to the root session",
        )

    # -- budget circuit-breaker ----------------------------------------------

    def test_budget_blocks_before_the_command_runs(self):
        """Costs zero credits: a TSA is priced at 2, so a budget of 1 blocks it."""
        out = run_agent(
            "Call tsa_capabilities action=set with callBudget=1. Then run exactly "
            f"once: {BIN_TSA} assess 'host.services.port=443' --product Test . "
            "Reply with one word: blocked or ran.",
        )
        self.assert_blocked(out)
        self.assertIn("budget", out.lower())

    # -- the plugin must not break unrelated work -----------------------------

    def test_free_tools_are_not_blocked(self):
        out = run_agent(
            f"Run exactly once: {BIN_TSA} report --template . "
            "Then reply with one word: ran or blocked.",
            caps=ALL_OFF,
        )
        self.assertIn("ran", out.lower(), f"--- output ---\n{out[-1500:]}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
