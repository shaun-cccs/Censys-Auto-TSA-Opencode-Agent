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
| `references/leads.md` | **source of truth** for the fan-out protocol: leads, waves, call caps |
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

   The single exception is a **permission pattern** in agent frontmatter, which
   is config addressed to opencode's matcher and never prose read by a model:
   `censys-tsa` allows `edit` under `/tmp/opencode/*`. That path is opencode's
   own scratch directory, identical on every machine, so it freezes no install
   location and resolves against nothing. Prose stays bound by the ban - if you
   want a path in a sentence, what you actually want is a `tsa` subcommand.
2. **No `python`, no `pip`.** There is no `python` on many machines, and `pip
   install` would hit the wrong interpreter. `bin/tsa` decides how to run things:
   uv for the Censys SDK subcommands, bare `python3` for the standard-library
   ones.
3. **The principles are generated, not written.** Edit `references/principles.md`
   and run `python scripts/gen_agents.py`. Never edit the block inside an agent
   file.
4. **No `ask`-class permission may be reachable from a subagent.** An `ask`
   inside a subagent hangs forever under `opencode run`, because `--auto` does not
   reach subagent sessions and there is no UI to prompt in. Concretely:
   - Never set `webfetch`/`websearch` to `ask` in agent frontmatter. Use `allow`
     and let the plugin be the gate.
   - Never have an agent touch a path outside the workspace, which triggers
     opencode's `external_directory` permission. This bit us for real: a
     `censys-deepdive` run stalled for 45 minutes reading the rate-state file
     from the home directory, on a prompt nothing could answer. State files are
     reached through `tsa budget` and `tsa credits`, never by path - which rule 1
     already required.

     `/tmp/opencode` is the exception, because opencode's built-in agent
     defaults already resolve `external_directory` to `allow` there. It is the
     one place outside the workspace an agent can touch without risking that
     prompt - useful for scratch files, useless for anything that must survive
     the run.

   When adding a tool call to any agent prompt, ask which permission it evaluates
   and whether the answer can be `ask`. If it can, the subagent will hang, not
   fail.
5. **No agent may sleep, poll, or wait.** Nothing in this workflow runs in the
   background: a `task` call blocks until the worker returns and a `bash` call
   blocks until the command exits, so a wait cannot let anything finish. Agents
   were observed sleeping "to let queries complete", which is invisible dead time
   inside a subagent. A rate-limit error is a *result* - report it, or raise the
   pacing profile and re-issue the one call. Never write prose that suggests
   waiting, and never ship a `sleep` in an example. Tests enforce this across
   every prompt and reference.

## Why a TSA used to take an hour

Worth knowing before touching anything here, because it is the reason for
`tsa probe`, `tsa candidates`, `tsa batch`, the pacing profiles and the fan-out.

Measured: one Censys action costs **0.7-2.6s** end to end, including process
start. The 90 saved specs in `reports/` record a mean of 18 fingerprint findings
and 15.6 deep-dive signals per assessment - on the order of **100-300 API
actions**. A hundred sub-second calls cannot take an hour.

The time went into **serial agent turns**: one call per bash call, one bash call
per turn, one turn at a time, one agent at a time. Wall clock was very nearly the
turn count multiplied by model latency. `tsa timeline` prints the split -
`idle gap = run span - time inside Censys` - and on an unoptimised run the idle
gap is over 90%.

Two consequences for anyone changing this kit:

- **A new capability should cost turns, not calls.** Adding a mandatory check
  that costs one credit is cheap; adding one that costs a separate *turn* is not.
  Fold it into a batching subcommand or into an existing call.
- **`standard` pacing is a museum piece.** Its 200-requests-per-hour rolling
  budget is below what a single assessment issues, which is why the default
  fallback is `fast`. Do not restore it as a default.

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

**Pacing (`rateLimit`) is carried in the capability set but enforced somewhere
else entirely.** It is a `tsa limits` profile persisted to a state file, read by
every Censys subcommand in every subagent - because pacing happens inside a Python
process, not at the tool boundary the plugin can see. So:

- The orchestrator must run `tsa limits <profile>` after registering. The
  `tsa_capabilities` response says so explicitly; `tsa run` does it itself rather
  than trusting an unattended agent to remember.
- The fallback when nobody chooses is `fast`, matching
  `censys_limits.FALLBACK_PROFILE`, so forgetting costs a little speed and not a
  stalled run. A test asserts the two defaults stay in sync.
- **Pacing is not a spend limit.** Credits are capped by `callBudget` and by
  `CENSYS_SESSION_CREDIT_CEILING`, and measured with `tsa credits`. Turning
  pacing off does not raise what a run may spend.
- The profile is machine-global, like the request budget and the credit ledger.
  Two concurrent TSAs share it - a documented trade, because a bash command
  cannot see an opencode session id.

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
  |  recon (tsa probe), leads, waves          |  skips 3b, endpoint validation, step 8
  |  assembles the report spec                |
  |
  +-> censys-fingerprint x N  (subagent)  one per LEAD, spawned in ONE message
  |     MODE: recon | lead | refine      steps 0, 0b, 1, 2, 3, 3b
  +-> censys-deepdive    x N  (subagent)  one per SIGNAL FAMILY, ditto
  |     MODE: family (8a-8b) | full (8a-8e)   [only after the user accepts]
  +-> censys-report           (subagent)  step 9  [writes <slug>.spec.json + .md]
```

**Fan-out is the shape, not an optimisation to bolt on.** `tsa ref leads` is the
protocol: 4 workers wide (6 hard ceiling), 3 waves, a Censys call cap per worker,
`leads[]` returned for the next wave, and a `STATUS:` line as every worker's last
line. Parallel task calls **must** go in one message - measured on opencode
1.18.18, two workers issued together overlapped for 5.5 of 6 seconds; issued in
separate messages they serialise, because a task call blocks until its worker
returns.

Two rules that keep fan-out from degrading quality:

- **Workers report, the orchestrator decides.** Splitting the work must not split
  the judgement. The rules that need the whole picture - measure contamination
  before gating, symmetric difference before replacing a fingerprint - are applied
  by the orchestrator to the merged numbers.
- **A family worker stops before 8c.** Several workers cannot each build a union
  and run their own `tsa assess`; the orchestrator unions the survivors and counts
  once. `MODE: full` exists for a hunt small enough for one worker.

The orchestrator is a **spec assembler**. Each subagent returns the fragment of
`reports/<slug>.spec.json` that it owns; the orchestrator merges them and hands
the merged spec to `censys-report`. The spec schema is defined by
`tsa report --template`.

| Spec key | Produced by |
| --- | --- |
| `product`, `vendor`, `summary`, `basis`, `rationale`, `sources`, `caveats` | reconciled by the orchestrator from every `censys-fingerprint` worker |
| `baseline.query` | reconciled by the orchestrator from the workers' candidate queries |
| `extra_assessments` | `censys-fingerprint` (step 0b version-scoped sub-counts) |
| `baseline.counts`, `country`, `cve`, `date`, `credits` | `censys-tsa` orchestrator |
| `deep_dive` | `censys-deepdive` under `MODE: full`; assembled by the orchestrator from family workers' signals |
| `verdict`, `examples`, `leads`, `calls_made` | every worker - routing data, not report content |
| the files on disk | `censys-report` |

## Step routing

| Step | Reference |
| --- | --- |
| the seven principles (already in every prompt) | `tsa ref principles` |
| tools, pacing profiles, credentials, the batching rule | `tsa ref workspace` |
| leads, waves, call caps, the fan-out contract | `tsa ref leads` |
| 0 - CVE intake; 0b - version derivation, for **any** named version, CVE or not | `tsa ref cve-workflow` |
| 1, 2, 3, 3b - probe, tagging, fingerprinting, web research | `tsa ref fingerprinting` |
| aggregation semantics (the two knobs, bucket levels, aliases, HONEYPOT) | `tsa ref aggregation-semantics` |
| 4 - CenQL query-drafting rules | `tsa ref cenql-rules` |
| 5, 6, 7 - validate, run the TSA, report | `tsa ref counting-and-report` |
| 8 - the deeper hunt | `tsa ref deep-dive` |
| 9 - persist the investigation | `tsa ref report-spec` |
| credit costs and measurement | `tsa ref credits` |
| worked examples (load on demand) | `tsa ref examples` |

Every reference an agent reads mid-workflow carries a **quick card** printed by
`tsa ref <name> --brief`: the procedure and the commands, about a tenth of the
text. Workers read cards; the full reference is for the judgement calls, and
`--brief` falls back to the whole file where no card exists (`credits`,
`examples`, `principles`, `report-spec`). When you add a hard-won rule to a
reference, decide whether it belongs in the card - if a worker would get the step
*wrong* without it, it does.

## Conventions

- **Never estimate credits.** Measure with `tsa credits`, per `tsa ref credits`.
- **Counts always come from `host.*` queries.** `web.*` and `cert.*` are pivots.
- **Do not hand-add honeypot or country clauses.** `tsa assess` appends
  `not labels: "HONEYPOT"` and `host.location.country=...` itself.
- **Only the base query goes in the spec.** The renderer derives the honeypot and
  country variants and the platform URLs. Never paste a URL into a spec.
- **The rate-limit budget is shared across subagents and across concurrent runs.**
  Budget burned by one subagent stalls the next. Read it with `tsa budget`, never
  by opening the state file - see rule 4.
- The user-facing question tool in this project is `question`. The upstream skill
  calls it `ask_user`; that name does not exist here.
