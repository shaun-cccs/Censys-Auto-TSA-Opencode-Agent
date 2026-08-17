<!--
Provenance: originally carved verbatim from the upstream censys-auto-tsa
SKILL.md (1497 lines). This copy is canonical for this kit.
Source lines: 942-1000

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


# Steps 5, 6, 7 - validate, run the TSA, report

Owned by the `censys-tsa` orchestrator, not by a subagent. Step 6 is the only
step that produces the headline counts.

## Quick card

**5. Validate before counting.** Sample the query - together with any competing
variant, in one call:

```bash
tsa batch --sample '<base query>' --count '<variant A>' --count '<variant B>'
```

Are the hits really the product? Tighten on false positives; widen if the count
is implausibly low against the seed. Validation ends at Censys and public
research - **never connect to a matching host.**

**6. Run the TSA.**

```bash
tsa assess '<base query>' --product '<Product Name>'
```

It appends `not labels: "HONEYPOT"` to both counts and the country clause to the
second, and reports measured credits. Do not add either clause yourself.
`--country <name>` changes the second scope.

**7. Report.** Seven things must be *known*: product summary · fingerprint
rationale naming the step that produced the query (and, for a CVE, the counting
basis: vulnerability-tag, version-scoped or product-exposure-only) · the base
query · global count · country count · **measured** credits, never estimated ·
caveats covering fingerprint confidence, version observability, and where the
query over- or under-counts.

**That list is what goes in the written report, not what you print.** The
terminal form is the compact block defined in your own agent prompt: product,
one or two sentences, the baseline query with both counts, the widened query and
delta if a deep dive ran, one `Basis:`/`Credits:` line, at most four one-line
caveats. Never print the honeypot or country variants, and never print a platform
URL.

## The full reference

### 5. Validate before counting

```bash
tsa search '<base query>' --max-results 5 --format table
```

Inspect the hits: are they really the product? If false positives appear,
tighten. If the count looks implausibly low versus the full-text seed, widen
with another `or` clause. Pivot through `web.*` / `cert.*` when helpful - find
the vendor's certificates, then come back to hosts via
`host.services.cert.fingerprint_sha256` or the certificate common name.
Validation ends at Censys and public research: never connect to matching hosts
to confirm a title, endpoint, version, certificate, or protocol response.

### 6. Run the TSA

```bash
tsa assess '<base query>' --product '<Product Name>'
```

The script appends `not labels: "HONEYPOT"` to both counts and
`host.location.country="Canada"` to the country count. Do not add those clauses
to the base query yourself.

Flags: `--country <name>` (default `Canada`), `--format json`, `-o results.json`,
`-v`, `--no-credits`.

By default the run also reports the Censys credits it consumed (typically 2 -
one per count), measured from the org credit balance before and after. Pass
`--no-credits` to skip that measurement.

### 7. Report

1. **Product summary** - what it is, vendor, what it exposes; CVE ID, severity,
   KEV status, affected versions, and advisory if CVE-driven. Cite the CVE
   source URL (cve.org or NVD) actually used, and any web research sources.
2. **Fingerprint rationale** - which step produced the query: CVE record
   (step 0), version derivation (step 0b), Censys tagging (step 2),
   evidence-based fingerprint (step 3), or web-informed fingerprint (step 3b) -
   plus what the aggregations showed. For a CVE, state the **counting basis**:
   vulnerability-tag, version-scoped, or product-exposure-only.
3. **Platform query** - the base CenQL query and its `platform.censys.io` URL.
4. **Global TSA** - host count excluding honeypots, with query and URL.
5. **Canada TSA** - host count excluding honeypots, with query and URL.
6. **Censys credit consumption** - **always include this section.** Report the
   credits the run consumed and the balance before and after, straight from the
   `Credits used` block that `tsa assess` prints. Where a deep dive
   (step 8) followed, give the total across every TSA run in the session, and
   count the aggregations too - each costs 1 credit, they are not free. Only
   `tsa cve` and the credit endpoints themselves cost nothing. Never omit
   this section, and never estimate the figure - quote what the tool measured.
   If credit tracking errored, say so rather than leaving it out.
7. **Caveats** - fingerprint confidence, whether version is remotely observable,
   and where the query may over- or under-count. For a CVE-driven TSA, always
   state whether the number is confirmed-vulnerable, version-scoped, or
   product-exposure-with-unknown-patch-status, and quantify the coverage gap
   between the `vulns.id` count and the product population where both exist.
