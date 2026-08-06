<!--
Provenance: carved verbatim from censys-auto-tsa/SKILL.md (1497 lines),
the canonical skill in `/home/jovyan/14 - Learning/Censys Auto TSA`.
Source lines: 1002-1220

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


# Step 8 - the deeper hunt

Owned by the `censys-deepdive` subagent.

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
cd "/home/jovyan/14 - Learning/censys-tsa-opencode"
python utils/censys_aggregate.py --suggest-fields '<base query>' -k 20
```

Or target fields individually - favicon hash, HTML title, certificate subject,
JARM, banner, port, cookie names, URI paths:

```bash
python utils/censys_aggregate.py host.services.endpoints.http.favicons.hash_shodan \
  '<base query>' -k 20
python utils/censys_aggregate.py host.services.endpoints.http.html_title \
  '<base query>' -k 20
python utils/censys_aggregate.py host.services.jarm.fingerprint '<base query>' -k 10
```

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
| **Quoted HTML attribute** | ``body=~`id=\"login_left\"` `` - a vendor's own markup. Escape the quotes (see `docs/censys_regex_language.md`); unquoted, the same token matches 36,017 unrelated login pages |
| Product-specific cookie name | `FESESSIONID`, `JSESSIONID` - match with ``host.services.endpoints.http.headers:(key="Set-Cookie" and value=~`FESESSIONID`)`` |
| Static asset or bundle path | `/s/.../_/download/resources/`, a versioned JS bundle name |
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

**Check what a candidate MISSES, not only what it adds - and check it by
version.** Step 8b tests candidates by incremental gain. When you are choosing
or replacing a *base* signal, run the comparison the other way as well:

```bash
python utils/censys_aggregate.py host.services.hardware.version \
  '<broad signal> and not (<precise signal>)' --count-hosts -k 20
python utils/censys_aggregate.py host.services.endpoints.http.html_title \
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
total while disagreeing on hundreds of hosts. Run both directions:

```bash
python utils/censys_query.py '<new> and not (<old>)' --max-results 1   # gained
python utils/censys_query.py '<old> and not (<new>)' --max-results 1   # lost
```

Report both figures. "2,630 vs 2,620" hides that the new query gained 54 and
lost 44; those two numbers are what tell you the swap was safe.

Where do you find them? Read a confirmed host's HTTP body. Pull a few known-good
hosts from the base query, look at what is in the response, and pick out tokens
that are meaningless outside this product:

```bash
cd "/home/jovyan/14 - Learning/censys-tsa-opencode"
python utils/censys_query.py '<base query>' --max-results 3 --format json \
  -o /tmp/known_good.json
grep -o -E '[a-z]{4,12}' /tmp/known_good.json | sort | uniq -c | sort -rn | head -40
```

Then test the candidate string as a body or banner match:

```bash
python utils/censys_query.py \
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
looking purely at the incremental hits:

```bash
python utils/censys_query.py \
  '<candidate signal> and not (<base query>)' \
  --max-results 5 --format table

python utils/censys_aggregate.py host.services.endpoints.http.html_title \
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
python utils/censys_query.py '<widened query>' --max-results 5 --format table
python utils/censys_tsa.py '<widened query>' --product '<Product Name>'
```

**8e. Report the delta.** Present the deeper result as an addition to the
original, never as a replacement. State:

- The widened query and its platform URL.
- New global and Canada counts, and the delta versus the tag-only TSA.
- Each signature you added, what evidence justified it, and its incremental
  contribution.
- Each candidate you tested and **rejected**, with the reason - this is what
  makes the widened number defensible.
- A revised confidence statement: widening trades precision for recall, so say
  explicitly whether the new count is a better estimate or a loose upper bound.
- **Total credit consumption across the session** - the second TSA run costs
  another ~2 credits, and every aggregation and validation search in the deep
  dive costs 1 each, so give the running total, not just the last run's figure.

Give the user both numbers side by side - the conservative tag-based count and
the widened count - so they can choose which to cite.
