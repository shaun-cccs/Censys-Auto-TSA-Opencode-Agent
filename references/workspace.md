<!--
Provenance: carved from censys-auto-tsa/SKILL.md.
Source lines: 64-116 (Workspace, Prerequisites), 1282-1291 (Rate limits),
1361-1365 (Credentials).

Edited, not verbatim: the path table now points at this project, the docs table
gained the references/ files, and the `skill-sync` maintenance block was dropped
(it does not apply here - this project's references/ are canonical for itself).
-->

# Workspace, prerequisites, rate limits, credentials

All paths are relative to `/home/jovyan/14 - Learning/censys-tsa-opencode`.
Always work from there. Run every script from the project root as
`python utils/<script>.py`.

## Executable tools

| Path | Purpose |
| --- | --- |
| `utils/censys_tsa.py` | TSA driver. Base host query and/or CVE in, platform query + global + Canada counts + credits out. |
| `utils/censys_aggregate.py` | Bucket a field across a query. The main fingerprint-discovery tool. Pass `--count-hosts` for host counts - the default counts nested occurrences. 1 credit per call. |
| `utils/censys_query.py` | Rate-limited Censys Platform search client. Validation and pivots. |
| `utils/cve_lookup.py` | Retrieve a CVE record from cve.org, falling back to NVD. Context only, no parsing. Free to call. |
| `utils/censys_credits.py` | Censys credit (token) balance and usage reporting. Free to call. |
| `utils/tsa_report.py` | Render a completed investigation as a markdown report from a JSON spec. Free to call. |
| `bin/tsa` | Non-interactive wrapper. Drives the `censys-tsa-auto` agent and emits `reports/<slug>.spec.json` on stdout. |
| `.opencode/plugins/tsa-capabilities.ts` | Negotiates and hard-enforces run capabilities (web research, endpoint validation, deep dive, report writing, credit budget) across every subagent. Provides the `tsa_capabilities` tool. |

## Query-language documentation

| Path | Purpose |
| --- | --- |
| `docs/censys_query_language.md` | CenQL syntax reference. **Read before writing any query.** |
| `docs/censys_regex_language.md` | CenQL regex reference - escaping, anchors, supported operators, credit cost. **Read before writing any `=~` pattern.** |
| `docs/queryable_fields/host_censys_queryable_fields.md` | Host fields. **Counts always come from host queries.** |
| `docs/queryable_fields/web_censys_queryable_fields.md` | Web property fields. Pivots only. |
| `docs/queryable_fields/certificate_censys_queryable_fields.md` | Certificate fields. Pivots only. |
| `docs/queryable_fields/misc_censys_queryable_fields.md` | Tag fields. Pivots only. |

Field files are large - grep, do not read whole:

```bash
grep -n 'favicon' docs/queryable_fields/host_censys_queryable_fields.md | head -20
```

## Workflow references

| Path | Owned by | Covers |
| --- | --- | --- |
| `AGENTS.md` | all agents | the seven principles, always loaded |
| `references/workspace.md` | all agents | this file |
| `references/cve-workflow.md` | `censys-fingerprint` | steps 0, 0b |
| `references/fingerprinting.md` | `censys-fingerprint` | steps 1, 2, 3, 3b |
| `references/aggregation-semantics.md` | shared | the two knobs, bucket levels, aliases, HONEYPOT |
| `references/cenql-rules.md` | shared | step 4 query-drafting rules |
| `references/counting-and-report.md` | `censys-tsa` | steps 5, 6, 7 |
| `references/deep-dive.md` | `censys-deepdive` | step 8 |
| `references/report-spec.md` | `censys-report` | step 9 |
| `references/credits.md` | `censys-tsa`, `censys-report` | credit costs and measurement |
| `references/examples.md` | on demand | three worked examples |
| `reports/` | `censys-report` | one `<slug>.spec.json` + `<slug>.md` pair per assessment |

## Prerequisites

All Censys scripts depend on the `censys-platform` SDK. Check for it once at the
start of a run and install it only if it is missing:

```bash
python -c "import censys_platform" 2>/dev/null || pip install --quiet censys-platform
```

If `pip` is not on `PATH`, use `python -m pip install --quiet censys-platform`.
Do not reinstall or upgrade the package when the import already succeeds.
`utils/cve_lookup.py` uses only the standard library and needs nothing.

## Rate limits

`utils/censys_query.py` enforces a min interval, a per-minute cap, and a rolling
request budget persisted across runs in `~/.censys_query_rate_state.json`. Every
Censys script shares it. On `request budget exhausted`, wait rather than raising
the budget. Aggregations are cheap per request but `--suggest-fields` issues one
request per field - use a targeted field list when the budget is tight. Keep
validation queries at `--max-results 5`; TSA counts fetch one hit each and read
`total_hits`. `utils/cve_lookup.py` does not touch Censys at all, so it is
outside this budget entirely.

The budget is shared across subagents. A `censys-fingerprint` run that burns the
budget will stall the `censys-deepdive` run that follows it in the same session.

## Credentials

The client reads `CENSYS_PERSONAL_ACCESS_TOKEN` from the environment, falling
back to the Spellbook vault (`CCDC1` / `Censys`). `CENSYS_ORG_ID` overrides the
default organization. Never print or commit the token.
