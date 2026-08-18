# Tests

Two suites. The fast one is static and runs in about a second; the live one
spawns real opencode agents.

```bash
tests/run.sh          # fast: no agent runs, no network, no Censys
tests/run.sh --live   # also exercises plugin enforcement against real agents
```

Standard library `unittest`, no third-party runner - adding a dependency to run
the tests would be a poor trade for a project whose point is auditability.

`run.sh` prefers `uv run` so the suite gets the kit's locked environment, which
is what lets `test_censys_credits.py` import the utils instead of skipping. With
no uv it falls back to `python3` and the static checks still run. It never calls
bare `python`, which does not exist on many machines - the reason this kit is
packaged the way it is.

## What each file covers

| File | Live? | Covers |
| --- | --- | --- |
| `test_portability.py` | no | no paths or interpreters in shipped prose, principles in sync, plugin scope, the `tsa` dispatch table, `tsa ref`/`tsa doc` coverage, the skill, `install.sh` against a throwaway HOME |
| `test_tsa_run.py` | no | slugs, version-breakdown decisions, capability serialisation, prompt building, spec recovery, CLI |
| `test_agent_config.py` | no | agent frontmatter, resolved permissions, who may write files, plugin source invariants, budget costs, the endpoint-probe gate |
| `test_speed.py` | no | the speed subsystem: call timing (`tsa timeline`), where instrumentation sits, the batching engine, rate-limit profiles, ledger locking |
| `test_fanout.py` | no | the fan-out topology: the lead protocol, call caps, the `STATUS:` completion signal, "never sleep", quick cards |
| `test_censys_credits.py` | no | credit tracking maths (skips without the SDK) |
| `test_carve_integrity.py` | no | **opt-in**: what a change to the upstream skill did or did not carry over. Set `TSA_SKILL_MD`; skips otherwise |
| `test_live_enforcement.py` | **yes** | capabilities actually reaching subagents in their own child sessions, the plugin leaving other agents alone, and that parallel task calls really do overlap |

## Why the live tests exist

Static checks cannot prove the two load-bearing assumptions of the design.

The first is that a capability registered on the orchestrator reaches a subagent
running in a **separate child session**. An earlier iteration passed every static
check and still hung forever in practice, because an `ask` permission inside a
subagent never returns under `opencode run` - `--auto` does not reach subagent
sessions and there is no UI to prompt in.

The second is that **two task calls issued in one message actually overlap**. If
they did not, fanning discovery out across four workers would be pure overhead
instead of the main speed win. `ParallelSubagentsOverlap` measures it with two
sleeping workers; a failure invalidates the topology in `tsa ref leads`, so
verify it by hand before concluding anything - it can also mean the runtime
changed or the model issued the calls one per message.

That is why `test_grant_reaches_the_deepdive_subagent` exists and why every
live case has a hard timeout. **A hang is a failure, not a wait.**

### Cost

Live tests consume model tokens. They consume **zero Censys credits**, by
construction:

- Every web probe targets `example.com`, IANA's documentation domain, never an
  assessed host. Principle six forbids contacting anything discovered in
  Censys, and that applies to the test suite too.
- The only command that would spend credits (`tsa assess`, priced at 2) is run
  under `callBudget=1`, so the plugin throws **before** execution. Verified:
  the thrown error names the budget, and no Censys response ever comes back.
- The concurrency check runs `sleep`, which costs nothing anywhere.

A full live run takes roughly three minutes.

## Invariants worth knowing about

Some assertions look odd until you know what they are defending.

**No agent may use `ask` for `webfetch`/`websearch`.** It hangs a subagent under
`opencode run`. Static config stays permissive (`allow`) and the plugin's
`tool.execute.before` hook is the only gate. `test_no_agent_uses_ask_for_network_tools`
and `test_resolved_network_permissions_are_not_ask` both guard this - the
second checks what opencode actually *resolved*, which catches a rule that lost
to a higher-precedence one.

**`references/` is canonical for this kit.** It began as a verbatim carve of the
upstream `SKILL.md`, and `test_carve_integrity` still compares the two - but only
when `TSA_SKILL_MD` points at a copy, and with a large `KNOWN_REWRITES` list,
because packaging rewrote every path and every invocation. Behavioural changes
now belong in `references/` or in a prompt, whichever the change is actually
about.

**No shipped prose may contain a path or an interpreter.** `test_portability.py`
enforces it line by line across the agents, the references and the skill. The
agents run in *someone else's* project: a relative path resolves against the
wrong directory, an absolute path freezes the install location, and `python` is
frequently not a command at all. `tsa ref` and `tsa doc` exist so that even
reading this kit's own documentation needs no path. HTML comments are exempt -
they address whoever edits the file, not the model.

**The capability plugin must leave other agents alone.** It is installed
globally, its `tool.execute.before` hook fires for every tool call in every
session on the machine, and its defaults are fail-closed - so an unscoped
version blocks `webfetch` in every unrelated project the user opens. The hook is
not told which agent it belongs to, so the plugin learns that from
`chat.message`/`chat.params`. `test_portability.PluginScope` checks the gate is
in place and that `TSA_AGENTS` matches the agents on disk; the live suite proves
a non-TSA agent is unaffected. **That live test is the most important one here.**

**Budget costs are tested as behaviour, not text.** The rules live in
TypeScript and cannot be imported, so `censys_cost_simulator()` parses them out
of the plugin and replays them in Python against real command strings. Asserting
on the source text instead was tried and was wrong: it matched prose in comments
as readily as real rules. The parser reads **one regex per rule** - if you join
two `.test()` calls with `||` in `censysCost`, it silently misparses and every
command costs whatever the last `return` said.

**The endpoint-probe regex is read from the plugin, not duplicated.** Six
phrasings must *not* match (they are legitimate questions) and three must. A
vaguer pattern would block real questions, which is a worse failure than
missing one.

**`versionBreakdown` is deliberately not enforced.** Unlike every other
capability, a version aggregation comes from `tsa agg` - the same command as all
legitimate fingerprinting - so there is no signature to block on.
`test_version_breakdown_is_not_gated` asserts the *absence* of a gate so nobody
adds one that would also break steps 1, 2, 3 and 8.

**Nothing may sleep, poll or wait.** Nothing in this workflow runs in the
background - a `task` call blocks until its worker returns and a `bash` call until
the command exits - so a wait cannot let anything finish, and inside a subagent it
is invisible dead time. Agents were observed doing it, and the reference prose
used to tell them to. `test_fanout.NobodyWaits` checks every prompt and every
reference; `Profiles.test_the_budget_error_tells_the_agent_not_to_wait` checks the
error message that used to invite it.

**Every worker ends with a `STATUS:` line.** "Is this subagent finished" must be
signalled, not inferred from the shape of a message.
`test_fanout.CompletionIsSignalled` checks the marker exists, is spelled the same
way in every agent, is documented as the last line, and can distinguish blocked
from finished.

**A quick card is not optional once a prompt asks for one.** `tsa ref x --brief`
falls back to printing the whole reference, which is safe but silently costs the
saving. `test_every_reference_an_agent_is_told_to_read_briefly_has_a_card` catches
a prompt asking for a card that was never written.

## Adding a test

Live tests need `run_agent()` from `helpers.py`; give the prompt a shape whose
answer is one word, so the assertion does not depend on model phrasing. Anything
that can be checked without an agent belongs in the fast suite.
