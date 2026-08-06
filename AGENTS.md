# Censys TSA - opencode agent implementation

Turn a product, vendor, appliance, or CVE into a Censys Platform query plus a
Threat Surface Assessment (TSA): a global exposed-host count and a Canada-scoped
count, both excluding honeypots.

This project is a subagent decomposition of the `censys-auto-tsa` skill. The
prose is carved verbatim into `references/`; the agents are thin routers over
it. The canonical skill lives in `/home/jovyan/14 - Learning/Censys Auto TSA`
and is **read-only** from here - never edit it.

Work from `/home/jovyan/14 - Learning/censys-tsa-opencode`. Run every script
from the project root as `python utils/<script>.py`.

---

## The seven principles

These are global constraints, not step-local advice. They apply to every agent
in this project, in every step, without exception.

**Core principle: start in Censys, not on the web.** Probe the data first with a
short full-text search and an aggregation. Only if Censys can't tell you what
you need do you escalate to creative queries, and only after that - with the
user's approval - to web research.

**Second principle: never assume Censys fingerprints the product.** Censys tags
a minority of software. `host.services.software.product` returning nothing means
"not tagged", not "not exposed" - and it does **not** even mean "not tagged",
because Censys keeps three parallel tag trees: `host.services.software`,
`host.services.hardware`, and `host.operating_system`. Appliances are commonly
absent from the software tree and fully tagged, with versions, under hardware.
Check all three before declaring a product untagged. When tagging really is
absent or incomplete, build a fingerprint from raw evidence (banners, HTML
titles, favicons, certificates, headers, ports).

**Third principle: the first TSA is never the last word.** After reporting,
always offer the user a deeper hunt (step 8) that harvests extra signatures from
the confirmed population and `or`s them onto the original query. A tag-based
count is a floor.

**Fourth principle: read CVE records, do not trust them as structured data.**
`utils/cve_lookup.py` retrieves the record and prints it as context - it does
not parse affected products or version ranges, because CNA and NVD data shapes
are too inconsistent for that to be reliable. Read the record yourself and turn
it into a Censys fingerprint by hand.

**Fifth principle: Censys rarely tags a CVE, and often cannot see the version.**
`host.services.vulns.id` matches only hosts Censys affirmatively flagged, which
is usually a tiny fraction - 18 flagged hosts against 81,232 tagged FortiOS
hosts for CVE-2024-21762. Derive the affected population from version evidence
instead (step 0b), and when the version is not remotely observable, report
product-level exposure and say plainly that patch status is unknown.

**Sixth principle: never contact assessed hosts directly.** Do not send HTTP,
TLS, DNS, protocol, scanner, browser, `curl`, or any other network request to an
IP address, hostname, or service discovered in Censys or supplied as an exposed
target. This prohibition applies even to apparently harmless unauthenticated
endpoints and positive-control checks. Validate only with stored Censys data,
authoritative public artifacts and documentation, or response evidence the user
already supplied. Web research means vendor sites, source repositories,
advisories, package registries, and documentation - never the assessed systems.

**Seventh principle: hand active validation to the user.** The agent must never
contact an assessed host, but it may identify a public version, build, status, or
configuration endpoint from authoritative source or release artifacts and ask
the user to request it manually. Make the boundary explicit: the user must own
the target or be authorized to test it, choose or confirm the IP/hostname, run
the request themselves, and paste the status, headers, and body back into the
conversation. Analyze only that user-supplied response. Never run the request,
silently assume authorization, ask for credentials, or ask the user to include
cookies, authorization headers, API keys, or other secrets.

---

## Capabilities

Network access, endpoint validation, the deep dive, report writing and the
credit budget are **negotiated once at the start of a run and then enforced by a
plugin** (`.opencode/plugins/tsa-capabilities.ts`) across every subagent.

- `censys-tsa` interviews the user (step -1) and records the answers with the
  `tsa_capabilities` tool.
- `censys-tsa-auto` takes them from the `TSA_CAPABILITIES` env var, which
  `bin/tsa` populates from its flags. No interview.
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

Two deliberate design points:

- Every agent that may reach the network has `webfetch`/`websearch` set to
  `allow` in its frontmatter, and the plugin is the only gate. This is not
  laziness: an `ask` permission inside a subagent hangs forever under
  `opencode run`, because `--auto` does not reach subagent sessions and there is
  no UI to prompt in. Static config stays permissive; the plugin throws.
  `censys-report` is the exception - denied outright, since it renders files and
  has no business on the network at all.
- Because the plugin is the only gate, **a plugin that fails to load enforces
  nothing**. The orchestrators therefore call `tsa_capabilities` as their first
  action: if that tool is missing the run fails loudly rather than proceeding
  with the network wide open.
- The credit budget is a **coarse circuit-breaker, not an accountant**. Real
  spend is still measured with `utils/censys_credits.py`. See the plugin header
  for why command-line cost estimation cannot be exact.

**Version breakdown is off by default.** A plain product TSA does not produce a
per-version distribution table - those cost an aggregation each and dominate the
report. It turns on when the user asks, when the target names a version
(`LobeChat 1.123.1`), or when the target is a CVE. This gates only the
distribution *table*: version **scoping** for a CVE remains mandatory, because
that is what makes the count correct.

Unlike every other capability here, `versionBreakdown` is **advisory, not
enforced**. A version aggregation is produced by `censys_aggregate.py`, the same
tool used for all legitimate fingerprinting, so the plugin has no signature to
block on. Honour it as an instruction; do not assume something will stop you.

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

Run the fast suite after changing an agent prompt, the plugin, or `bin/tsa`.
Run `--live` after changing anything about capability enforcement. See
`tests/README.md` for what each suite defends and why.

Two invariants the tests enforce that are easy to break by accident:

- **Never set `webfetch`/`websearch` to `ask`.** It hangs a subagent under
  `opencode run`. Use `allow` and let the plugin gate it.
- **Never put a behavioural change in `references/`.** That directory is a
  verbatim carve of `SKILL.md`; changes belong in agent prompts.

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

The seven-item skeleton in `references/counting-and-report.md` describes what
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
`python utils/tsa_report.py --template`.

| Spec key | Produced by |
| --- | --- |
| `product`, `vendor`, `summary`, `basis`, `rationale`, `sources`, `caveats` | `censys-fingerprint` |
| `baseline.query` | `censys-fingerprint` |
| `extra_assessments` | `censys-fingerprint` (step 0b version-scoped sub-counts) |
| `baseline.counts`, `country`, `cve`, `date`, `credits` | `censys-tsa` orchestrator |
| `deep_dive` | `censys-deepdive` |
| the files on disk | `censys-report` |

## Step routing

| Step | Reference file |
| --- | --- |
| workspace, prerequisites, rate limits, credentials | `references/workspace.md` |
| 0, 0b - CVE intake, affected population | `references/cve-workflow.md` |
| 1, 2, 3, 3b - probe, tagging, fingerprinting, web research | `references/fingerprinting.md` |
| aggregation semantics (the two knobs, bucket levels, aliases, HONEYPOT) | `references/aggregation-semantics.md` |
| 4 - CenQL query-drafting rules | `references/cenql-rules.md` |
| 5, 6, 7 - validate, run the TSA, report | `references/counting-and-report.md` |
| 8 - the deeper hunt | `references/deep-dive.md` |
| 9 - persist the investigation | `references/report-spec.md` |
| credit costs and measurement | `references/credits.md` |
| worked examples (load on demand) | `references/examples.md` |

## Conventions

- **Never estimate credits.** Measure with `utils/censys_credits.py`, per
  `references/credits.md`.
- **Counts always come from `host.*` queries.** `web.*` and `cert.*` are pivots.
- **Do not hand-add honeypot or country clauses.** `utils/censys_tsa.py` appends
  `not labels: "HONEYPOT"` and `host.location.country=...` itself.
- **Only the base query goes in the spec.** The renderer derives the honeypot and
  country variants and the platform URLs. Never paste a URL into a spec.
- **The rate-limit budget is shared across subagents** via
  `~/.censys_query_rate_state.json`. Budget burned by one subagent stalls the next.
- The user-facing question tool in this project is `question`. The source skill
  calls it `ask_user`; that name does not exist here.
