<!--
Provenance: carved verbatim from censys-auto-tsa/SKILL.md (1497 lines),
the canonical skill in `/home/jovyan/14 - Learning/Censys Auto TSA`.
Source lines: 691-834

Step -> reference file map (the skill's inline "see step N" pointers resolve here):
  the seven principles    -> AGENTS.md (always loaded)
  workspace, credentials  -> references/workspace.md
  steps 0, 0b  (CVE)      -> references/cve-workflow.md
  steps 1, 2, 3, 3b       -> references/fingerprinting.md
  aggregation semantics   -> references/aggregation-semantics.md
  step 4  (CenQL rules)   -> references/cenql-rules.md
  steps 5, 6, 7           -> references/counting-and-report.md
  step 8  (deep dive)     -> references/deep-dive.md
  step 9  (persistence)   -> references/report-spec.md
  credit costs            -> references/credits.md
  worked examples         -> references/examples.md
-->


# Aggregation semantics - verified reference

These four subsections are children of "step 3. No usable tag - get creative
inside Censys" (`references/fingerprinting.md`), but they are shared reference
consumed by steps 0b, 2, 3, 6 and 8. Read them before running any aggregation.

Every number in this file was measured, not estimated. Where it corrects an
earlier version of the workflow, the correction is stated inline - trust the
correction.

#### The two knobs that decide what a bucket number means

An aggregation has two independent parameters, and **a bucket count is
uninterpretable until you know both**. Get either wrong and you will read a
number that answers a different question from the one you asked.

`filter_by_query` decides *which* values are counted. True (the util's default)
counts only values that satisfied the query constraint; false counts every value
present on the matching records.

`count_by_level` decides *what* is counted. It is the API's "Count By" dropdown
from the Report Builder UI, and the util exposes it as `--count-by-level`:

| `count_by_level` | Counts |
| --- | --- |
| `""` (API default) | documents at the deepest nested level containing the field - **service, endpoint or software occurrences, not hosts** |
| `"."` (`--count-hosts`) | root documents - **hosts**, deduplicated |
| `"host.services"` (`--count-services`) | a named intermediate level |

The four combinations, each verified against the equivalent search on a
16,100-host Catalyst SD-WAN Manager population, aggregating
`host.services.labels.value`:

| `count_by_level` | `filter_by_query` | `HONEYPOT` bucket | Equivalent search |
| --- | --- | --- | --- |
| `""` | true | 3,453 | none - occurrence count, not a host count |
| `"."` | **false** | **6,255** | `<query> and labels: "HONEYPOT"` -> 6,263 |
| `"."` | **true** | **2,018** | `host.services:(<constraint> and labels.value="HONEYPOT")` -> 2,013 |

Read that table carefully, because the middle two rows are the two questions you
will actually want to ask, and they differ by 3x:

- **`--count-hosts --no-filter-by-query`** reproduces a plain
  `<query> and <field>=<value>` search - "how many matching hosts have this value
  *anywhere* on them".
- **`--count-hosts`** alone (filter on) binds the value to the *same service* the
  query matched, reproducing
  `host.services:(<constraint> and <field>=<value>)` - "how many hosts carry this
  value on the service that made them match".

That second form is the important one and it is new leverage. Step 6 and step 8
repeatedly need a service-bound count to decide whether a tag or signal is
contaminated; previously that meant one search per candidate value. One
`--count-hosts` aggregation answers it for **every bucket key at once, for one
credit**. Reach for it before you write a loop of searches.

#### Buckets are not host counts unless you asked for host counts

At the default level a bucket counts *occurrences*, and the inflation is large.
Aggregating `host.services.software.vendor` over a 16,134-host population
returned `cisco: 35,774` - 2.22x - because each host contributed one entry per
tagged service. Quote that as a host count and you have overstated exposure by
more than double.

`--compare-levels` runs both levels and prints the per-key inflation factor, so
you can see at a glance whether a distribution you are about to report is
occurrence-based:

```bash
python utils/censys_aggregate.py host.services.software.vendor '<query>' --compare-levels
```

An inflation of exactly 1.00x means the default count *happens* to be a host
count - true for `host.services.port`, where a host has at most one service per
port. Do not generalize from that: `software.vendor`, `software.product` and
`labels.value` all inflate, because one service carries many of each.

**Buckets can legitimately sum to more than the population even at host level.**
A host with services on 443, 8443 and 22 is counted in three port buckets. So
`sum(buckets) > total_count` is expected overlap, not a bug and not evidence of
double-counting - the util prints `sum` and `other` next to the bucket count so
you can see it. What you must never do is *add* buckets together to get a host
count; to count the union of several values, run one search with an `or`.

#### Field aliases work in the query, not in the `field` parameter

This is the reconciliation of two rules that have both appeared in this skill in
contradictory forms. Verified on the same population:

| Where | Form | Result |
| --- | --- | --- |
| `field` parameter | `labels` | **422 `Field 'labels' not found`** |
| `field` parameter | `host.services.labels.value` | works |
| `field` parameter | `host.labels.value` | works - 1 bucket, `IPV6` |
| query / filter clause | `not labels: "HONEYPOT"` | works |
| query / filter clause | `not host.services.labels.value="HONEYPOT"` | works |

So: **always write the full field path in the `field` parameter** - aliases are
rejected outright there, loudly, with a 422. Inside the `query` string the alias
is fine and `labels:` is what `utils/censys_tsa.py` emits.

An earlier version of this skill claimed the `labels:` alias "silently returns 0
buckets in an aggregation" when used as a *filter*, and told you to rewrite it to
`host.labels.value`. **That was wrong and is removed** - it prescribed the one
clause that does nothing. The alias filters correctly; the 0-bucket observation
is explained by the next section. The grain of truth in the old rule was about
the `field` parameter, which is now stated above.

**If an aggregation returns 0 buckets, do not assume the field is empty - run a
positive control.** Re-run without the added clause. If the unfiltered
aggregation returns buckets and the filtered one returns none, the filter is
doing something you did not intend. When two filter forms disagree, establish
which one is the no-op before deciding which one is broken. This is the same
discipline step 4 demands of a 0-hit regex.

#### The `HONEYPOT` label is a SERVICE label, not a host label

This is the single most common way to build a honeypot filter that silently does
nothing. Verified as a controlled set:

| Query | Hits |
| --- | --- |
| `<query> and labels: "HONEYPOT"` | 6,263 |
| `<query> and host.services.labels.value="HONEYPOT"` | 6,267 |
| `<query> and host.labels.value: "HONEYPOT"` | **0 - wrong field** |
| `<query> and host.labels.value="HONEYPOT"` | **0 - wrong field** |

`host.labels.value` is a real, populated field, which is why the mistake is easy
to miss - it just carries different values. Aggregating it over that population
returns exactly one bucket, `IPV6`, at 10 hosts. The product and deception labels
live one level down, on the service:

```
host.services.labels.value  (--count-hosts, of 16,105 hosts):
  LOGIN_PAGE 15,842 · NETWORK 15,749 · HONEYPOT 6,255
```

`labels:` is an alias for the **service-level** field, so `labels: "HONEYPOT"`
and `host.services.labels.value:"HONEYPOT"` are equivalent - the small count gap
is index churn between calls. Both `:` and `=` work. `utils/censys_tsa.py`
appends the alias form, which is correct.

Censys labelled **39%** of that population as honeypots. If a honeypot clause
appears to remove nothing, you have almost certainly written `host.labels.value`
where you meant `host.services.labels.value` - check the field level before
concluding that Censys does not label the population.

**Honeypot exclusion is Censys's job.** Do not build bespoke honeypot detection -
service-count thresholds, foreign-title exclusions, ASN blocklists - into a TSA
base query. They are heuristics rather than product signatures, they are not
reproducible by whoever reads the report, and they demonstrably discard genuine
hosts. Rely on the `HONEYPOT` label that `utils/censys_tsa.py` already applies.
If a population still looks contaminated afterwards, say so in the caveats and
quantify it; do not encode a private filter in the query.
