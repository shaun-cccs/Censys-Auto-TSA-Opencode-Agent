<!--
Provenance: originally carved verbatim from the upstream censys-auto-tsa
SKILL.md (1497 lines). This copy is canonical for this kit.
Source lines: 861-940

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


# Step 4 - CenQL rules for drafting the base host query

Shared reference. Read before writing ANY query, in any step.
Also run `tsa doc cenql` and, for any `=~` pattern,
`tsa doc regex`.

## Quick card

**Count from `host.*` only.** `web.*`, `cert.*` and tag fields are pivots.

**Bind criteria to the same object.** `host.services: (port=443 and
endpoints.http.html_title="...")`. A plain `and` of two top-level fields only
requires both values *somewhere* on the host. Aliases (`product`, `vendor`,
`labels`, `banner`, ...) are invalid **inside** nested queries.

**`:` is tokenized and case-insensitive; `=` is exact and case-sensitive.** When
widening with `or`, prefer `=` - a tokenized common word is the main source of
false positives.

**The four silent-zero traps.** Each returns an empty result that reads as "not
exposed", with no error:

| Trap | Wrong | Right |
| --- | --- | --- |
| inline regex flags | ``value=~`(?i)jetty` `` -> **0** | ``value=~`[Jj]etty` `` -> 199,548 |
| unescaped `"` in regex | ``body=~`id="login_left"` `` -> 1 | ``body=~`id=\"login_left\"` `` -> 2,558 |
| fieldless CIDR | `"163.127.5.0/24"` -> **0** (full-text) | `host.ip="163.127.5.0/24"` -> 8 |
| unquoted CIDR | `host.ip=163.127.5.0/24` -> 422 | quote it, always, in every `ip_range` field too |

**Any regex or CIDR query returning 0 needs a positive control before you believe
it.** Re-run it against a population known to contain the string. If the control
is also 0 the query is malformed, not the data. Check in order: unescaped `"`,
inline flag, misplaced `^`/`$`, case.

**A quoted HTML attribute is one of the best fingerprints available.** Bare
`login_left` matches 36,017 generic login pages; ``id=\"login_left\"`` matches
2,558 with a single hardware bucket. Escape before you gate.

**Name a signal's role before rejecting it - disjunct, gate, or exclusion.** A
disjunct adds hosts, so it needs **precision**. A gate adds none and only filters,
so it needs **recall** and may be arbitrarily broad, name a third party, or
describe another machine. "Too generic to count" and "useless as a gate" are
different verdicts.

**Regex is not metered differently** - 1 credit per API action, same as any
search or aggregation. Twenty regex candidates cost about twenty credits. Prefer
aggregations for precision and speed, not to save money.

## The full rules

### 4. Draft the base host query

Rules:

- **Count from `host.*` fields only.** `web.*`, `cert.*`, and tag fields are for
  pivoting and enrichment, never for the TSA counts.
- Follow `tsa doc cenql`. For anything using `=~`, read
  `tsa doc regex` first - escaping, anchor placement and the
  supported operator set are all sources of silent 0-hit results. Key points:
  - `:` is tokenized and case-insensitive; `=` is exact and case-sensitive.
  - **Always quote a CIDR block, and always give it a field.** Those are two
    separate mistakes with two different symptoms, and the second is the
    dangerous one. Measured on a subnet containing two known hosts:
    `host.ip="163.127.5.0/24"`, ``host.ip=`163.127.5.0/24` `` and
    `host.ip: "163.127.5.0/24"` all return 8. Unquoted,
    `host.ip=163.127.5.0/24` fails loudly with **HTTP 422 `Invalid character:
    '/'`** - definitive, not worth retrying, and 422 is deliberately absent from
    `RETRYABLE_STATUS`. But **fieldless and quoted, `"163.127.5.0/24"` returns a
    silent 0**, because a fieldless term is a full-text search and no document
    contains that literal string. The failure path to watch for is the sequence:
    unquoted CIDR 422s, you add quotes to fix it, you dropped the field along the
    way, and the silent 0 reads as "nothing exposed in that subnet". A bare
    fieldless CIDR 422s as well - entering a CIDR in the search bar with no field
    is a **web-UI affordance that does not exist in the API**, whatever
    `tsa doc cenql` implies.
  - **The quoting rule is universal across fields, including the `ip_range`
    ones.** `tsa doc cenql`'s type table shows `ip_range` with an unquoted
    example (`125.8.0.0/13`), and that example is misleading: measured,
    `host.autonomous_system.bgp_prefix=163.127.4.0/22` 422s while the quoted,
    backticked and `:` forms each return 47. The other `ip_range` field is
    `host.whois.network.cidrs`. Note also that these fields hold a CIDR as a
    *value* to match exactly - they do not do containment, so they answer "which
    hosts are in this announced prefix", not "which prefixes contain this host".
  - The trap underneath all of this is that the adjacent syntax is *legal*: a
    single bare address needs no quotes (`host.ip=163.127.5.42` returns 1),
    because `ip` is its own type, while a CIDR block is parsed as a string, and
    unquoted strings must match `[a-zA-Z][a-zA-Z0-9._-]*` - which admits neither
    `/` nor a leading digit. When in doubt, quote it; quoting a single IP is
    harmless. And per the positive-control rule below, a CIDR query returning 0
    needs one before you believe it: `bgp_prefix="125.8.0.0/13"` returns 0
    because no indexed host announces that prefix, which is indistinguishable
    from a syntax error until you test a prefix you know is populated.
  - Bind criteria to the *same* object with nested syntax:
    `host.services: (port=443 and endpoints.http.html_title="...")`.
    Plain `and` only requires both values somewhere on the record.
  - Aliases (`product`, `vendor`, `cpe`, `labels`, `vulns`, `banner`, ...) cannot
    be used inside nested queries.
  - Use backtick regex with `=~` for prefix/substring matches on tokenized
    fields, e.g. ``host.services.banner=~`^220 ProFTPD` ``.
  - **Never use inline regex flags.** `(?i)`, `(?s)` and `(?is)` are unsupported
    and return **0 hits silently** - no error, just an empty result that looks
    like "not exposed". Regex is case-sensitive, so express case-insensitivity
    with character classes: ``[Ff]ish[Ee]ye``, not ``(?i)fisheye``. Verified:
    ``value=~`Jetty` `` returns 199,543 hosts while ``value=~`(?i)jetty` ``
    returns 0.
  - **Escape `"` inside regex - forgetting it silently returns 0.** CenQL's
    escape set is `.` `+` `()` `{}` `[]` `"` `*` `?` `:` `\` `/` `^` `$`, and
    that applies inside backticks too. ``body=~`class="ewcontent"` `` returns
    **0** while ``body=~`class=\"ewcontent\"` `` returns **1,577**;
    ``body=~`id="login_left"` `` returns **1** while
    ``body=~`id=\"login_left\"` `` returns **2,558**. Do not conclude that a
    quoted pattern "doesn't work" - escape it.
  - **Escaped HTML attributes are among the best fingerprints available.** The
    bare token `login_left` matches 36,017 hosts of generic login pages; the
    same string as markup, ``body=~`id=\"login_left\"` ``, matches 2,558 with a
    single `hardware.product` bucket. Quoting an attribute converts a useless
    generic word into a vendor-specific signature. Reach for `id=\"…\"` and
    `class=\"…\"` before you fall back to gating a bare token.
  - **Any regex returning 0 needs a positive control** before you believe it -
    re-run it against a population known to contain the string. If the control
    is also 0, the regex is malformed, not the data. Check, in order: an
    unescaped `"` or other special character; an inline flag; a `^`/`$` that is
    not the first or last character; and case.
  - **Regex queries are not metered differently.** On the enterprise plan
    Censys charges 1 credit per API action with **no difference in cost between
    standard and advanced (regex) queries** - measured at 1 credit each. Prefer
    aggregations first for precision and speed, not to save money: an
    aggregation also costs 1 credit. Testing twenty regex candidates costs
    about twenty credits, the same as twenty ordinary searches.
  - **Gate a generic token instead of discarding it.** A token that collides
    outside the vendor is often still usable when bound to a vendor-specific
    server header or port. ``body=~`ewcontent` `` alone pulls in unrelated
    MIXpbx management pages, but
    ``body=~`ewcontent` and host.services.endpoints.http.headers:(key="Server" and value=~`^SMA/`)``
    is clean. The converse holds too: a vendor `Server` header alone is usually
    honeypot-dominated and only becomes trustworthy when paired with content
    evidence. Neither half is a fingerprint; the conjunction is. Prefer a gated
    disjunct over dropping a signal that was recovering real hosts. Try
    escaping the quotes first, though - a properly quoted attribute is often
    precise enough to need no gate.
  - **Every signal has three possible roles: disjunct, gate, exclusion. Name the
    role before you reject it.** A `or` clause adds hosts directly to the count,
    so it needs **precision**. An `and` gate contributes no hosts at all and only
    filters, so it needs **recall** - it may be arbitrarily over-broad at zero
    cost provided it is present on nearly every real instance. Those are opposite
    requirements, so the same signal is routinely worthless in one role and ideal
    in the other. "Too generic to count" therefore does **not** imply "useless";
    it is the normal profile of a good gate. When you discard a signal, record
    which role you tested it in. Rejecting it as a disjunct is not rejecting it,
    and a rejection list that does not name the role will be read by the next
    agent as final.
  - **Pick the gate your known false positives cannot satisfy.** Gate selection
    is constructive, not lucky. Enumerate what is actually polluting the broad
    signal, then ask what none of those contaminants could ever have. A generic
    path polluted by unrelated IAM products and media servers is rescued by an
    authentication component none of them can sit behind. A broad signal is only
    "barren" once you have listed its contaminants and failed to find something
    structurally impossible for all of them.
  - **Every host count written into this kit's references is a dated
    measurement, not a constant - trust the ratio, never the absolute.** Censys
    scan coverage moves, so the illustrative figures here drift, sometimes by
    a lot. Re-measured against the numbers recorded in these references: bare
    `login_left` was 36,017 and is now 212,659; the quoted form
    ``id=\"login_left\"`` was 2,558 and is now 6,224; ``value=~`Jetty` `` was
    199,543 and is now 198,488. What survived unchanged is every *invariant* the
    numbers were cited to demonstrate - quoting an attribute still cuts the
    population by well over an order of magnitude (212,659 to 6,224), and the
    inline-flag trap ``(?i)jetty`` still returns exactly **0**. Cite these
    figures as evidence of direction and magnitude; re-measure before quoting
    any of them as a current count in a report.
  - HTTP headers are nested: bind key and value together with
    ``host.services.endpoints.http.headers:(key="Server" and value=~`[Jj]etty`)``.
    Key-only presence checks work too. `Set-Cookie` values are queryable with
    `=~` (not `=`), even though aggregations display them as `<REDACTED>` — so
    cookie names like `FESESSIONID` are usable fingerprints.
- Combine several weak signals with `or` when no single tag exists, e.g.
  favicon hash `or` HTML title `or` banner regex. Wrap the whole thing in
  parentheses - `tsa assess` does this too, but be explicit.
- Verify every field name with `tsa doc host --grep <field>`. Invalid fields fail
  or silently return nothing.
- Port alone is never sufficient; always pair it with content evidence.
- **Software and hardware tags are always vendor-qualified and nested:**
  `host.services.software:(vendor="<vendor_name>" and product="<product_name>")`
  or `host.services.hardware:(vendor="<vendor_name>" and product="<product_name>")`.
  A bare `product=` match, or a top-level `vendor= and product=` pair, is not
  acceptable for a TSA count.
- **Check the hardware tree for appliances.** If the target is a physical or
  virtual appliance and the software tree is empty, aggregate
  `host.services.hardware.product` before concluding the product is untagged.
- **Never assume the hardware and software trees agree - measure the difference
  both ways.** Agreement varies enormously by product, so which tree you query
  can change the count by an order of magnitude. Measured: Fortinet FortiGate is
  perfectly coextensive - `hardware:(vendor="fortinet" and product="fortigate")`
  and `software:(vendor="fortinet" and product="fortios")` both return 81,445
  hosts with **0** difference in either direction, so either tree serves. But
  Check Point's `hardware.product="firewall-1"` returns 149,535 hosts of which
  only 15,308 carry any Check Point *software* tag - about **90% are
  hardware-tagged only** - and of 231,672 hosts tagged `connect_vpn` in hardware,
  75,144 have no software tag at all. Run
  `'<hardware query> and not (<software query>)'` and its converse before
  choosing, and say in the report which tree the count came from.
- **A hardware tag is good enrichment and often a bad base query.** Where the
  tag over-matches (step 2's over-counting check), keep an evidence fingerprint
  as the base and `and` the tag on only to scope by version.
