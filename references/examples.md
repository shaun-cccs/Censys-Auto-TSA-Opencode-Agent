<!--
Provenance: originally carved verbatim from the upstream censys-auto-tsa
SKILL.md (1497 lines). This copy is canonical for this kit.
Source lines: 1367-1497

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

## Worked example - tier 2b, a version Censys cannot see

The target names a version, so step 0b applies even with no CVE. Censys tags the
product but parses no version for it, and the authoritative version endpoint is
not crawled - which looks like tier 3 and is not. Measured on Jellyfin 10.11.0.

```bash
# 0b tier 1. does Censys parse a version? Run the control before believing a 0.
tsa agg host.services.software.version \
  'host.services.software:(vendor="jellyfin" and product="media_server")' --count-hosts -k 30
# -> 0 buckets. Control with --no-filter-by-query returns 2000, all of them OTHER
#    software on those hosts (OpenSSH 9.6p1, nginx 1.24.0). Mechanism control over
#    the f5/nginx tag returns 494 version buckets, so the 0 is real. Tier 1 is out.

# 0b tier 2. is a version string visible in stored evidence?
tsa search '<base> and host.services.endpoints.http.body=~`10\.1[01]\.[0-9]`' -n 1
# -> 89 of 84,620 hosts. The web client does not print its version. Tier 2 is out.

# 0b tier 2b step 2. read the vendor's BUNDLER CONFIG before judging any token.
#   jellyfin-web@v10.11.0 webpack.common.js:
#     MiniCssExtractPlugin  filename: '[name].[contenthash].css'   <- content-derived
#     HtmlWebpackPlugin     hash: true                             <- per-BUILD hash
#   and src/index.html ships no <script>/<link> at all, so both exist only in the
#   built output. Guessing the format instead costs a wrong conclusion:
#   body=~`bundle\.js\?v\=10\.` returns 0 - because the real form is ?<20 hex>,
#   never ?v=<version>. A failed format guess is NOT evidence of absence.

# 0b tier 2b step 1. official artifacts for the target AND both sides of it.
#   Stream-extract one file; do not download the whole 131 MB tarball.
curl -sL "$REPO/portable/stable/v10.11.11/any/jellyfin_10.11.11.tar.gz" \
  | tar -xzO --wildcards --occurrence=1 '*jellyfin-web/index.html' > index.html
#   Check provenance: an npm 'jellyfin-web' 10.11.0 exists and is an IMPOSTOR -
#   wrong maintainer, published 10 months before the real release, no dist.

# 0b tier 2b step 3 + gate. content hash vs build hash, tested across packagings.
#   Same release 10.11.11 from the portable tarball and the official Docker image:
#     sha256 of index.html      3f6b19d4...  vs  d06008c6...   <- DIFFER (per build)
#     ?<compilation hash>       4c3e5ec6...  vs  3cf5acc8...   <- DIFFER (per build)
#     main.jellyfin.<hash>.css  f725276386e5b19afe0c  in BOTH  <- SAME (per release)
#   So body_hash_sha256 is a build key, and the stylesheet hash is the release key.
#   (body_hash_sha256 does match the shipped file byte-for-byte - it is exact, just
#   not packaging-independent.)

# 0b tier 2b step 5. bind the release signal to the SAME service as the product.
tsa assess \
  'host.services:(software:(vendor="jellyfin" and product="media_server") and endpoints.http.body=~`main\.jellyfin\.0196d1aa92641204d3e6\.css`)' \
  --product 'Jellyfin Media Server 10.11.0'
# -> 312 global, 14 Canada, out of 84,616 exposed instances of all versions.

# 0b tier 2b step 6. uniqueness in BOTH directions before quoting it.
#   adjacent releases carry different hashes: 10.10.7 7d6eaeb0..., 10.11.1-4
#   28c12127..., 10.11.5 9c6fd4f2..., 10.11.6 7eaf27d2..., 10.11.7-11 f7252763...
tsa search '<target hash> and not (<base>)' -n 3
# -> 1 host. Negligible collision; the 312 is if anything one short.
```

Two things this example exists to teach. **The response body is truncated at
2,048 bytes but the index is not** - `body_size` was 5,331 and the asset names sit
past the cut, yet ``body=~`jellyfin\.bundle\.js` `` still matches 69,109 hosts, so
a hash obtained from an artifact is searchable even though you cannot read it back
out of a record. And **a shared stylesheet scopes a family, not a release**: five
releases share `f725276386e5b19afe0c`, so report that bucket as 10.11.7-11 rather
than pretending to split it. Classify the result as a *release inference*, never as
a confirmed version, and say which releases the signal cannot separate.
