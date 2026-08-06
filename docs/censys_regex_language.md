# Regex in CenQL

Reference for the `=~` operator in Censys Platform queries. Source:
<https://docs.censys.com/docs/platform-regex-cenql> (retrieved 2026-08-05),
supplemented with behaviour verified against the live API from this repository.

Read this alongside `censys_query_language.md` before writing any regex.

## The operator

Use `=~` to match a pattern instead of an exact value. **`=~` is
case-sensitive.** There is no case-insensitivity switch — express it with
character classes (`[Ff]ish[Ee]ye`), never with an inline flag.

Regex queries are "advanced queries", available only on Censys Starter or
enterprise plans. **On enterprise they cost the same as any other query - 1
credit.** Censys states there is no difference in cost between standard and
advanced queries, and a measured `=~` search on this org's plan deducted
exactly 1 credit. Do not avoid regex on cost grounds; the reasons to prefer an
aggregation first are precision and speed, not price. (The old "8 credits each"
figure applies to legacy Starter pricing and is not what this repository pays.)

## Delimiters and escaping — the most common source of silent zeros

A pattern may be wrapped in **backticks** (a raw string) or in **double
quotes**. If you use double quotes you must **double-escape** special regex
characters.

Inside either delimiter, `\` escapes these characters:

```
.  +  ()  {}  []  "  *  ?  :  \  /  ^  $
```

**`"` is on that list.** A double quote inside a pattern must be written `\"`
even in a backtick-delimited raw string. Forget it and the query returns **0
hits with no error** — indistinguishable from "this product is not exposed".

Verified against the SonicWall SMA 1000 population:

| Pattern | Hits |
| --- | --- |
| ``body=~`class="ewcontent"` `` | **0** |
| ``body=~`class=\"ewcontent\"` `` | **1,577** |
| ``body=~`id="login_left"` `` | **1** |
| ``body=~`id=\"login_left\"` `` | **2,558** |
| ``body=~`login_left` `` (no quotes at all) | 36,017 |

This matters far more than it looks. Matching HTML attributes is one of the best
fingerprinting techniques available, because `id=\"login_left\"` is a specific
piece of one vendor's markup while the bare token `login_left` is a generic CSS
name shared by tens of thousands of unrelated login pages. Escaping the quotes
took a signal from unusable (36,017 hosts, ~93% noise) to a near-perfect
fingerprint (2,558 hosts, single `hardware.product` bucket). **Do not abandon a
quoted pattern that returns 0 — escape it and try again.**

Note that `=` and `%` are *not* on the escape list and work literally, which is
why a URL-encoded fragment such as ``body=~`product=SMA%201000%20Series` ``
needs no escaping at all.

## Anchors

Regex in CenQL is **not anchored** — a pattern matches if it appears anywhere in
the field value. Use `^` and `$` to anchor, but note the restriction: **they may
only appear as the first and last characters of the pattern.** You cannot anchor
mid-alternation.

| Query | Matches | Does not match |
| --- | --- | --- |
| ``web.hostname=~`\w{3}\.censys\.\w{3}` `` | `docs.censys.com`, `mail.censys.com.mx`, `www.censys.biz` | `app.censys.io` |
| ``web.hostname=~`^\w{3}\.censys\.\w{3}$` `` | `www.censys.com`, `app.censys.com`, `go2.censys.com` | `docs.censys.com`, `mail.censys.com.mx` |

## Supported operators and assertions

| Operator | Use |
| --- | --- |
| `\` | Escapes `.` `+` `()` `{}` `[]` `"` `*` `?` `:` `\` `/` `^` `$` |
| `.` | Any character |
| `+` | Preceding character one or more times |
| `*` | Preceding character zero or more times |
| `()` | Group — e.g. `(org\|com\|net\|biz\|xyz)`, `(exe\|py\|msi\|jar)` |
| `\|` | Alternation |
| `[]` | Any one character in the set; `-` for a range; leading `^` negates. `c[^e]nsys` matches `cansys` and `c0nsys`, not `censys` |
| `{}` | Repetition count. `c[^e]{3}nsys` matches `caaansys`. `e{2,4}` matches 2–4 `e` characters |
| `^` | Start-of-input assertion (first character only) |
| `$` | End-of-input assertion (last character only) |

## Character classes

| Class | Equivalent |
| --- | --- |
| `\w` | `[A-Za-z0-9_]` |
| `\W` | `[^A-Za-z0-9_]` |
| `\d` | `[0-9]` |
| `\D` | `[^0-9]` |
| `\s` | `[\t-\n\r ]` — space, tab, form feed, line feed, Unicode spaces |
| `\S` | `[^\t-\n\r ]` |

## What is NOT supported

- **Inline flags.** `(?i)`, `(?s)`, `(?is)` are absent from the operator table
  and return **0 hits silently**. Verified: ``value=~`Jetty` `` returns 199,543
  hosts, ``value=~`(?i)jetty` `` returns 0.
- **Lookarounds, backreferences, non-greedy quantifiers, `\b`.** None appear in
  the documented operator set. Treat anything beyond the tables above as
  unsupported until proven otherwise with a positive control.

## The positive-control rule

Every documented failure mode above produces **zero hits and no error message**.
A 0-hit regex is therefore ambiguous: it means either "not present in the data"
or "your pattern is malformed". You cannot tell which by looking.

So: **any regex returning 0 must be re-run against a population known to contain
the string** before you believe it. If the control also returns 0, the pattern
is broken — check, in order:

1. An unescaped `"` (or `.` `/` `:` `(` `[` `{` `*` `?` `+` `^` `$` `\`).
2. An inline flag such as `(?i)`.
3. A `^` or `$` that is not the first or last character.
4. Case — `=~` is case-sensitive; use `[Ff]oo`, not `(?i)foo`.

## Escaping in double-quoted patterns

The two delimiters are not interchangeable in escaping depth. Censys's own
example of a proxy-detection query uses double quotes with `.*,.*`, while the
Google-impersonation example needs `".*\\.google\\..*"` — a *doubled* backslash
for what would be a single `\.` in backticks.

**Prefer backticks.** One level of escaping is easier to reason about, and it is
what every example in `SKILL.md` uses. Reserve double quotes for patterns you
are copying verbatim out of Censys documentation.

## Worked examples from the Censys docs

```
cert.names=~`.*\..*\.example\.com$`

host.services.endpoints.http.headers:(key="X-Forwarded-For" and value=~".*,.*")

web.cert.parsed.issuer_dn=~`^C=\w{2},\s+ST=[a-z0-9]{8},\s+L=[a-z0-9]{8},\s+O=[a-z0-9]{8},\sOU=[a-z0-9]{8},\sCN=[a-z0-9]{8}$`

web.hostname=~`.*\.okta.com` and web.labels.value="LOGIN_PAGE" and web.endpoints.http.status_code="200"
```

## Fingerprinting patterns that work well

```bash
# HTML attribute - escape the quotes, and precision improves by an order of magnitude
host.services.endpoints.http.body=~`id=\"login_left\"`

# URL-encoded query parameter - no escaping needed, = and % are literal
host.services.endpoints.http.body=~`product=SMA%201000%20Series`

# Server banner prefix - anchor at the start
host.services.banner=~`^220 ProFTPD`

# Header value, bound to its key with nested syntax
host.services.endpoints.http.headers:(key="Server" and value=~`^SMA/`)

# Case-insensitivity via character classes, never (?i)
host.services.endpoints.http.html_title=~`[Ff]ish[Ee]ye and [Cc]rucible 4\.`
```
