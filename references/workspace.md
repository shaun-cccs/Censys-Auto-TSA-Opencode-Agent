<!--
Provenance: originally carved from the censys-auto-tsa SKILL.md (Workspace,
Prerequisites, Rate limits, Credentials), then rewritten for a kit that is
installed rather than checked out. references/ is canonical for this project.
-->

# Tools, prerequisites, rate limits, credentials

**There are no paths in this workflow.** Everything ships behind one command,
`tsa`, which finds its own installation. Run it from wherever the user is
working; output files land in the current directory. Never guess at a path to a
script, a reference or a doc, and never `cd` anywhere.

## Executable tools

| Command | Purpose |
| --- | --- |
| `tsa assess` | TSA driver. Base host query and/or CVE in, platform query + global + country counts + credits out. 2 credits. |
| `tsa agg` | Bucket a field across a query. The main fingerprint-discovery tool. Pass `--count-hosts` for host counts - the default counts nested occurrences. 1 credit per call. |
| `tsa search` | Rate-limited Censys Platform search client. Validation and pivots. 1 credit. |
| `tsa cve` | Retrieve a CVE record from cve.org, falling back to NVD. Context only, no parsing. Free. |
| `tsa credits` | Censys credit (token) balance and usage reporting. Free. |
| `tsa budget` | Session credit ledger state. Free. |
| `tsa report` | Render a completed investigation as a markdown report from a JSON spec. Free. |
| `tsa run` | Non-interactive wrapper. Drives the `censys-tsa-auto` agent and emits `reports/<slug>.spec.json` on stdout. |
| `tsa doctor` | Verify the installation: dependencies, credentials, links, capability plugin. Free. |

Every subcommand takes `--help`.

## Query-language documentation

| Command | Purpose |
| --- | --- |
| `tsa doc cenql` | CenQL syntax reference. **Read before writing any query.** |
| `tsa doc regex` | CenQL regex reference - escaping, anchors, supported operators, credit cost. **Read before writing any `=~` pattern.** |
| `tsa doc host` | Host fields. **Counts always come from host queries.** |
| `tsa doc web` | Web property fields. Pivots only. |
| `tsa doc cert` | Certificate fields. Pivots only. |
| `tsa doc misc` | Tag fields. Pivots only. |

The field documents are large. Search them instead of printing them whole:

```bash
tsa doc host --grep favicon
```

## Workflow references

`tsa ref` with no argument lists them; `tsa ref <name>` prints one.

| Command | Owned by | Covers |
| --- | --- | --- |
| `tsa ref principles` | all agents | the seven principles - already in your system prompt |
| `tsa ref workspace` | all agents | this file |
| `tsa ref cve-workflow` | `censys-fingerprint` | steps 0, 0b - CVE intake, and version derivation for **any** named version |
| `tsa ref fingerprinting` | `censys-fingerprint` | steps 1, 2, 3, 3b |
| `tsa ref aggregation-semantics` | shared | the two knobs, bucket levels, aliases, HONEYPOT |
| `tsa ref cenql-rules` | shared | step 4 query-drafting rules |
| `tsa ref counting-and-report` | `censys-tsa` | steps 5, 6, 7 |
| `tsa ref deep-dive` | `censys-deepdive` | step 8 |
| `tsa ref report-spec` | `censys-report` | step 9 |
| `tsa ref credits` | `censys-tsa`, `censys-report` | credit costs and measurement |
| `tsa ref examples` | on demand | four worked examples - untagged, tagged, CVE, tier 2b version |

## Prerequisites

**Do not install anything.** The Censys SDK is managed by the kit's own locked
environment and is materialised on first use; `tsa cve` and `tsa report` need
nothing at all. There is no dependency-installation step in this workflow, and
hand-installing a package would land it in an interpreter none of these commands
use.

If a `tsa` subcommand reports a missing dependency, that is an installation
fault, not something to work around: run `tsa doctor`, report what it says, and
stop. Never fall back to calling a script with `python` directly.

## Output files

Reports are written to `./reports/` **relative to the directory the user is
working in**, and that is the only place this workflow writes. Never write
outside it, and never write into the kit's own installation.

## Rate limits

`tsa search` enforces a min interval, a per-minute cap, and a rolling request
budget persisted across runs in `~/.censys_query_rate_state.json`. Every Censys
subcommand shares it. On `request budget exhausted`, wait rather than raising the
budget. Aggregations are cheap per request but `--suggest-fields` issues one
request per field - use a targeted field list when the budget is tight. Keep
validation queries at `--max-results 5`; TSA counts fetch one hit each and read
`total_hits`. `tsa cve` does not touch Censys at all, so it is outside this
budget entirely.

The budget is shared across subagents. A `censys-fingerprint` run that burns the
budget will stall the `censys-deepdive` run that follows it in the same session.

## Credentials

Two environment variables, both read from the environment and never from a file:

- `CENSYS_PERSONAL_ACCESS_TOKEN` - required for every Censys call.
- `CENSYS_ORG_ID` - required; the Censys Platform organization to query and to
  build platform URLs for.

Never print either value, never write one to a file, and never ask the user to
paste a token into the conversation. If one is missing, `tsa doctor` says so -
report that and stop rather than trying to proceed.
