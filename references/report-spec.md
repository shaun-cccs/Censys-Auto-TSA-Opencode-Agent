<!--
Provenance: originally carved verbatim from the upstream censys-auto-tsa
SKILL.md (1497 lines). This copy is canonical for this kit.
Source lines: 1222-1280

Step -> reference file map (the skill's inline "see step N" pointers resolve here):
  the seven principles    -> tsa ref principles (already in every agent prompt)
  workspace, credentials  -> tsa ref workspace
  steps 0, 0b  (CVE)      -> tsa ref cve-workflow
  steps 1, 2, 3, 3b       -> tsa ref fingerprinting
  aggregation semantics   -> tsa ref aggregation-semantics
  step 4  (CenQL rules)   -> tsa ref cenql-rules
  steps 5, 6, 7           -> tsa ref counting-and-report
  step 8  (deep dive)     -> tsa ref deep-dive
  step 9  (persistence)   -> tsa ref report-spec
  credit costs            -> tsa ref credits
  worked examples         -> tsa ref examples
-->


# Step 9 - persist the investigation

Owned by the `censys-report` subagent. Costs 0 credits and never calls Censys.

### 9. Write the investigation to a markdown file

Every completed assessment gets persisted under `reports/` as a pair: a JSON
spec that records the findings, and the rendered markdown. `tsa report`
does the rendering, so all reports share one layout - product summary,
fingerprint rationale, baseline query and counts, deep-dive delta table with the
signals kept and rejected, credit consumption, and caveats.

```bash
# start from a skeleton
tsa report --template > reports/<product>.spec.json

# fill it in, then render
tsa report reports/<product>.spec.json -o reports/<product>.md
```

Only `product` and `baseline` (a `query` plus `counts`) are required. Any other
section - `rationale`, `deep_dive`, `extra_assessments`, `credits`, `caveats`,
`sources` - is dropped from the output when absent and the remaining sections
renumber themselves, so a tag-based TSA with no deep dive still renders cleanly.

`extra_assessments` is a list of additional numbered sections, rendered between
the deep dive and the credits. Use it for a version-scoped sub-count (step 0b),
a per-branch firmware distribution, or any secondary population worth its own
query and counts. Each entry accepts `heading`, `intro`, `distribution` (a list
of rows) with `distribution_columns`, `query` with `query_label` and `counts`,
and `notes`. Every field is optional, so an entry can be a bare distribution
table, a bare extra query, or both:

```json
"extra_assessments": [{
  "heading": "Version-scoped assessment - end-of-support builds",
  "distribution_columns": ["Firmware", "Global hosts", "Canada hosts", "Support status"],
  "distribution": [["12.5", "1,499", "43", "Current branch"],
                   ["12.3", "164", "3", "End of support"]],
  "query_label": "End-of-support builds (<= 12.3)",
  "query": "<base query> and host.services.hardware:(vendor=\"…\" and product=\"…\" and (version=\"12.3\" or …))",
  "counts": {"global": 227, "country": 3},
  "notes": "Why discrete versions were enumerated instead of a range."
}]
```

A `query` in an extra assessment gets the same treatment as the base query - the
renderer appends the honeypot and country clauses itself and prints both derived
queries with platform URLs - so put only the base form in the spec.

Put only the **base** query in the spec. The renderer derives the two queries
the counts actually came from - the base plus `not labels: "HONEYPOT"` for the
global count, and that plus `host.location.country="<country>"` for the national
one - and prints each with its own platform URL, exactly as
`tsa assess` reports them. It does this for the deep-dive query too.
Never paste the honeypot or country clauses, or any platform URL, into the spec.

Copy the counts and the credit figures straight from what `tsa assess`
printed - the spec is a record of the run, not a re-derivation of it. Keep the
spec alongside the markdown so a later re-assessment can diff against it. The
script never calls Censys, so it costs no credits and no rate budget.
