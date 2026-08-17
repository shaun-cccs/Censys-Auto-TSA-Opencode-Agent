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

Requires [opencode](https://opencode.ai), [uv](https://docs.astral.sh/uv/), a
POSIX shell (macOS, Linux, WSL), and a Censys Platform account.

```bash
git clone https://github.com/<you>/censys-tsa-opencode ~/.config/opencode/censys-tsa
~/.config/opencode/censys-tsa/install.sh
```

Then export your credentials - both are required, and neither is ever written to
a file by this kit:

```bash
export CENSYS_PERSONAL_ACCESS_TOKEN=...   # Censys Platform → personal access token
export CENSYS_ORG_ID=...                  # your organization; the `org=` in any platform URL
```

Restart opencode (config, agents and plugins load once at startup), then check
the install from anywhere:

```bash
tsa doctor
```

`install.sh` **symlinks** rather than copies, so `git pull` in the checkout
updates the agents, prompts, references and plugin in one step. Nothing outside
these five locations is touched, and your `opencode.json` is not edited:

```
~/.config/opencode/agent/censys-{tsa,tsa-auto,fingerprint,deepdive,report}.md
~/.config/opencode/plugin/tsa-capabilities.ts
~/.config/opencode/skill/censys-tsa/
~/.local/bin/tsa
<the checkout>/.venv                       created by uv from the committed lockfile
```

Clone it wherever you like - the `tsa` command resolves its own location through
the symlink. `~/.config/opencode/censys-tsa` is only the recommended spot,
because a plugin whose real path lives there resolves its runtime dependency
without any help. Elsewhere, `install.sh` bridges that with a `node_modules`
symlink and `tsa doctor` verifies it.

Options: `--copy` (instead of symlinks), `--name <cmd>` (if `tsa` is taken),
`--config-dir`, `--bin-dir`, `--dry-run`, `--uninstall`. `install.sh --uninstall`
removes only the links it created and leaves the checkout, the venv and your
reports alone.

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
| `tsa probe <seed>` | the whole first-pass sweep in one call: seed sample plus all three tag trees | 4 |
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
