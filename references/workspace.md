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
| `tsa probe` | **Step 1 in one call**: the seed sample plus the product bucket in all three tag trees, concurrently. 4 credits (9 with `--wide`). |
| `tsa candidates` | **Step 8b in one call**: how many hosts each candidate signal adds over the base query, and what those hosts' titles are. 1 + 2 per candidate. |
| `tsa batch` | Any set of independent counts, samples and aggregations, run together. 1 credit each. |
| `tsa cve` | Retrieve a CVE record from cve.org, falling back to NVD. Context only, no parsing. Free. |
| `tsa credits` | Censys credit (token) balance and usage reporting. Free. |
| `tsa budget` | Session credit ledger state. Free. |
| `tsa timeline` | Where the run's wall-clock time went: time inside Censys versus idle gap. Free. |
| `tsa report` | Render a completed investigation as a markdown report from a JSON spec. Free. |
| `tsa run` | Non-interactive wrapper. Drives the `censys-tsa-auto` agent and emits `reports/<slug>.spec.json` on stdout. |
| `tsa doctor` | Verify the installation: dependencies, credentials, links, capability plugin. Free. |

Every subcommand takes `--help`.

## One turn, many calls - this is the difference between 5 minutes and an hour

**A Censys call costs about a second. A turn costs tens of seconds.** Measured on
this kit: a request plus process start is 0.7-2.6s, and a real assessment issues
around a hundred of them. Run one per turn and the assessment takes half an hour
of which almost none is Censys - `tsa timeline` prints that split, and the idle
gap is normally over 90%.

So the rule is: **never spend a turn on a single call when you have several
independent calls to make.** Two ways to obey it, in order of preference:

1. **A batching subcommand.** `tsa probe` does step 1's whole four-call sweep.
   `tsa candidates` does step 8b for every candidate at once, with the title
   evidence you need to judge them. `tsa batch` takes any mixture:

   ```bash
   tsa batch --count '<query A>' --count '<query B>' \
             --agg host.services.port '<query A>' \
             --sample '<query A>'
   ```

   These share one process, one connection pool and one credit ledger, so they
   are cheaper in wall time than the same calls made separately and cost exactly
   the same in credits.

2. **Several tool calls in one message.** When the calls do not fit one
   subcommand - different subcommands, or a query you want to see rendered its
   own way - issue them as parallel calls in a single message rather than one per
   turn.

What must stay serial is only what is genuinely dependent: you cannot test a
candidate against a base query you have not built yet. Everything else goes
together.

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

## Rate limits - a session decision, and never a reason to wait

Pacing is chosen once per run and persisted, so every subcommand in every
subagent obeys the same profile:

| Profile | Pacing | Use it when |
| --- | --- | --- |
| `none` | none at all | you want the assessment to finish; credits are still capped |
| `fast` | 120/min, 5000/hour, no interval | the default if nobody chooses - bounded, never in the way |
| `standard` | 1s interval, 20/min, 200/hour | reproducing an old run, or deliberately crawling |

```bash
tsa limits          # what is in force, and where each number came from
tsa limits none     # apply a profile - do this once, right after step -1
```

**`standard` is below what one assessment needs.** A real run issues 100-300
Censys actions; a 200-per-hour rolling budget therefore runs out partway through
its own work. That is why it is not the default any more.

**Never sleep, never poll, never wait out a limit.** A rate-limit error is a
*result*: report it and move on, or raise the profile with `tsa limits fast` and
re-issue the one call. Waiting is how a fifteen-minute assessment became an hour
- there is nothing happening in the background that a wait would let finish, and
a `sleep` in a subagent is pure dead time.

**Pacing is not a spend limit.** Credits are capped separately and measured
independently: `tsa budget` for the session ledger, `tsa credits` for the real
org balance. Turning pacing off does not raise what a run may spend.

Read the budget with `tsa budget`, and never by opening the state file. Those
files live outside any workspace, so reading one directly trips an
`external_directory` permission prompt - which, raised inside a subagent, has no
UI to answer it and hangs the run indefinitely. `tsa budget`, `tsa limits` and
`tsa credits` report the same state and cost nothing.

The request budget - when a profile has one - is shared across subagents *and*
across concurrent runs on the same machine, as is the pacing profile itself. A
second TSA started elsewhere draws on the same allowance. `tsa cve` does not
touch Censys at all, so it is outside this entirely.

Keep validation searches at `--max-results 5`; TSA counts fetch one hit each and
read `total_hits`. `tsa agg --suggest-fields` issues one request per field, but
issues them concurrently.

## Credentials

Two environment variables, both read from the environment and never from a file:

- `CENSYS_PERSONAL_ACCESS_TOKEN` - required for every Censys call.
- `CENSYS_ORG_ID` - required; the Censys Platform organization to query and to
  build platform URLs for.

Never print either value, never write one to a file, and never ask the user to
paste a token into the conversation. If one is missing, `tsa doctor` says so -
report that and stop rather than trying to proceed.
