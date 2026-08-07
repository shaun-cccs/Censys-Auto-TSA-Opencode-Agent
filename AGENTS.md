# Censys TSA - contributor guide

Turn a product, vendor, appliance, or CVE into a Censys Platform query plus a
Threat Surface Assessment (TSA): a global exposed-host count and a country-scoped
count, both excluding honeypots.

This repository is **an installable kit**, not a working directory. It is cloned
once and linked into `~/.config/opencode` by `./install.sh`; from then on its
five agents are available in every project on the machine, and every script is
reached through one command, `tsa`, which finds its own installation. Users never
`cd` here.

`README.md` is the user-facing document. This file is for people changing the
kit.

## Layout

| Path | What it is |
| --- | --- |
| `.opencode/agent/censys-*.md` | the five agents. Symlinked into `~/.config/opencode/agent/` by install.sh |
| `.opencode/plugin/tsa-capabilities.ts` | capability negotiation and enforcement. Symlinked into `~/.config/opencode/plugin/` |
| `.opencode/skill/censys-tsa/SKILL.md` | discovery skill: teaches a user's own agent to hand off to `@censys-tsa` |
| `bin/tsa` | the single entrypoint. POSIX sh, self-locating, symlinked onto PATH |
| `utils/*.py` | the actual tools. Flat scripts, never imported as a package |
| `references/*.md` | the workflow prose the agents read via `tsa ref <name>` |
| `references/principles.md` | **source of truth** for the seven principles |
| `docs/` | CenQL and queryable-field documentation, read via `tsa doc <name>` |
| `scripts/gen_agents.py` | splices `principles.md` into all five agent prompts |
| `scripts/parse_definitions.py` | maintainer-only: regenerates `docs/queryable_fields/` from saved Censys HTML |
| `install.sh` | link (or copy) everything into place; also `tsa doctor` |
| `pyproject.toml`, `uv.lock` | the Python environment, managed by uv |

`./reports/` is where a *run* writes, in whatever directory the user invoked it
from - which for a contributor is this repo. It is gitignored: assessments are a
user's output, not part of the kit.

## Absolute rules for anything user-facing

1. **No filesystem paths in agent prompts or references.** Not relative, not
   absolute, not `~/`. The agents run inside someone else's project, so a
   relative path is wrong and an absolute path freezes the install location.
   Everything goes through `tsa` subcommands - including reading this kit's own
   documentation, which is what `tsa ref` and `tsa doc` are for. Tests enforce
   this.
2. **No `python`, no `pip`.** There is no `python` on many machines, and `pip
   install` would hit the wrong interpreter. `bin/tsa` decides how to run things:
   uv for the Censys SDK subcommands, bare `python3` for the standard-library
   ones.
3. **The principles are generated, not written.** Edit `references/principles.md`
   and run `python scripts/gen_agents.py`. Never edit the block inside an agent
   file.
4. **Never set `webfetch`/`websearch` to `ask`** in agent frontmatter. An `ask`
   inside a subagent hangs forever under `opencode run`, because `--auto` does not
   reach subagent sessions and there is no UI to prompt in. Use `allow` and let
   the plugin be the gate.

## The seven principles

They live in `references/principles.md`, are spliced into every agent prompt, and
bind every agent in every step. Read them there - `tsa ref principles` prints
them. They are not repeated here, because a second copy is a copy that drifts.

## Python and uv

`pyproject.toml` deliberately has **no `[build-system]`**, which makes it a
*virtual* project: `uv sync` installs the dependencies into `.venv` and does not
install this directory as a package. That is what keeps `utils/*.py` ordinary
scripts whose flat sibling imports (`from censys_query import ...`) work. Adding
a build backend would break them.

`bin/tsa` runs SDK subcommands as `uv run --project <kit> python <kit>/utils/x.py`
- `--project`, never `--directory`, because `--directory` would chdir and
silently break relative output paths like `-o reports/foo.md`. Warm dispatch
costs about 30 ms.

`CENSYS_TSA_PYTHON` bypasses uv entirely for air-gapped installs.

## Installation, and the one sharp edge

`install.sh` symlinks; nothing is copied by default, so `git pull` updates
agents, prompts, references and plugin in one step. It edits no `opencode.json`:
verified against opencode 1.18.14, the config directory is globbed for
`{plugin,plugins}/*.{ts,js}` with symlinks followed.

The sharp edge is plugin module resolution. `tsa-capabilities.ts` imports
`@opencode-ai/plugin`, which opencode installs into its own config directory -
but resolution starts from the plugin's **real** path, not the symlink. Measured:

- real path inside `~/.config/opencode` → resolves, plugin loads
- real path outside it → **silently loads as nothing, and enforces nothing**

So `install.sh` bridges the gap with a `node_modules` symlink at the kit root
when the kit lives elsewhere, and `tsa doctor` checks the resolution chain
explicitly. If you touch the plugin's imports, re-read that part of `install.sh`.

## Capabilities

Network access, endpoint validation, the deep dive, report writing and the
credit budget are **negotiated once at the start of a run and then enforced by a
plugin** (`.opencode/plugin/tsa-capabilities.ts`) across every subagent.

- `censys-tsa` interviews the user (step -1) and records the answers with the
  `tsa_capabilities` tool.
- `censys-tsa-auto` takes them from the `TSA_CAPABILITIES` env var, which
  `tsa run` populates from its flags. No interview.
- **Any agent can call `tsa_capabilities` with `action: "get"`** to learn what it
  is permitted to do. Do this before planning work that might be blocked.

Capabilities are **not advisory**. The plugin throws on a disallowed call, so a
blocked tool is a hard failure, not a suggestion. Treat such an error as final:
do not retry, record the limitation in `caveats`, and continue with the evidence
you can legitimately obtain.

Defaults are **fail-closed** - no web research, no endpoint validation. A run
that never registers capabilities cannot silently reach the network.

Why a plugin at all: opencode resolves agent permissions statically at load
time, and the Task tool takes only a prompt, so an orchestrator cannot grant a
tool to a subagent at invocation time. The plugin supplies that missing runtime
layer, keying capabilities by root session and resolving each subagent's child
session back to it via `Session.parentID`.

**It is installed globally, so it must stay out of the way.** `tool.execute.before`
fires for every tool call in every session on the machine, and the defaults are
fail-closed - enforcing unconditionally would block `webfetch` in every unrelated
project the user opens. The hook is not told which agent it belongs to, so the
plugin learns that from `chat.message`/`chat.params` (which are) and only polices
sessions whose agent is one of the five. Everything else returns immediately. If
you change the agent set, change `TSA_AGENTS` in the plugin; a test checks they
match.

Three further design points:

- Every agent that may reach the network has `webfetch`/`websearch` set to
  `allow` in its frontmatter, and the plugin is the only gate - see rule 4 above.
  `censys-report` is the exception: denied outright, since it renders files and
  has no business on the network at all.
- Because the plugin is the only gate, **a plugin that fails to load enforces
  nothing**. The orchestrators therefore call `tsa_capabilities` as their first
  action: if that tool is missing the run fails loudly rather than proceeding
  with the network wide open. `tsa doctor` is the out-of-band check.
- The credit budget is a **coarse circuit-breaker, not an accountant**. Real
  spend is still measured with `tsa credits`. See the plugin header for why
  command-line cost estimation cannot be exact.

**Version breakdown is off by default.** A plain product TSA does not produce a
per-version distribution table - those cost an aggregation each and dominate the
report. It turns on when the user asks, when the target names a version
(`LobeChat 1.123.1`), or when the target is a CVE. This gates only the
distribution *table*: version **scoping** for a CVE remains mandatory, because
that is what makes the count correct.

Unlike every other capability here, `versionBreakdown` is **advisory, not
enforced**. A version aggregation is produced by `tsa agg`, the same command used
for all legitimate fingerprinting, so the plugin has no signature to block on.
Honour it as an instruction; do not assume something will stop you.

Web research is a **corroboration tool, not a discovery tool**. In
`censys-fingerprint` it is the documented last resort (step 3b) after Censys has
failed to identify the product; in `censys-deepdive` it exists to verify that a
harvested signal means what you think it means. Neither may use it to *find*
signals, and principle six is never relaxed by it: research means vendor sites,
repositories, advisories and registries - never the assessed hosts.

## Tests

```bash
tests/run.sh          # fast: static checks, no agent runs, no Censys
tests/run.sh --live   # also exercises plugin enforcement against real agents
```

Run the fast suite after changing an agent prompt, the plugin, `bin/tsa`,
`install.sh` or `utils/tsa_run.py`. Run `--live` after changing anything about
capability enforcement or the plugin's session scoping - that suite contains the
one test that catches the worst regression this kit can have, namely the plugin
blocking tools for agents that are none of its business. See `tests/README.md`.

## Two report surfaces

They are not the same thing and must not be conflated.

- **The terminal report (step 7)** is deliberately compact. Product and a
  one-or-two-line summary, the baseline query with its global and country
  counts, the widened query and delta if a deep dive ran, one line of basis and
  credits, then at most four one-line caveats. Never print the honeypot or
  country query variants, and never print a platform URL.
- **The written report (`reports/<slug>.md`, step 9)** stays comprehensive. It
  is the durable artifact and carries the full rationale, every query variant,
  the credit table, all caveats and sources.

The seven-item skeleton in `tsa ref counting-and-report` describes what
must be **known** and what goes in the file. It is not the print format.

## Agent topology

```
censys-tsa  (primary, interactive)          censys-tsa-auto  (primary, non-interactive)
  |  owns steps 4,5,6,7 + all user gates      |  same graph, question+webfetch denied
  |  assembles the report spec                |  skips 3b, endpoint validation, step 8
  |
  +-> censys-fingerprint  (subagent)  steps 0, 0b, 1, 2, 3, 3b
  +-> censys-deepdive     (subagent)  step 8a-8e   [only after the user accepts]
  +-> censys-report       (subagent)  step 9        [writes reports/<slug>.spec.json + .md]
```

The orchestrator is a **spec assembler**. Each subagent returns the fragment of
`reports/<slug>.spec.json` that it owns; the orchestrator merges them and hands
the merged spec to `censys-report`. The spec schema is defined by
`tsa report --template`.

| Spec key | Produced by |
| --- | --- |
| `product`, `vendor`, `summary`, `basis`, `rationale`, `sources`, `caveats` | `censys-fingerprint` |
| `baseline.query` | `censys-fingerprint` |
| `extra_assessments` | `censys-fingerprint` (step 0b version-scoped sub-counts) |
| `baseline.counts`, `country`, `cve`, `date`, `credits` | `censys-tsa` orchestrator |
| `deep_dive` | `censys-deepdive` |
| the files on disk | `censys-report` |

## Step routing

| Step | Reference |
| --- | --- |
| the seven principles (already in every prompt) | `tsa ref principles` |
| tools, prerequisites, rate limits, credentials | `tsa ref workspace` |
| 0 - CVE intake; 0b - version derivation, for **any** named version, CVE or not | `tsa ref cve-workflow` |
| 1, 2, 3, 3b - probe, tagging, fingerprinting, web research | `tsa ref fingerprinting` |
| aggregation semantics (the two knobs, bucket levels, aliases, HONEYPOT) | `tsa ref aggregation-semantics` |
| 4 - CenQL query-drafting rules | `tsa ref cenql-rules` |
| 5, 6, 7 - validate, run the TSA, report | `tsa ref counting-and-report` |
| 8 - the deeper hunt | `tsa ref deep-dive` |
| 9 - persist the investigation | `tsa ref report-spec` |
| credit costs and measurement | `tsa ref credits` |
| worked examples (load on demand) | `tsa ref examples` |

## Conventions

- **Never estimate credits.** Measure with `tsa credits`, per `tsa ref credits`.
- **Counts always come from `host.*` queries.** `web.*` and `cert.*` are pivots.
- **Do not hand-add honeypot or country clauses.** `tsa assess` appends
  `not labels: "HONEYPOT"` and `host.location.country=...` itself.
- **Only the base query goes in the spec.** The renderer derives the honeypot and
  country variants and the platform URLs. Never paste a URL into a spec.
- **The rate-limit budget is shared across subagents** via
  `~/.censys_query_rate_state.json`. Budget burned by one subagent stalls the next.
- The user-facing question tool in this project is `question`. The upstream skill
  calls it `ask_user`; that name does not exist here.
