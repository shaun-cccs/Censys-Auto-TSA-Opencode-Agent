<!--
Provenance: originally carved verbatim from the upstream censys-auto-tsa
SKILL.md (1497 lines). This copy is canonical for this kit.
Source lines: 1367-1497

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


# Worked examples

Three end-to-end illustrations. Load on demand when a step is ambiguous; they
are not part of the required reading for any single step.

## Worked example - an untagged product

```bash
# 1. simple 1-2 word full-text seed, then a scoped aggregation
tsa search '"MOVEit"' --max-results 5 --format table
tsa agg host.services.software.product '"MOVEit"' -k 30

# 2. no matching product bucket -> sweep discovery fields
tsa agg --suggest-fields '"MOVEit Transfer"' -k 20

# 3. tagging is thin -> pivot to the dominant favicon hash and confirm
tsa agg host.services.endpoints.http.html_title \
  'host.services.endpoints.http.favicons.hash_shodan="<hash>"' -k 20

# 4. build a multi-signal query and validate
tsa search \
  '(host.services.endpoints.http.favicons.hash_shodan="<hash>" or host.services.endpoints.http.html_title: "MOVEit Transfer")' \
  --max-results 5 --format table

# 5. run the TSA
tsa assess \
  '(host.services.endpoints.http.favicons.hash_shodan="<hash>" or host.services.endpoints.http.html_title: "MOVEit Transfer")' \
  --product 'Progress MOVEit Transfer'
```

Produces the platform query plus:

- Global: `(...) and not labels: "HONEYPOT"`
- Canada: `(...) and not labels: "HONEYPOT" and host.location.country="Canada"`

## Worked example - a tagged product

```bash
# 1. simple full-text seed, then a scoped aggregation
tsa search '"N-central"' --max-results 5 --format table
tsa agg host.services.software.product '"N-central"' -k 30
# -> "n-central" bucket present: tagging exists

# 2. confirm the vendor, then query the vendor+product pair
tsa agg host.services.software.vendor \
  'host.services.software.product="n-central"' -k 10
# -> single bucket "n-able"

# 3. check the tag isn't under-counting against an independent signal
tsa search \
  'host.services.endpoints.http.html_title: "N-able N-central" and not host.services.software.product="n-central"' \
  --max-results 3 --format table
# -> 0 hits: tag coverage is complete, no `or` widening needed

# 4. run the TSA on the nested vendor+product query
tsa assess \
  'host.services.software:(vendor="n-able" and product="n-central")' \
  --product 'N-able N-central'
```

Then report, and ask the user whether to dig deeper (step 8). If they say yes:

```bash
# 8a. harvest signatures from the confirmed population
tsa agg --suggest-fields \
  'host.services.software:(vendor="n-able" and product="n-central")' -k 20
# -> a dominant favicon hash and a recurring login-page title

# 8b. test a candidate in isolation, subtracting the known population
tsa search \
  'host.services.endpoints.http.favicons.hash_shodan="<hash>" and not host.services.software:(vendor="n-able" and product="n-central")' \
  --max-results 5 --format table
tsa agg host.services.endpoints.http.html_title \
  'host.services.endpoints.http.favicons.hash_shodan="<hash>" and not host.services.software:(vendor="n-able" and product="n-central")' -k 20
# -> incremental hits are coherently N-central: keep the signal

# 8c/8d. `or` the survivor onto the original query, validate, re-run the TSA
tsa assess \
  '(host.services.software:(vendor="n-able" and product="n-central") or host.services.endpoints.http.favicons.hash_shodan="<hash>")' \
  --product 'N-able N-central (widened)'
```

Report both counts side by side, plus every candidate you rejected and why.

## Worked example - a CVE

```bash
# 0. retrieve the record and read it - cve.org plus NVD
tsa cve CVE-2024-21762
# -> Fortinet FortiOS / FortiProxy, out-of-bounds write, CVSS 9.6, in CISA KEV.
#    Read the affected-version text yourself; do not assume the vendor and
#    product strings match Censys tags.

# 1. fingerprint the product in Censys as usual
tsa agg host.services.software.product '"FortiOS"' -k 30
tsa agg host.services.software.vendor \
  'host.services.software.product="fortios"' -k 10
# -> vendor "fortinet"

# 0b. measure the coverage gap before quoting anything
tsa search 'host.services.vulns.id="CVE-2024-21762"' --max-results 1
# -> 18 hosts flagged
tsa search \
  'host.services.software:(vendor="fortinet" and product="fortios")' --max-results 1
# -> 81,232 hosts tagged. The tag covers ~0.02% of the population: it is a floor.

# 0b tier 1. does Censys parse the version for this product?
tsa agg host.services.software.version \
  'host.services.software:(vendor="fortinet" and product="fortios")' --count-hosts -k 30
# -> only 7.2.1 / 7.2.2 / 7.2.3, 41 hosts total. Version coverage is also thin,
#    so a version-scoped count is a second floor, not the answer. Fall to tier 2
#    and hunt the build string in banners and bodies, or report tier 3.

# count on whichever basis you can defend, and label it
tsa assess --cve CVE-2024-21762                      # confirmed vulnerable
tsa assess \
  'host.services.software:(vendor="fortinet" and product="fortios" and version<="7.2.2")' \
  --product 'Fortinet FortiOS <= 7.2.2'                              # version scoped
tsa assess \
  'host.services.software:(vendor="fortinet" and product="fortios")' \
  --product 'Fortinet FortiOS (exposure, patch status unknown)'      # product exposure
```

Give the user the numbers side by side with their bases named - 18 confirmed
vulnerable, 27 running an observably affected build, 81,232 exposed with unknown
patch status - rather than picking one and calling it "the" answer. Then report
the CVE context (severity, KEV status, source URL) and the credit consumption,
and offer the step 8 deep dive as always.
