<!--
Provenance: originally carved verbatim from the upstream censys-auto-tsa
SKILL.md (1497 lines). This copy is canonical for this kit.
Source lines: 416-689, 836-859

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


# Steps 1, 2, 3, 3b - probe, tagging, creative fingerprinting, web research

Owned by the `censys-fingerprint` subagent.

## Quick card

1. **Probe.** One call, not five: `tsa probe '<1-2 word seed>'`. It samples the
   seed host-scoped, buckets `product` in **all three** tag trees -
   `host.services.software`, `host.services.hardware`, `host.operating_system` -
   and buckets `host.services.protocol`. Appliances are routinely absent from
   `software` and fully tagged under `hardware`; checking one tree is the
   commonest way to conclude "untagged" wrongly. Add `--wide` for vendors, ports,
   titles and favicon hashes.
2. **A bucket names the target in any tree -> step 2.** Nothing does -> step 3.
   **A named protocol -> read its structured sub-document first**, before any
   content regex: `tsa doc host --grep <protocol>`.
3. **Step 2, tagging exists.** Confirm the vendor, then bind vendor and product
   to the *same* object:
   `host.services.software:(vendor="x" and product="y")` - never a bare
   `product=`, which matches a host running someone else's product too. Then two
   checks, both mandatory:
   - read the tag's own evidence (`tsa search '<tag query>' --max-results 1
     --format json`): a tag whose only evidence is `favicons.hash_*` is worth
     exactly as much as a favicon, so treat it as a candidate, not a base query
   - test for over-counting: aggregate titles and ports over
     `<tag query> and not labels: "HONEYPOT" and not (<evidence fingerprint>)`.
     A remainder of unrelated products means the tag is inflated - fall back to
     step 3 and keep the tag for version enrichment only. Confirm any
     over-counting verdict at service scope (`--count-hosts`, keep
     `filter_by_query`) before acting on it.
4. **Step 3, no usable tag.** Build the fingerprint from raw evidence. Sweep with
   `tsa agg --suggest-fields '<seed>'` or target fields directly, then **invert**:
   take the dominant favicon / title / JARM / cert organisation, use it as the
   query, and aggregate back on product, hardware and OS to check the population
   is coherent. Favicons: always `favicons.hash_shodan`, and **always quote the
   value** - a leading minus 422s unquoted.
5. **Step 3b, web research.** Last resort, capability-gated, never a way to find
   signals you have not looked for in Censys. Never contact an assessed host.

Batch the independent calls in each step; the only thing that must be serial is
what genuinely depends on a previous answer.

## The full procedure

Steps 1-3 below are the discovery core. The dense aggregation-semantics
subsections that originally sat inside step 3 are now a reference of their own:
run `tsa ref aggregation-semantics` before any aggregation, and
`tsa ref cenql-rules` before writing any query.

### 1. Probe Censys first with a simple full-text search

Do **not** start with web research. Start with a cheap full-text probe using a
simple **1-2 word** search - the product or vendor name, nothing clever - then
aggregate the tag trees over it with `filter_by_query` enabled (the default, so
the buckets are scoped to what actually matched).

**Censys has three parallel tag trees, not one.** `software` is only the first
of them, and appliances are routinely absent from it while being fully tagged
under `hardware`. Always check all three before concluding "no tagging":

| Tree | Nested query form | Typically tags |
| --- | --- | --- |
| `host.services.software` | `host.services.software:(vendor=… and product=…)` | applications, web servers, libraries |
| `host.services.hardware` | `host.services.hardware:(vendor=… and product=…)` | appliances, VPN concentrators, cameras, routers |
| `host.operating_system` | `host.operating_system.product` / `.vendor` / `.version` | host OS (top level, not per-service) |

Each has the same sub-fields - `vendor`, `product`, `version`, `cpe`, `part`,
`source`, `confidence`, `life_cycle.end_of_life`, and an `evidence` block. The
CPE `part` letter tells you which tree a value belongs to: `a` = application,
`h` = hardware, `o` = operating system.

```bash
# All of step 1 in ONE call: the seed sample, every tag tree, and the decoded
# protocols, concurrently.
tsa probe '"MOVEit"'

# Add vendors, ports, titles and favicon hashes when you can already tell this
# is heading for step 3 (5 more calls):
tsa probe '"MOVEit"' --wide
```

`tsa probe` is the preferred form because the sweep is five independent calls and
five separate turns is where a TSA loses its time. The equivalent longhand, when
you need to vary something it does not expose:

```bash
# 1-2 word full-text seed: does the name appear anywhere in host records?
tsa search '"MOVEit" and host.ip: *' --max-results 5 --format table

# Check ALL THREE trees before deciding tagging is absent - in one message, not
# three turns
tsa agg host.services.software.product '"MOVEit"' -k 30
tsa agg host.services.hardware.product '"MOVEit"' -k 30
tsa agg host.operating_system.product '"MOVEit"' -k 30

# And the fourth layer, which is not a tag tree: what did Censys DECODE?
tsa agg host.services.protocol '"MOVEit"' -k 30
```

## The fourth layer - decoded protocols

**Tagging and HTTP content are two evidence layers, not all of them.** Censys
decodes a set of named service protocols and stores a **structured
sub-document** for each one it recognises - `host.services.any_connect`,
`host.services.ike`, and so on. Those fields outrank every banner, body and
title regex you could write, because they are parsed values rather than strings
that any host may echo. `tsa probe` therefore buckets
`host.services.protocol` on every run, and when a protocol you care about
appears you **read its sub-document before writing a content pattern**:

```bash
tsa doc host --grep any_connect
```

**A port aggregation is not this check.** Ports and protocols look
interchangeable and are not: a port number is a guess about what is listening,
a decoded protocol is Censys telling you what answered.

**Worked failure to learn from - Cisco ASA/FTD.** An assessment ran four
fingerprint workers across all three tag trees and five deep-dive workers across
every HTTP/TLS/certificate signal family. It aggregated ports - including 443 and
UDP 500 - and concluded that a large part of the population was untagged and
reachable only through contaminated web content. Every worker missed
`host.services.protocol="ANYCONNECT"` and its `any_connect.groups` field, where
the single default value `DefaultWEBVPNGroup` identified **1,661 exposed VPN
head-ends the final query did not have** - about 1,500 of them carrying no tag in
any of the three trees. The field was documented in `tsa doc host` the whole
time. The lesson is not "check ANYCONNECT"; it is that "no tag and no clean
content signal" is a conclusion you may not reach until you have looked at what
Censys decoded.

**A bare full-text seed is not host-scoped.** `"MOVEit Transfer"` on its own
matches web-property and certificate records too, and they have no IP, no
location and no services - so a sample of them tells you nothing about exposed
hosts, and a count of them is not a host count. Add `and host.ip: *` when you
search a bare string, which is what `tsa probe` does for you and prints. The tag
tree aggregations need no such clause: bucketing a `host.*` field is host-scoped
by the field itself.

Broad seeds will pull in other products - that is expected and fine. You are
looking for a bucket that names the product the user asked about.

Interpretation:

- A bucket in **any** tree clearly names the target product -> **tagging exists,
  go to step 2** and confirm the vendor before querying.
- All three trees are empty, generic (`nginx`, `Apache httpd`, `Microsoft IIS`),
  or unrelated -> tagging is absent or too thin. Go to step 3 and build a
  fingerprint yourself.
- `host.services.protocol` names a protocol the product speaks -> **read that
  protocol's structured sub-document before anything else in step 3.** This is
  independent of the three trees: a decoded protocol on an otherwise untagged
  host is the strongest fingerprint available, and it survives the honeypot
  contamination that ruins body and title signals.

**Worked failure to learn from - SonicWall SMA 1000.** Aggregating only
`host.services.software.product` over `"sonicwall"` returned five buckets
(`http`, `virtual_office`, `ssl-vpn`, `email_security`,
`universal_management_appliance`) and none of them was the SMA 1000, so the
product looked entirely untagged. It was not: it is tagged under **hardware** as
`host.services.hardware:(vendor="sonicwall" and product="secure_mobile_access")`
with a parsed `hardware.version` (`12.5`, `12.4`, `12.3`, `11.4`, ...) and a
CPE of `cpe:2.3:h:sonicwall:secure_mobile_access:12.5:*:*:*:*:*:*:*`. Checking
only the software tree turned a tier-1 version-scoped assessment into a
mistaken "version not remotely observable" conclusion. Anything that is an
appliance - VPN gateway, firewall, load balancer, NAS, camera, printer, ICS
device - should be assumed to live in the `hardware` tree first.

If the 1-word seed is hopelessly noisy, try the 2-word form (e.g.
`"MOVEit Transfer"`) before concluding anything. Keep these probes to a couple
of requests.

### 2. If tagging exists, rely on it

When step 1 surfaced a matching bucket in any tag tree, first confirm the
vendor, then build the base query on the **vendor + product pair**, nested in
whichever tree the bucket came from:

```bash
# Which vendor owns that product tag? One clean bucket = unambiguous.
tsa agg host.services.software.vendor \
  'host.services.software.product="n-central"' -k 10

tsa agg host.services.port \
  'host.services.software:(vendor="n-able" and product="n-central")' -k 20

# hardware tree - same shape, same rules
tsa agg host.services.hardware.vendor \
  'host.services.hardware.product="secure_mobile_access"' -k 10
```

**Always pair product with vendor, bound to the same object:**

```
host.services.software:(vendor="<vendor_name>" and product="<product_name>")
host.services.hardware:(vendor="<vendor_name>" and product="<product_name>")
```

Never count on a bare `host.services.software.product="<name>"`. Product names
are not globally unique across vendors, and a plain `and` of two top-level
fields only requires both values to appear *somewhere* on the host - it can
match a host running vendor A's product plus vendor B's unrelated software. The
nested `host.services.software:( ... )` form binds both criteria to the same
software entry. Inside the nested block use the bare field names `vendor` and
`product` (not the `host.services.software.` prefix, and not the top-level
`vendor` / `product` aliases, which are invalid inside nested queries). The same
applies verbatim to `host.services.hardware:( ... )`.

`host.operating_system` is **top level, not per-service**, so there is no
nesting to do - query `host.operating_system.product` and
`host.operating_system.vendor` directly.

Add `version` or `cpe` inside the same nested block when you need to scope
further, e.g. a CVE-affected range:

```
host.services.software:(vendor="n-able" and product="n-central" and version="2024.1")
```

Still sanity-check coverage: compare the tagged count against the full-text seed
count. If full text returns far more hosts, the tag under-counts - widen with an
`or` clause from step 3 and say so in the report. Then go to step 4.

**Read the tag's own evidence before you trust or reject it - it is the cheapest
check available and it costs one search.** Every `software`, `hardware` and
`operating_system` entry carries `confidence` and an `evidence[]` array whose
`data_path` names the field the tag was derived from. Pull one raw record and
look:

```bash
tsa search '<tag query>' --max-results 1 --format json -o /tmp/one.json
```

A tag derived from a single weak signal is a lookup, not a fingerprint:

```
cisco     / catalyst_sd_wan_manager  conf 0.75  evidence: [endpoints.http.favicons.hash_sha256]
nextgen   / mirth_connect            conf 0.75  evidence: [http.html_title]
eclipse   / jetty                    conf 0.25  evidence: [http.headers.server]
oracle    / application_server       conf 0.25  evidence: [http.headers.server]
wordpress / wordpress                conf 0.25  evidence: [http.body, path]
```

Two things to take from a record like that. First, a `product` tag whose only
evidence is `favicons.hash_*` is worth exactly as much as the favicon - and
favicons are shared, rebranded and copied, so treat such a tag as a candidate
signal rather than a base query. Second, **one service can carry many software
tags at once** - five in the example above - so "this host is tagged X" is a far
weaker statement than it appears, and a tag population will always contain
services whose dominant identity is some other product.

Where a tag is single-evidence, name that in the report: "Censys assigns this tag
from `<data_path>` at confidence `<n>`" is a concrete, checkable justification
for building an evidence-based fingerprint instead.

**Sanity-check the tag for over-counting too, and do it before you trust it.**
Hardware tags in particular are inferred from weak evidence and attract
emulating honeypots that Censys's `HONEYPOT` label does not always catch. Take
the tag population, subtract a known-good evidence fingerprint, and aggregate
titles and ports over the remainder:

```bash
tsa agg host.services.endpoints.http.html_title \
  '<tag query> and not labels: "HONEYPOT" and not (<evidence fingerprint>)' \
  --count-hosts --no-filter-by-query -k 20
tsa agg host.services.port \
  '<tag query> and not labels: "HONEYPOT" and not (<evidence fingerprint>)' \
  --count-hosts --no-filter-by-query -k 12
```

If the remainder is dominated by unrelated titles and a scattering of thousands
of random high ports (or port `0`), the tag is inflated and **must not** be used
as the base query. That is exactly what the SonicWall `secure_mobile_access`
hardware tag does: 10,287 hosts, but the non-honeypot incremental over a
confirmed fingerprint is FortiManager, FortiSwitch, Confluence, ASUS routers and
AXIS cameras. Fall back to step 3 for the base query and keep the tag purely for
version enrichment.

**Confirm any over-counting verdict at service scope before acting on it.** The
aggregations above count a host once for any title anywhere on it, so a host
legitimately running several products contributes all of them and the population
looks more mixed than it is. Re-run the title aggregation **with**
`filter_by_query` (drop `--no-filter-by-query`, keep `--count-hosts`), which
binds the title to the same service that carried the tag:

```bash
tsa agg host.services.endpoints.http.html_title \
  '<tag query>' --count-hosts -k 20
```

Each bucket is then equivalent to the search
`host.services:(software:(vendor="<v>" and product="<p>") and endpoints.http.html_title="<title>")`,
for one credit instead of one search per title. Measured on one population, the
unbound form returned 13,312 hosts for a foreign title where the service-bound
form returned 1,760 - a 7.6x difference, and the difference between rejecting a
usable tag and keeping it. Read one raw record too, to see the per-service
structure for yourself:

```bash
tsa search '<query>' --max-results 1 --format json -o /tmp/one.json
```

Even when coverage looks complete, a tag-only query is the most likely to be
under-counting. Make sure you offer the step 8 deep dive after reporting.

### 3. No usable tag - get creative inside Censys

Stay in Censys. Use aggregations to reverse-engineer a fingerprint from raw
evidence: banners, HTML titles, favicon hashes, certificate subjects, JARM,
headers, cookie names, URI paths, ports.

`tsa agg` wraps the Censys aggregation API (max **2000** buckets):

```python
res = sdk.global_data.aggregate(
    search_aggregate_input_body={
        "field": "<field_name>",
        "number_of_buckets": 2000,
        "query": "<CenQL query>",
        "filter_by_query": True,
        "count_by_level": ".",   # "." = count hosts; "" = deepest nested level
    }
)
```

Start from a broad seed - the full-text name, an associated string, a banner
regex, or a CVE - then bucket fields to find what those hosts have in common:

```bash
# Sweep the standard fingerprint-discovery fields in one go
tsa agg --suggest-fields '"MOVEit Transfer"' -k 20

# Or target a single field
tsa agg host.services.endpoints.http.favicons.hash_shodan \
  '"MOVEit Transfer"' -k 20
tsa agg host.services.endpoints.http.html_title \
  'host.services.vulns.id="CVE-2023-34362"' -k 30
tsa agg host.services.cert.parsed.subject.organization \
  '"MOVEit Transfer"' -k 20
```

**Favicons: always use the Shodan hash.** Censys exposes four favicon hashes -
`hash_shodan`, `hash_sha256`, `hash_md5`, `hash_phash`. Prefer
`host.services.endpoints.http.favicons.hash_shodan`: it is the mmh3 hash Shodan
uses, so the value is portable - you can paste it straight into Shodan
(`http.favicon.hash:<value>`), match it against public favicon-hash IOC lists,
and hand it to the user as a signature that works outside Censys. The other
three are Censys-only and buy you nothing extra. It is a **signed decimal
integer**, and CenQL rejects a bare leading minus with
`422 Invalid character: '-'`, so **always quote the value** - quoting is safe for
positive hashes too, and keep the minus sign:
`host.services.endpoints.http.favicons.hash_shodan="-886778564"` (verified: 927
hosts; unquoted the same query 422s). Only fall back
to `hash_sha256` if the Shodan hash is absent for the population you are
fingerprinting, and say so in the report if you do.

Useful fields to bucket: `host.services.port`, `host.services.protocol`,
`host.services.labels.value`, `host.services.software.product`,
`host.services.software.cpe`, `host.services.hardware.product`,
`host.services.hardware.vendor`, `host.services.hardware.version`,
`host.services.hardware.cpe`, `host.operating_system.product`,
`host.operating_system.version`, `host.services.endpoints.http.html_title`,
`host.services.endpoints.http.favicons.hash_shodan`,
`host.services.cert.parsed.subject.organization`,
`host.services.cert.parsed.subject.common_name`, `host.services.jarm.fingerprint`,
`host.autonomous_system.organization`, `host.location.country`.

Run the hardware and OS fields against your candidate fingerprint even when you
built it without them - they are the cheapest available check that the
population is the product you think it is, and they frequently hand you a parsed
version you would otherwise have had to regex out of a body. Aggregating
`host.services.hardware.product` over a confirmed SMA 1000 fingerprint returns a
single bucket, `secure_mobile_access`, at 2,635 of 2,624 hosts - a near-perfect
1:1 corroboration that no title or favicon could have given.

Then invert: take the dominant favicon hash, title, JARM, or certificate
organization and use it as the query, aggregating back on
`host.services.software.product` to confirm the population is coherent. Iterate
until the fingerprint is both precise (few false positives in sampled hits) and
broad (count is not obviously truncated by missing tags).

### 3b. Last resort - web research, with the user's approval

Only if steps 1-3 fail to produce a defensible fingerprint. **Ask the user for
approval before doing any web search**, e.g. "Censys tagging and aggregation
didn't identify this product - may I search the web for its fingerprint
details?" Do not browse without an explicit yes. Approval to research the web
does **not** authorize contacting assessed hosts: browse only public vendor,
source, advisory, package, registry, and documentation resources.

If approved, establish:

- Vendor and exact product name, and how a banner/HTTP response spells it.
- Default ports and protocols; HTTP, TLS, or custom protocol.
- Distinguishing strings: HTML `<title>`, login page text, `Server` /
  `X-Powered-By` / custom headers, cookie names, banner prefixes, URI paths,
  JavaScript bundle names, copyright footers.
- TLS certificate hints: subject organization, common name patterns, self-signed
  issuer strings used by the appliance.
- For a CVE: affected product, affected version range, vendor advisory, and
  whether the version is observable remotely.
- CPE strings (`cpe:2.3:a:vendor:product:...`).

Record every source you used; cite them in the final report. Then return to
step 3 and turn those strings into Censys queries and aggregations.
