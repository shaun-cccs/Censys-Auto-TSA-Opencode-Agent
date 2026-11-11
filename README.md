# Censys TSA for opencode

Turn a product, vendor, appliance, or CVE into a **Censys Platform query plus a
Threat Surface Assessment**: how many hosts on the internet expose it, how many
of those are in one country, honeypots excluded, with the counting basis and the
credits spent stated explicitly.

Install once, and five agents plus a `tsa` command are available in every
project on your machine.

```
> @censys-tsa Ivanti EPMM

## Ivanti Endpoint Manager Mobile
Mobile device management appliance; exposes an HTTPS admin portal and an
enrolment endpoint.

**Baseline query**
`host.services.software.product="Endpoint Manager Mobile" and host.services.software.vendor="Ivanti"`
Global **7,391** · Canada **442**

Basis: tag-based (step 3) · Credits: 6 used (1,204 → 1,198)

**Caveats**
- Version is not remotely observable, so patch status is unknown.
- Tag-based counts are a floor; a deep dive would widen them.

Full report: reports/ivanti-epmm.md
```

## Install

Requires [opencode](https://opencode.ai) **1.18.14 or newer, including
OpenCode 2**, [uv](https://docs.astral.sh/uv/), a POSIX shell (macOS, Linux,
WSL), and a Censys Platform account with the **API Access** role.

```bash
git clone https://github.com/<you>/censys-tsa-opencode ~/.config/opencode/censys-tsa
~/.config/opencode/censys-tsa/install.sh --dry-run    # see what it would do
~/.config/opencode/censys-tsa/install.sh
```

The installer detects your opencode version, links the matching plugin, checks
the install, and - when run in a terminal and your Censys credentials are
missing - offers to set them up:

1. You paste the token (hidden as you type) and the organization ID.
2. It checks them with Censys using the credit-balance call, which costs no
   credits, and explains a rejection (400 / 401 / 403) in plain words.
3. Only after you say yes, it backs up your shell profile (`~/.bashrc`,
   `~/.zshrc` or `~/.profile`) and writes the two `export` lines in a marked
   block that a re-run replaces. The file is set to mode 600.
4. It adds the Censys Platform MCP server to your global `opencode.json`
   (see below), and offers to restart the OpenCode background service so its
   agents see the new variables. That restart interrupts running sessions, so
   the default answer is no.
5. Finally it offers to open a new shell in place of the script, with the
   credentials already loaded. (A script cannot change the shell that started
   it; the new shell reads your profile as it starts. `exit` returns to the
   old one.) New terminals load them on their own from then on.

Run that step on its own at any time with `install.sh --credentials`.

Where to find the two values (from the
[Censys docs](https://docs.censys.com/reference/get-started)):

| Variable | Where |
| --- | --- |
| `CENSYS_PERSONAL_ACCESS_TOKEN` | platform.censys.io > user icon > **API Access**, or [accounts.censys.io/settings/personal-access-tokens](https://accounts.censys.io/settings/personal-access-tokens) > **Create New Token**. Shown only once. |
| `CENSYS_ORG_ID` | Same page, **Current Organization** box > Copy. Select your organization, not your Free account. |

Prefer to do it by hand? Put these in your shell profile, open a new terminal,
and restart opencode:

```bash
export CENSYS_PERSONAL_ACCESS_TOKEN=...
export CENSYS_ORG_ID=...
```

Check the install from anywhere:

```bash
tsa doctor
```

`tsa doctor` lists every failed check, then explains how to fix credential
problems below the "N check(s) failed" line.

### What it installs

`install.sh` **symlinks** rather than copies, so `git pull` in the checkout
updates the agents, prompts, references and plugin in one step:

```
~/.config/opencode/agent/censys-{tsa,tsa-auto,fingerprint,deepdive,report}.md
~/.config/opencode/plugin/tsa-capabilities.ts       OpenCode 1 plugin
~/.config/opencode/plugins/tsa-capabilities/        OpenCode 2 plugin
~/.config/opencode/skill/censys-tsa/
~/.local/bin/tsa
<the checkout>/.venv                                created by uv from the lockfile
```

Two writes outside those links, both only with your consent or once the
credentials check out:

- your shell profile, for the two credentials (`--credentials` flow above);
- your global `opencode.json`, for the `censys-platform` MCP server. A dated
  backup is made first. The entry holds `{env:CENSYS_PERSONAL_ACCESS_TOKEN}`
  and `{env:CENSYS_ORG_ID}` placeholders, never the values. A
  `opencode.jsonc` with comments is never rewritten; the script prints the
  snippet to add instead.

### OpenCode 1 and OpenCode 2

OpenCode 2 has a new plugin API and does not run OpenCode 1 plugins, so the
kit ships the capability plugin twice with the same rules:

| | Source | Installed as |
| --- | --- | --- |
| OpenCode 1 | `plugins/v1/tsa-capabilities.ts` | `plugin/tsa-capabilities.ts` |
| OpenCode 2 | `plugins/v2/tsa-capabilities/index.ts` | `plugins/tsa-capabilities/` |

Why they live outside `.opencode/`: opencode auto-loads plugins from a
project's `.opencode/`, so opening this checkout would load the plugin a second
time (OpenCode 2 refuses it as a duplicate) or try to run the V1 file on V2.
A test fails if the two copies' shared rules drift apart.

`install.sh` picks the version from `opencode --version`, or installs both when
opencode is not on PATH. On OpenCode 2 it reloads opencode instead of asking
you to restart it, and `tsa run` uses `opencode run --standalone`, because only a
private server inherits `TSA_CAPABILITIES` from the environment.

### The Censys MCP server

Added once your credentials check out, so you can ask Censys questions in any
ordinary opencode chat. **TSA runs are kept off it**: its calls spend credits
the run's budget cannot count, so the capability plugin refuses them in every
TSA session and the agents use `tsa` instead. Your other sessions are not
affected.

### Options

| Option | Effect |
| --- | --- |
| `--dry-run` | print what would happen, change nothing |
| `--doctor` | check an existing install (same as `tsa doctor`) |
| `--credentials` | prompt for, verify and save the two Censys credentials |
| `--mcp` / `--no-mcp` | always / never add the MCP server (default: once credentials check out) |
| `--no-prompt` | never ask anything (scripts, CI) |
| `--opencode 1\|2\|both` | override the detected opencode version |
| `--copy` | copy instead of symlinking (re-run after `git pull`) |
| `--name <cmd>` | install the command as something other than `tsa` |
| `--config-dir`, `--bin-dir` | install somewhere else |
| `--force` | replace files the script does not recognise as its own |
| `--uninstall` | remove only what it created, including the MCP entry (`--no-mcp` keeps it); leaves the checkout, venv, reports and your shell profile alone |

Clone it wherever you like - the `tsa` command resolves its own location through
the symlink. On OpenCode 1, `~/.config/opencode/censys-tsa` is the recommended
spot, because a plugin whose real path lives there resolves its runtime
dependency without help. Elsewhere, `install.sh` bridges that with a
`node_modules` symlink and `tsa doctor` verifies it. OpenCode 2 needs no bridge.

No uv? Install `censys-platform` into any interpreter and set
`CENSYS_TSA_PYTHON` to it; uv is then never invoked.

## Use it

**Interactively** - switch to the `censys-tsa` agent in the opencode TUI and name
a target. It opens with a handful of questions about what it is allowed to do (web
research, user-operated endpoint validation, the deep dive, a credit budget,
report output, request pacing), then runs the assessment - reconnoitring the
target itself and fanning the discovery work out across several subagents that
run at the same time.

```
@censys-tsa Ivanti EPMM
@censys-tsa CVE-2024-21762
@censys-tsa CVE-2024-21762, scoped to Fortinet FortiOS
```

**Unattended** - no questions, for CI or a batch of targets:

```bash
tsa run "Ivanti EPMM"
tsa run --cve CVE-2024-21762 --country Australia
tsa run --allow-web --deep-dive --budget 50 "Flowise"
tsa run --rate none "Flowise"          # no request pacing at all
```

Reports are written to `./reports/` in **the directory you run from**, so
assessments land next to the work they belong to. `tsa run` also prints the spec
to stdout, so it pipes.

Everything the agents use is available to you directly:

| Command | What it does | Credits |
| --- | --- | --- |
| `tsa assess <query>` | global + country counts for a base query | 2 |
| `tsa search <query>` | rate-limited host search, for validating a query | 1 |
| `tsa agg <field> <query>` | bucket a field across a query - the fingerprint tool | 1 |
| `tsa probe <seed>` | the whole first-pass sweep in one call: seed sample, all three tag trees, decoded protocols | 5 |
| `tsa candidates <base> <c>...` | per candidate signal, the hosts it adds over the base and what they look like | 1 + 2 each |
| `tsa batch --count/--sample/--agg` | any set of independent calls, run together | 1 each |
| `tsa cve <CVE-ID>` | fetch a CVE record from cve.org, falling back to NVD | 0 |
| `tsa credits balance` | credit balance and usage | 0 |
| `tsa limits [none\|fast\|standard]` | how fast Censys requests may be issued | 0 |
| `tsa timeline` | where a run's wall-clock time went | 0 |
| `tsa report <spec.json> -o <out.md>` | render a report from a spec | 0 |
| `tsa ref [name] [--brief]` | the workflow references the agents read | 0 |
| `tsa doc host --grep favicon` | CenQL and queryable-field documentation | 0 |

`tsa help` lists them all; every subcommand takes `--help`.

## Speed

An assessment issues 100-300 Censys API actions. Each one takes about a second,
so the work itself is a couple of minutes; everything else is the agent thinking
between calls. Three things keep that from dominating:

- **Independent calls go out together.** `tsa probe`, `tsa candidates` and
  `tsa batch` each do in one call what used to take four, twenty or arbitrarily
  many separate ones.
- **Independent hypotheses go out together.** The orchestrator reconnoitres the
  target, derives leads from what it sees, and runs four fingerprinting subagents
  concurrently, each with a hard cap on how many queries it may spend.
- **Pacing is a choice, not a default.** `tsa limits none` removes it entirely;
  credits stay capped separately. The old default paced every request by a second
  and allowed 200 an hour - less than one assessment needs.

`tsa timeline` shows the split for the last run: time spent inside Censys versus
idle gap. If the idle gap is over 90%, the run was waiting on agent turns rather
than on Censys.

## What it will not do

Two rules are load-bearing, and they are in every agent's system prompt rather
than left to good intentions:

- **It never contacts an assessed host.** No HTTP, TLS, DNS, scanner, browser or
  `curl` request to any IP, hostname or service that comes out of a query - not
  even a harmless-looking unauthenticated endpoint. Every count comes from stored
  Censys data. If a version can only be confirmed by requesting an endpoint, it
  asks *you* to run that request against a host *you* own, and analyses only what
  you paste back. It will never ask for credentials, cookies or auth headers.
- **It does not go to the web unless you allow it.** Web research is off by
  default and, when enabled, means vendor sites, repositories, advisories and
  registries - never the assessed systems.

Those limits, the deep dive, report writing and the credit budget are negotiated
once at the start of a run and then **enforced by a plugin** across every
subagent, not merely requested in a prompt. Defaults are fail-closed: a run that
never registers capabilities cannot reach the network.

That plugin is installed globally, so it is careful to stay out of the way: it
governs only the five `censys-*` agents and returns immediately for every other
session on your machine.

## Credits, and why the counts are honest

Censys calls cost credits: 1 for a search or an aggregation, 2 for an
assessment. The agents **measure** real spend rather than estimating it, and
report it on every assessment. `--budget N` is a coarse circuit-breaker against a
runaway loop, not an accountant. Running discovery in parallel costs somewhat more
than running it serially - several hypotheses get tested that a serial pass would
have abandoned - so every subagent has a hard cap on the queries it may spend, and
the budget is the backstop.

Counts always come from `host.*` queries, honeypots are always excluded, and the
report says which of these the number is:

- **tag-based** - Censys affirmatively fingerprints the product
- **version-scoped** - the affected population was derived from version evidence
- **product exposure (patch status unknown)** - the version is not remotely
  observable, and the report says so plainly

A first count is treated as a **floor**, never a ceiling: Censys tags a minority
of software, so the deep dive exists to harvest extra signatures (favicons, HTML
titles, certificates, banners, JARM) from the confirmed population and widen the
query.

## Contributing

See `AGENTS.md` for the layout, the design decisions and the five absolute rules
for anything user-facing. Tests:

```bash
tests/run.sh          # fast: static checks, no agent runs, no Censys, no network
tests/run.sh --live   # also exercises plugin enforcement against real agents
```
