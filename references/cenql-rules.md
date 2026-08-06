<!--
Provenance: carved verbatim from censys-auto-tsa/SKILL.md (1497 lines),
the canonical skill in `/home/jovyan/14 - Learning/Censys Auto TSA`.
Source lines: 861-940

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


# Step 4 - CenQL rules for drafting the base host query

Shared reference. Read before writing ANY query, in any step.
Also read `docs/censys_query_language.md` and, for any `=~` pattern,
`docs/censys_regex_language.md`.

### 4. Draft the base host query

Rules:

- **Count from `host.*` fields only.** `web.*`, `cert.*`, and tag fields are for
  pivoting and enrichment, never for the TSA counts.
- Follow `docs/censys_query_language.md`. For anything using `=~`, read
  `docs/censys_regex_language.md` first - escaping, anchor placement and the
  supported operator set are all sources of silent 0-hit results. Key points:
  - `:` is tokenized and case-insensitive; `=` is exact and case-sensitive.
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
  - HTTP headers are nested: bind key and value together with
    ``host.services.endpoints.http.headers:(key="Server" and value=~`[Jj]etty`)``.
    Key-only presence checks work too. `Set-Cookie` values are queryable with
    `=~` (not `=`), even though aggregations display them as `<REDACTED>` — so
    cookie names like `FESESSIONID` are usable fingerprints.
- Combine several weak signals with `or` when no single tag exists, e.g.
  favicon hash `or` HTML title `or` banner regex. Wrap the whole thing in
  parentheses - `utils/censys_tsa.py` does this too, but be explicit.
- Verify every field name by grepping the host field file. Invalid fields fail
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
- **A hardware tag is good enrichment and often a bad base query.** Where the
  tag over-matches (step 2's over-counting check), keep an evidence fingerprint
  as the base and `and` the tag on only to scope by version.
