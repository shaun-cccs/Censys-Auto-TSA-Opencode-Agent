# Tests

Two suites. The fast one is static and runs in about a second; the live one
spawns real opencode agents.

```bash
tests/run.sh          # fast: no agent runs, no network, no Censys
tests/run.sh --live   # also exercises plugin enforcement against real agents
```

Standard library `unittest`, no third-party runner - the repo already uses it
(`utils/test_censys_credits.py`), and adding a dependency to run the tests
would be a poor trade for a project whose point is auditability.

## What each file covers

| File | Live? | Covers |
| --- | --- | --- |
| `test_carve_integrity.py` | no | `references/` is still a faithful copy of `SKILL.md` |
| `test_bin_tsa.py` | no | slugs, version-breakdown decisions, capability serialisation, prompt building, spec recovery, CLI |
| `test_agent_config.py` | no | agent frontmatter, resolved permissions, plugin source invariants, budget costs, the endpoint-probe gate |
| `test_live_enforcement.py` | **yes** | capabilities actually reaching subagents in their own child sessions |

## Why the live tests exist

Static checks cannot prove the load-bearing assumption of the whole design:
that a capability registered on the orchestrator reaches a subagent running in
a **separate child session**. An earlier iteration passed every static check
and still hung forever in practice, because an `ask` permission inside a
subagent never returns under `opencode run` - `--auto` does not reach subagent
sessions and there is no UI to prompt in.

That is why `test_grant_reaches_the_deepdive_subagent` exists and why every
live case has a hard timeout. **A hang is a failure, not a wait.**

### Cost

Live tests consume model tokens. They consume **zero Censys credits**, by
construction:

- Every web probe targets `example.com`, IANA's documentation domain, never an
  assessed host. Principle six forbids contacting anything discovered in
  Censys, and that applies to the test suite too.
- The only command that would spend credits (`censys_tsa.py`, priced at 2) is
  run under `callBudget=1`, so the plugin throws **before** execution. Verified:
  the thrown error names the budget, and no Censys response ever comes back.

A full live run takes roughly two minutes.

## Invariants worth knowing about

Some assertions look odd until you know what they are defending.

**No agent may use `ask` for `webfetch`/`websearch`.** It hangs a subagent under
`opencode run`. Static config stays permissive (`allow`) and the plugin's
`tool.execute.before` hook is the only gate. `test_no_agent_uses_ask_for_network_tools`
and `test_resolved_network_permissions_are_not_ask` both guard this - the
second checks what opencode actually *resolved*, which catches a rule that lost
to a higher-precedence one.

**Editing `references/` should fail the build.** `references/` is a verbatim
carve of `SKILL.md`; behavioural changes belong in agent prompts. If
`test_carve_integrity` fails after you edit a reference, the fix is usually to
revert that edit and move the change into a prompt. Lines may be exempted via
`DROPPED` or `KNOWN_REWRITES`, but each entry is a decision with a reason - and
`test_rewrite_list_has_no_dead_entries` deletes the bookkeeping when it goes
stale.

**Budget costs are tested as behaviour, not text.** The rules live in
TypeScript and cannot be imported, so `censys_cost_simulator()` parses them out
of the plugin and replays them in Python against real command strings. Asserting
on the source text instead was tried and was wrong: it matched prose in comments
as readily as real rules.

**The endpoint-probe regex is read from the plugin, not duplicated.** Six
phrasings must *not* match (they are legitimate questions) and three must. A
vaguer pattern would block real questions, which is a worse failure than
missing one.

**`versionBreakdown` is deliberately not enforced.** Unlike every other
capability, a version aggregation comes from `censys_aggregate.py` - the same
tool as all legitimate fingerprinting - so there is no signature to block on.
`test_version_breakdown_is_not_gated` asserts the *absence* of a gate so nobody
adds one that would also break steps 1, 2, 3 and 8.

## Adding a test

Live tests need `run_agent()` from `helpers.py`; give the prompt a shape whose
answer is one word, so the assertion does not depend on model phrasing. Anything
that can be checked without an agent belongs in the fast suite.
