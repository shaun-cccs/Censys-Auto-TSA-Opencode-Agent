<!--
Provenance: originally carved verbatim from the upstream censys-auto-tsa
SKILL.md (1497 lines). This copy is canonical for this kit.
Source lines: 1293-1359

Step -> reference file map (the skill's inline "see step N" pointers resolve here):
  the seven principles       -> tsa ref principles (already in every agent prompt)
  workspace, credentials     -> tsa ref workspace
  steps 0, 0b  (CVE/version) -> tsa ref cve-workflow
  steps 1, 2, 3, 3b          -> tsa ref fingerprinting
  aggregation semantics      -> tsa ref aggregation-semantics
  step 4  (CenQL rules)      -> tsa ref cenql-rules
  steps 5, 6, 7              -> tsa ref counting-and-report
  step 8  (deep dive)        -> tsa ref deep-dive
  step 9  (persistence)      -> tsa ref report-spec
  credit costs               -> tsa ref credits
  worked examples            -> tsa ref examples
-->


Read before quoting any credit figure. Never estimate - measure.

## Credit (token) usage

Rate limits are separate from credits: credits are the metered spend. **Never
guess a credit figure - measure it with `tsa credits`, or quote the
published rate below.** `tsa assess` reports the credits a run consumed
unless `--no-credits` is passed; a TSA run is 2 searches, so about 2 credits.

### What things actually cost

Censys enterprise metering, from the vendor's pricing documentation and
confirmed by measuring the org balance before and after each call
(2026-08-05):

| Action | Cost | Verified |
| --- | --- | --- |
| Any API action - search, aggregation, asset lookup | **1 credit** | yes |
| Regex / "advanced" query | **1 credit - no surcharge** | yes, 1 |
| Each additional page of 100 search results | **+1 credit** | yes, 5 pages = 5 |
| Aggregation, any `number_of_buckets` up to 2000 | **1 credit** | yes, k=5 and k=2000 both 1 |
| Credit balance / usage endpoints (`tsa credits`) | **0** | yes, control delta 0 |
| `tsa cve` (cve.org / NVD, not Censys) | **0** | n/a |
| `tsa report` (renders locally, never calls Censys) | **0** | n/a |
| Bulk host / certificate / web property endpoints | **1 per asset retrieved** | not used here |
| Live Rescan | 10 | not used here |
| Adversary Investigation: Initiate Live Discovery scan | 15 | not used here |
| Adversary Investigation: host history for a certificate | 5 per page | not used here |
| Adversary Investigation: get scan status | 0 | not used here |
| CensEye: value counts to discover pivots | 1 per count condition | not used here |
| CensEye: create a pivot analysis job | 44 host / 28 web property / 7 certificate | not used here |

Platform **UI** actions are unlimited and mostly free for enterprise users;
credits meter **API** usage only. Censys Assistant chats bill as the API calls
they make.

Two corrections to earlier versions of this skill, both wrong and now fixed:
regex searches do **not** cost 8 credits (that was Starter-plan pricing), and
aggregations are **not** free - they cost 1 credit like any other API action.
Budget an investigation by counting API calls, roughly one credit each, plus one
per extra page of 100 results.

**Always surface this in the report** - section 6 of step 7 is mandatory. Quote
the measured figure and the balance delta; do not estimate.

### Reading the balance and usage report

Check the balance or a historical report at any time - both endpoints are free:

```bash
tsa credits balance
tsa credits usage --start-date 2026-07-01 --granularity daily
tsa credits usage --granularity monthly --by-consumer
tsa credits -f json usage --by-consumer   # -f is a global flag, before the subcommand
```

`usage` defaults to the last 30 days; `--start-date` must be on or after
2025-01-01 and the range must not exceed 365 days. `--by-consumer` requires the
Admin role. The usage report lags by a short interval, so a TSA run's credit
figure is taken from the balance delta and `consumed_reported` may read 0.

**The balance is org-wide, so a delta is only yours if nobody else is
spending.** This org runs other consumers - a daily automated job accounts for
roughly 1,000 credits/day on its own, so a raw day total says nothing about the
TSA. Attribute spend with `--by-consumer`, and treat a `tsa assess` credit
figure as approximate if another consumer may have been active during the run.
When a delta looks implausible (negative, or far larger than the calls you
made), say so in the report rather than quoting it as fact.
