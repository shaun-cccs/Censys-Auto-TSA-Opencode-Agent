<!--
Provenance: originally carved verbatim from the upstream censys-auto-tsa
SKILL.md (1497 lines). This copy is canonical for this kit.
Source lines: 1002-1220

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


# Step 8 - the deeper hunt

Owned by the `censys-deepdive` subagent.

## Quick card

**8a. Harvest** from the confirmed population, using the base query as the seed:
`tsa agg --suggest-fields '<base query>' -k 20`, then targeted favicon, title,
JARM and certificate aggregations - batched, not one per turn.

**8a-0. Before any of that, aggregate `host.services.protocol`.** Every other
signal in this reference is HTTP, TLS or certificate evidence. A decoded protocol
is a different evidence *layer*, and its structured sub-document
(`any_connect.groups`, `ike.*`, ...) beats any regex here because a parsed field
cannot be echoed by a host that merely mentions the string. Read the
sub-document with `tsa doc host --grep <protocol>`. **Aggregating ports is not
this check.**

**8a-bis. Hunt a unique identifier string.** Ranked best first:

1. a **self-identifying support or doc link** - the appliance names its own
   product line (`product=SMA%201000%20Series`), often with the build number
2. an **acquired-company or legacy brand name** - survives rebranding in SSO
   endpoints and redirect targets (`viptela` recovered +112 hosts)
3. a **quoted HTML attribute**, an internal codename, a product-specific cookie
   name, a custom header, a static asset path

Reject real English words and common technical terms; they collide.

**Empty harvest is positive evidence, not absence of it.** No title, no markup,
no favicon and a bare 301/302 is the *signature of a fronted deployment*. Enumerate
the redirect chain - every hop and the destination host of every hop - and read
records individually; at single-digit seed sizes narrative reading beats
aggregation outright.

**With a redirect signal, ask which END runs the product.** Decide by what the
token *names*, never by same-host versus cross-host:

- names the **destination's** product -> the emitting host is a client, do not
  count it. Measured: a Shibboleth path in `redirect_chain.path` returns 2,440
  hosts against 16 in the same-host `uri` field - 99% referral traffic
- names the **host's own** product or vendor -> count it, even across machines.
  `Location` matching `meraki\.com` returns 6,320, of which 4,452 carry a Cisco tag
- names a **third party** shared across vendors -> identifies neither end.
  `\.okta\.com` returns 10,030 hosts of no single product

**A neighbour is a gate, never a disjunct.** Require it to be observable at the
unauthenticated boundary. A signal that collapses to near-zero under a gate
indicts the gate - try two structurally different gates before abandoning it. And
**measure contamination before gating**: a signal that is already coherent must
ship as a plain disjunct, because gating a clean 225-host path took it to 0.

**"0 hosts outside" is circularity, not agreement.** Censys builds tags from the
very artifacts you would use as confirmation. Test both directions; if both are
~0, treat the pair as one signal and corroborate from a different layer - cert,
JARM, port, DNS.

**8b. Test every candidate in one call**, always subtracting the base:

```bash
tsa candidates '<base query>' '<cand 1>' '<cand 2>' '<cand 3>'
```

Read the titles it prints, not just the counts. Discard any candidate whose
incremental population is not coherently the product.

**8c-8e.** `or` the survivors onto the **intact** original, prefer `=` over `:`,
validate, re-run `tsa assess`, and report the delta. Classify every rejection as
**empirically closed** (queried, genuinely not there) or **role judgement** (set
aside as substrate, sibling or too generic) - the second must be re-opened when
the role changes, and anything never queried is *untested*, not rejected.

## The full procedure

GATE: the user-facing offer at the top of this step is owned by the
`censys-tsa` orchestrator, which asks via the `question` tool. The subagent is
invoked ONLY after the user has already said yes, so it starts at 8a and must
not re-ask. The `censys-tsa-auto` variant skips this step entirely.

### 8. Offer to dig deeper

After delivering the report, **always ask the user whether they want to go
deeper**. Censys product tagging covers only a fraction of exposed hosts, so a
tag-only TSA is a floor, not a ceiling. Use the `question` tool - do not ask in
plain prose:

> **Ownership note for this project:** this gate belongs to the `censys-tsa`
> orchestrator, which owns the conversation with the user. The
> `censys-deepdive` subagent is invoked only after the user has already
> accepted, so it begins at 8a below and must never re-ask. The
> `censys-tsa-auto` variant has the `question` tool denied and skips step 8
> entirely, reporting the baseline as a floor.

```
question: "The TSA above is based on <basis>. Want me to dig deeper and hunt for
           additional signatures (favicons, HTML titles, certs, banners, JARM)
           to widen the query beyond Censys tagging?"
choices:  ["Yes, dig deeper (Recommended)", "No, the current TSA is enough"]
```

Offer this regardless of which step produced the query. It matters most after a
step 2 tag-based TSA, but even an evidence-based fingerprint from step 3 usually
has room for another `or` clause.

If the user declines, stop. If they accept, run a deeper hunt:

**8a. Harvest signatures from the known-good population.** Use the TSA base
query itself as the seed and aggregate the discovery fields over it. These hosts
are confirmed instances, so whatever they have in common is a candidate
signature:

```bash
tsa agg --suggest-fields '<base query>' -k 20
```

Or target fields individually - favicon hash, HTML title, certificate subject,
JARM, banner, port, cookie names, URI paths:

```bash
tsa agg host.services.endpoints.http.favicons.hash_shodan \
  '<base query>' -k 20
tsa agg host.services.endpoints.http.html_title \
  '<base query>' -k 20
tsa agg host.services.jarm.fingerprint '<base query>' -k 10
```

**And the one that is not HTTP at all - do this first:**

```bash
tsa agg host.services.protocol '<base query>' --count-hosts -k 20
tsa doc host --grep any_connect     # read whatever protocol that named
```

**Worked failure - Cisco ASA/FTD.** A hunt ran five family workers over favicon,
title, certificate, JARM, path, header, cookie, redirect and release evidence.
Four of the five reported their family "exhausted"; three independently returned
"UDP 500 / IKE as a structural gate" as their top unexplored lead. Every one of
them missed `host.services.protocol="ANYCONNECT"`, whose `any_connect.groups`
field holds the ASA default tunnel-group name `DefaultWEBVPNGroup` - by itself
worth **+1,661 hosts** the published query lacked, roughly 1,500 of them untagged
in all three trees and invisible to every content signal in this file. The port
aggregations the workers *did* run (443, UDP 500) found nothing, because a port
number is not a decoded protocol. Two lessons: check the protocol layer before the
content layers, and treat unanimous convergence in worker leads as a directive.

**8a-bis. Hunt for a unique identifier string - the highest-value signal.**
Aggregations only surface values Censys already buckets. The strongest widening
signal is usually a string that is *unique to the product's implementation* and
would never appear anywhere else, searched directly in the HTTP body or banner.
These beat favicons and titles because they survive rebranding, custom themes,
and reverse proxies, and they carry essentially no false-positive risk.

Look for internal names the vendor never marketed but left in the code:

| Kind of string | Example |
| --- | --- |
| **Self-identifying support/doc link** | **the single best signal - the appliance names its own product line.** `product=SMA%201000%20Series` from the SonicWall portal's help link. See below. |
| Internal codename / build name | `fecru` - the FishEye+Crucible application name, in every install's paths and cookies |
| **Acquired-company / legacy brand name** | **survives rebranding in SSO endpoints, asset paths and redirect targets.** `viptela` for Cisco Catalyst SD-WAN Manager - Cisco acquired Viptela years earlier, yet the domain still appears in live SAML endpoints. Recovered +112 hosts the product's own name missed. |
| **Quoted HTML attribute** | ``body=~`id=\"login_left\"` `` - a vendor's own markup. Escape the quotes (see `tsa doc regex`); unquoted, the same token matches 36,017 unrelated login pages |
| Product-specific cookie name | `FESESSIONID`, `JSESSIONID` - match with ``host.services.endpoints.http.headers:(key="Set-Cookie" and value=~`FESESSIONID`)`` |
| Static asset or bundle path | `/s/.../_/download/resources/`, a versioned JS bundle name - identifies the **product** |
| **The same asset, taken by its hash** | **identifies the *release*.** A content-hashed name or cache-busting query string - `main.<app>.<contenthash>.css`, `bundle.js?<hash>` - changes between versions. That is a tier 2b signal, not a widening signal: read `tsa ref cve-workflow`. Do not improvise a version query from it, and do not read a failed guess at its format as proof the version is invisible |
| Custom or vendor HTTP header | `X-AUSERNAME`, `X-Forwarded-Server` values, vendor `Server` strings - query with `host.services.endpoints.http.headers:(key="X-AUSERNAME")` |
| Login-form field or JS variable | a uniquely named form input or JS global |
| Copyright / footer string | an exact vendor footer line |
| Error page wording | a verbatim product-specific error message |

**Rank a self-identifying string above an internal codename.** Login pages
routinely link to the vendor's documentation, and those URLs carry the product
line as a query parameter - `?category=Secure%20Remote%20Access&product=SMA%201000%20Series&version=12.5.0`.
This beats a codename on two counts: it names the product *the user asked
about* in the vendor's own words, so it needs no justification in the report,
and it **disambiguates sibling product lines** that share a codebase and every
other signal. The SonicWall SMA 1000 and SMA 100 are different appliances; the
help link separates them, an internal token does not. It often carries the
build number too, giving you a tier-2 version source for free. Grep a
known-good body for `product=`, `version=`, `category=` and `support`.

Their weakness is coverage, which brings us to the next rule.

**SSO-fronted instances are invisible to title and body fingerprints - check for
them explicitly.** An instance behind SAML or OIDC does not serve its own login
page at all. It returns a bare auto-submit form with **no `html_title` and none
of the product's markup**, so every title-based and body-markup-based signal
misses it, and often only the favicon remains. Example, confirmed genuine by
browsing to it:

```
IP 54.218.70.190, one service on 443, html_title: None
<body onload="document.forms[0].submit()">
  <form action="https://test-okta.viptela.com/app/cisco-viptela-b2b-poc_sdwanfabric.../sso/saml" method="post">
```

This bias matters because SSO-protected estates are usually the larger, better
run deployments - exactly the ones an exposure assessment should not silently
drop. Hunt them with the redirect target rather than the page content: the
vendor's or tenant's SSO domain, the acquired-company domain, or an
`/app/.../sso/saml` path. Aggregating `html_title` over the incremental
population is the check - a clean SSO population shows a handful of redirect
titles (`301 Moved Permanently`, `Redirecting...`, `Document Moved`) rather than
a long tail of unrelated products.

**The fronting layer is not always a cloud IdP.** The same reasoning covers an
on-premises access-management component, and very often that component is
**another product from the same vendor** - an access-manager WebGate, a web
dispatcher, a policy agent, an API gateway. Do not restrict this check to SAML
and OIDC tenants.

**An empty harvest is positive evidence, not absence of evidence. Never report a
seed as "signature-barren" on missing content alone.** No `html_title`, no body
markup, no favicon and a bare 301/302 is the *diagnostic signature of a fronted
deployment*, and it is the trigger condition for this whole section. When the
harvest comes back empty, the mandatory next move is to enumerate the redirect
chain in full - **every hop, and the destination host of every hop** - because the
evidence has moved out of the page and into the redirect. Aggregating a field
cannot find this: a hop to a *different* hostname is relational evidence, and a
field-by-field checklist has no cell for it. Read the confirmed records
individually and ask what each host talks to. At small seed sizes (single digits)
per-host narrative reading beats aggregation outright - aggregating `html_title`
over such a seed returns `302 Found` and teaches you nothing.

**With a redirect signal, ask which END of the redirect the product sits on.
Getting this backwards can invert a count almost entirely.** The rule above tells
you to hunt with the redirect target, and that is sound - but a redirect links two
machines, and the matched token tells you which one is running the product. Do not
decide this by same-host versus cross-host; decide it by **what the token names**:

- **The token names the DESTINATION's product - do not count the emitting host.**
  It is a client of the product, usually on unrelated infrastructure. Shibboleth
  IdP, measured: `redirect_chain.path` matching `/idp/profile/SAML2` returns
  **2,440** hosts while the same string in the same-host `uri` field returns
  **16** - roughly **99%** of the apparent population is referral traffic. The
  records are `moodle-admin-test.warwick.ac.uk` redirecting to
  `idp.warwick.ac.uk` and `uiscitrix.uis.edu` redirecting to `uisshibb1.uis.edu`.
  Every one is a Service Provider; the real IdPs are the *destinations*. Reporting
  2,440 would have counted Moodle and Citrix installs as Shibboleth.
- **The token names the HOST's OWN product or vendor - count it, even though the
  destination is a different machine.** An appliance redirecting to its vendor's
  cloud, or an SSO-fronted product posting to its own vendor tenant, is still the
  product. Measured: `Location` matching `meraki\.com` returns **6,320** hosts, of
  which **4,452** independently carry a Cisco vendor tag - genuine Meraki devices
  bouncing to the Meraki cloud dashboard. Cisco Catalyst SD-WAN Manager is the
  same shape: the acquired-company token `viptela` appears in the **body** the
  product itself serves (136 hosts), which is same-host content pointing at an
  external tenant. Discarding these as "cross-host" would throw away thousands of
  true positives.
- **The token names a THIRD-PARTY service shared across vendors - identifies
  neither end.** `Location` matching `\.okta\.com` returns **10,030** hosts of no
  single product. Useless as a disjunct - and precisely the neighbour-gate case
  below.

Use the field taxonomy as a verification aid, not as the rule: `endpoints.path`,
`endpoints.http.uri` and `body` are all **same-host** - the scanner requested or
received them from this host - whereas `Location` and `redirect_chain.path` may
describe another machine, so compare `redirect_chain.hostname` against the host's
own IP and certificate names before deciding which of the three cases you are in.

Two corollaries that keep this consistent with the gate rule below:

- **Gates are exempt from all of this.** A gate may name a third party or another
  machine freely, because it is evidence about the surrounding architecture rather
  than about what is installed here. In the Oracle Identity Governance case the
  product hop was self-referential (`<ip> -> <same ip> /identity/`) while the
  access-manager gate hop pointed at a different hostname - the correct shape is
  **the counted signal must identify this host's product; the filtering signal
  need not.**
- **A destination-naming match is still a pivot.** Those 2,440 SPs enumerate the
  hostnames of real IdPs, a genuinely useful discovery route into `host.dns.names`
  or certificate names. Use them to *find* the product; never add them to the
  total.

**Neighbour as gate: the fronting component is the gate, never the disjunct.**
A component the target is always deployed behind has high recall on the target
and almost no precision - the profile that makes it useless as an `or` clause
and ideal as an `and` gate (see `tsa ref cenql-rules` for the role triage).
Measured, on Oracle Identity Governance: the `/identity/` context root alone
matched 993 hosts (contaminated by Plex Media Server, SailPoint IdentityIQ,
Fischer Identity, Teldat); the vendor's access-manager WebGate redirect alone
matched 486 hosts (mostly a *different* product, the vendor's portal server,
with zero overlap with the confirmed population). Neither half is a fingerprint.
Their intersection was 6 hosts, 6/6 genuine, tripling a 3-host baseline. So:

- **Do not let "sibling product, keep disjoint" or "substrate" exclude a signal
  from gate duty.** Those labels are correct for a base disjunct and wrong for a
  gate. A disjointness requirement between the target and its neighbours applies
  to what you *count*, not to what you *filter with*.
- **Require the gate to be observable at the unauthenticated boundary** - in the
  same anonymous response the scanner already collected. This is what separates a
  working gate from a failed one. An app-server or proxy header sits *behind* the
  fronting layer and is only sometimes emitted, whereas an access-manager
  redirect must answer the anonymous request, because that is its entire
  function. Being a neighbour is not sufficient; revealing itself to an
  unauthenticated request is.
- **A signal that collapses to near-zero under a gate indicts the gate, not the
  signal.** The 993-host signal above went to 1 under an app-server gate and was
  written off as barren; under the access-manager gate it yielded 6. A correct
  gate on a real population leaves a plausible remainder, so near-zero means the
  gate is orthogonal to the target. Try at least two structurally different gates
  before abandoning a signal that has real hosts in it.
- **Declare the recall cost in the caveats.** A gated count is scoped to
  instances *that have that neighbour*, which is a real and directional bias -
  gating on one vendor's SSO silently excludes the same product behind any other.
  Check whether the survivors collapse into a few organisations before treating
  the gain as population growth: those 6 hosts were 2 organisations.
- **Never let the gate migrate into the base.** Drop the weak product-specific
  half and you are counting the neighbour - a different product, and in that
  example an 80x larger number.

**Corroboration must be causally INDEPENDENT of what it corroborates, and
"0 hosts outside" is the signature of circularity, not of agreement.** Censys
builds many tags by matching exactly the artifacts you would reach for as
confirmation - HTML title, `Server` header, banner, favicon. When the tag is
derived from the title, comparing them proves nothing: the check re-reports the
fingerprint and looks like a clean validation. Measured, on the FortiGate
appliance tag: `html_title: "ACME Access Only"` returns 81,406 hosts and
**0** of them fall outside `hardware:(vendor="fortinet" and product="fortigate")`,
while the tag exceeds the title by only ~40 hosts. Two populations that agree to
within 0.05% in both directions are not independent witnesses; one is almost
certainly the input to the other. Test it before believing an agreement:

```bash
tsa search '<signal> and not (<tag>)' --max-results 1   # 0 => signal may FEED the tag
tsa search '<tag> and not (<signal>)' --max-results 1   # also ~0 => near-identical
```

If both directions are ~0, treat the pair as one signal, not as confirmation, and
corroborate from a **different layer** instead - certificate subject, JARM, port,
or `host.dns.names` - since those are not inputs to an HTTP-content tag.

**Run the contamination check on TAG-based populations too, not only on evidence
signals.** The rule above about aggregating `html_title` before gating applies
equally to a step-2 tag query. It is what surfaces a tag whose population is
uniform in a way a real product estate never is, and it costs one aggregation.
Pair it with an ASN aggregation to separate a genuine dispersed estate from
shared infrastructure: the FortiGate population above spread across Comcast,
AT&T, Deutsche Telekom, Swisscom and a long tail, which is what a real appliance
fleet looks like, whereas concentration in one hosting or CDN ASN means you are
counting edge nodes rather than deployments.

**Measure the contamination BEFORE you gate. A signal that is already coherent
must be shipped as a plain disjunct, never gated.** Gating is a precision
instrument, so applying it to a signal that is already precise buys nothing and
costs recall. Order of operations: aggregate `html_title` over the broad signal
and read a handful of records *first*, then gate only what the contamination
actually justifies. Measured counter-example, deliberately tested against the
rule above: PeopleSoft is untagged by Censys in all three trees, its own
`PS_TOKEN`/`SignOnDefault` cookie fingerprint finds 29 hosts, and its `/psp/`
context root finds 225 - a 7.8x under-count by the direct fingerprint, with the
population dominated by bare redirect stubs. That is the fronted-deployment
signature, and the redirect-hop enumeration duly confirmed the residual genuine
(`/psp/fscm/EMPLOYEE`, `/psp/hcprd/`, state-government hostnames). But the path
was **already clean**, so gating it actively destroyed the finding: an
access-manager gate took 225 to **0**, and an F5 gate took it to 109, discarding
over half of a confirmed population. Near-zero after gating can indict the
*decision to gate at all*, not merely the choice of gate - if the ungated signal
was coherent, stop gating and keep it.

**A structured multi-segment path is self-gating.** `/psp/<site>/<PORTAL_NODE>/`
carries the product's own fixed vocabulary in later segments - PeopleSoft's
`EMPLOYEE`, `SUPPLIER`, `CUSTOMER` nodes, its `cmd=login` parameter, its `/psc/`
sibling root. 160 of those 225 hosts matched such a marker. Path *structure*
supplies the specificity a gate would otherwise provide, so test the deeper
segments before reaching for a neighbour: a first segment that looks generic in
isolation is often unambiguous two segments in. This is the same lesson as
quoting an HTML attribute rather than gating a bare token - prefer making the
signal itself more specific over conjoining a second signal.

**Check what a candidate MISSES, not only what it adds - and check it by
version.** Step 8b tests candidates by incremental gain. When you are choosing
or replacing a *base* signal, run the comparison the other way as well:

```bash
tsa agg host.services.hardware.version \
  '<broad signal> and not (<precise signal>)' --count-hosts -k 20
tsa agg host.services.endpoints.http.html_title \
  '<broad signal> and not (<precise signal>)' --count-hosts -k 20
```

If the missed hosts are coherently the product, the precise signal is
under-counting - and the miss is frequently **biased toward old firmware**,
because self-identifying help links, favicons and modern titles are added in
later releases and simply do not exist on legacy builds. The SMA 1000 help link
misses 307 hosts skewed to 12.3 / 12.1 / 11.4 - precisely the end-of-support
population a TSA exists to surface. A fingerprint that is 100% precise and
silently blind to every unpatched appliance is worse than a slightly looser one.
Recover the gap with gated disjuncts rather than accepting the clean number.

**Replacing a fingerprint is a symmetric-difference measurement.** Never compare
two candidate base queries by total count alone - two queries can agree on a
total while disagreeing on hundreds of hosts. Run both directions, together:

```bash
tsa batch --count '<new> and not (<old>)' \
          --count '<old> and not (<new>)' \
          --count '<new>' --count '<old>'
```

Report both figures. "2,630 vs 2,620" hides that the new query gained 54 and
lost 44; those two numbers are what tell you the swap was safe.

Where do you find them? Read a confirmed host's HTTP body. Pull a few known-good
hosts from the base query, look at what is in the response, and pick out tokens
that are meaningless outside this product:

```bash
tsa search '<base query>' --max-results 3 --format json \
  -o /tmp/known_good.json
grep -o -E '[a-z]{4,12}' /tmp/known_good.json | sort | uniq -c | sort -rn | head -40
```

Then test the candidate string as a body or banner match:

```bash
tsa search \
  'host.services.endpoints.http.body=~`[Ff]ecru` and not (<base query>)' \
  --max-results 5 --format table
```

Prefer a token that is a made-up word, a vendor-internal abbreviation, or a
concatenation - `fecru`, `zmcallbackuri`, `owaauth`. Reject any real English
word or common technical term; those collide badly. Apply the same 8b test to
these as to any other candidate: if the incremental population is not coherently
the product, discard it.

**8b. Test each candidate in isolation, excluding the original population.**
A candidate is only worth adding if it finds hosts the base query missed *and*
those hosts are genuinely the product. Always subtract the base query so you are
looking purely at the incremental hits.

**Test every candidate in one call.** The tests are independent of each other, so
`tsa candidates` runs them all concurrently and prints, per candidate, the
incremental host count *and* the titles of those incremental hosts - the count
and the evidence you judge it by, together:

```bash
tsa candidates '<base query>' \
  'host.services.endpoints.http.favicons.hash_shodan="<hash>"' \
  'host.services.endpoints.http.html_title="Log in to FishEye"' \
  'host.services.endpoints.http.body=~`[Ff]ecru`'
```

An increment of **0** is ambiguous - either the base query already covers those
hosts, or the candidate matches nothing at all. `--totals` counts each candidate
on its own as well and tells the two apart. It costs one extra call per
candidate, so use it when the answer matters.

The longhand, one candidate at a time, when you need to vary the witness field or
read raw records:

```bash
tsa search \
  '<candidate signal> and not (<base query>)' \
  --max-results 5 --format table

tsa agg host.services.endpoints.http.html_title \
  '<candidate signal> and not (<base query>)' -k 20
```

Read the buckets before believing the count. Generic names collide - a "fisheye"
signal pulls in IP cameras, an "atlas" signal pulls in unrelated software. If
the incremental hits are dominated by unrelated titles, organizations, or ports,
**discard the candidate**. Only keep signals whose incremental population is
coherently the target product.

**8c. Concatenate the surviving signals to the original query with `or`.**
Keep the original base query intact as the first disjunct and append each
validated signature, wrapping the whole thing in parentheses:

```
(<original base query> or <signal 1> or <signal 2> or <signal 3>)
```

For example, widening a tag-only query:

```
(host.services.software:(vendor="atlassian" and product="fisheye")
 or host.services.endpoints.http.favicons.hash_shodan="<hash>"
 or host.services.endpoints.http.html_title="Log in to FishEye")
```

Prefer exact `=` over tokenized `:` for the added signals - tokenized matching on
a common word is the main source of false positives when widening. Bind port and
content evidence to the same service with nested syntax where relevant.

**8d. Validate the widened query, then re-run the TSA.**

```bash
tsa search '<widened query>' --max-results 5 --format table
tsa assess '<widened query>' --product '<Product Name>'
```

**8e. Report the delta.** Present the deeper result as an addition to the
original, never as a replacement. State:

- The widened query and its platform URL.
- New global and Canada counts, and the delta versus the tag-only TSA.
- Each signature you added, what evidence justified it, and its incremental
  contribution.
- Each candidate you tested and **rejected**, with the reason - this is what
  makes the widened number defensible. **Classify every rejection as one of two
  kinds, because they are not equally final:**
  - **empirically closed** - it was queried and the population is genuinely not
    there (a 0 with a passing positive control, or an incremental population that
    is coherently *not* the product). Safe to declare settled.
  - **role judgement** - it was set aside as substrate, as a sibling product, as
    too generic, or as untested. This is a judgement about the role it would
    play, not a measurement of the data, and it **must be re-opened the moment
    the role changes** - most often when a signal rejected as a disjunct becomes
    a candidate gate.

  Never hand another agent an undifferentiated "do not reintroduce these" list.
  Mixing the two kinds hardens a role judgement into a fact and makes the blind
  spot permanent across the handoff. Mark anything you never actually queried as
  **untested with no count**, and never let it read as rejected.
- A revised confidence statement: widening trades precision for recall, so say
  explicitly whether the new count is a better estimate or a loose upper bound.
- **Total credit consumption across the session** - the second TSA run costs
  another ~2 credits, and every aggregation and validation search in the deep
  dive costs 1 each, so give the running total, not just the last run's figure.

Give the user both numbers side by side - the conservative tag-based count and
the widened count - so they can choose which to cite.
