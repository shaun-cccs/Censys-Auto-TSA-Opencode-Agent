<!--
Provenance: carved verbatim from censys-auto-tsa/SKILL.md (1497 lines),
the canonical skill in `/home/jovyan/14 - Learning/Censys Auto TSA`.
Source lines: 942-1000

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


# Steps 5, 6, 7 - validate, run the TSA, report

Owned by the `censys-tsa` orchestrator, not by a subagent. Step 6 is the only
step that produces the headline counts.

### 5. Validate before counting

```bash
cd "/home/jovyan/14 - Learning/censys-tsa-opencode"
python utils/censys_query.py '<base query>' --max-results 5 --format table
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
cd "/home/jovyan/14 - Learning/censys-tsa-opencode"
python utils/censys_tsa.py '<base query>' --product '<Product Name>'
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
   `Credits used` block that `utils/censys_tsa.py` prints. Where a deep dive
   (step 8) followed, give the total across every TSA run in the session, and
   count the aggregations too - each costs 1 credit, they are not free. Only
   `cve_lookup.py` and the credit endpoints themselves cost nothing. Never omit
   this section, and never estimate the figure - quote what the tool measured.
   If credit tracking errored, say so rather than leaving it out.
7. **Caveats** - fingerprint confidence, whether version is remotely observable,
   and where the query may over- or under-count. For a CVE-driven TSA, always
   state whether the number is confirmed-vulnerable, version-scoped, or
   product-exposure-with-unknown-patch-status, and quantify the coverage gap
   between the `vulns.id` count and the product population where both exist.
