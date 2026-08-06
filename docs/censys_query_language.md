# Censys Query Language (CenQL) Syntax Reference

Source: <https://docs.censys.com/docs/censys-query-language> (updated 2026-03-31)

Field list: see [`queryable_fields/host_censys_queryable_fields.md`](./queryable_fields/host_censys_queryable_fields.md).

## Query types

- **Full-text query** — searches the whole record, e.g. `"example.com"`. For certificate records, full-text only targets `cert.names`, `cert.parsed.issuer_dn`, and `cert.parsed.subject_dn`.
- **Field-value query** — `<field name> <operator> <value>`, e.g. `host.location.city="Ann Arbor"`.

You can also look up a host or certificate directly by entering its IP address or SHA-256 hash in the search bar.

## Operators

| Operator | Description | Example | Hit | Miss |
| --- | --- | --- | --- | --- |
| `:` | Case-insensitive, tokenized match | `field: "hello"` | `Hello World` | `Hi World` |
| `=` | Exact match (case-sensitive for strings) | `field = "hello"` | `hello` | anything else |
| `=~` | Regex match against any part of the field. `^`/`$` allowed only at start/end. **Case-sensitive; inline flags like `(?i)` fail silently — see Regex gotchas** | ``field=~`^Hello\s\w{5}$` `` | `Hello World` | `World Hello` |
| `<`, `>`, `<=`, `>=` | Range comparison; works for strings, numbers, dates, IPs | `field > 10` | `20` | `9` |
| `:*` | Field contains any non-zero value | `field: *` | `hello` | `""` |

### Tokenization

The `:` operator splits text into searchable tokens rather than scanning the whole field as one block.

- `web.endpoints.http.body: "click save"` tokenizes `click` and `save` separately and requires them in close proximity, in order.
- `web.endpoints.http.body: "access=denied"` tokenizes to `access denied` and matches that phrase.

**Certificates behave differently.** All `*.common_name` and `cert.names` fields use a subdomain analyzer. `cert.parsed.subject.common_name: "abcdefg-1234567.example.domain.com"` yields tokens `abcdefg-1234567.example.domain.com`, `example.domain.com`, and `domain.com`. To match a component of a tokenized string, use regex:

```
cert.parsed.subject.common_name=~`^abcdefg-1234567`
```

### Regex gotchas — verified empirically

**Inline flag groups such as `(?i)`, `(?s)` and `(?is)` are not supported and fail
silently, returning 0 hits rather than an error.** This is the single most
dangerous trap in CenQL: a query with `(?i)` looks valid, costs credits, and
returns an empty result set that is easily mistaken for "this product is not
exposed". Measured on `host.services.endpoints.http.headers`:

| Query | Hits |
| --- | --- |
| ``value=~`Jetty` `` | 199,543 |
| ``value=~`jetty` `` | 1,237 |
| ``value=~`[Jj]etty` `` | 199,548 |
| ``value=~`(?i)jetty` `` | **0 — silently wrong** |

**Regex is case-sensitive; express case-insensitivity with character classes.**
Write ``value=~`[Jj]etty` ``, not ``value=~`(?i)jetty` ``. For a longer string,
bracket only the letters whose case actually varies — usually the first letter of
each word, e.g. ``[Ff]ish[Ee]ye`` or ``[Cc]rucible``.

**Substring matching works by default** — the docs are correct that `=~` matches
any part of the field, so no `.*` padding is needed. ``value=~`Jetty` `` and
``value=~`Jetty.*` `` return the same population.

**Always run a positive control before believing a 0.** Re-run the regex against
a population you know contains the string. If the control also returns 0, the
regex is malformed, not the data.

## HTTP headers — nested key/value querying

`host.services.endpoints.http.headers` is a **nested** field with `key` and
`value` subfields, so header criteria must be bound to the same object:

```
host.services.endpoints.http.headers:(key="Set-Cookie" and value="...")
host.services.endpoints.http.headers:(key="Server" and value=~`[Jj]etty`)
```

Key-only matching tests for the presence of a header, which is a strong
product signal in its own right:

```
host.services.endpoints.http.headers:(key="X-AUSERNAME")
```

A plain top-level `and` of `headers.key` and `headers.value` is wrong — it only
requires both values to appear somewhere on the host, so it will match a
`Server` key against some *other* header's value.

Header keys preserve their original casing (`Set-Cookie`, `X-AUSERNAME`), and a
few hosts send lowercase variants (`transfer-encoding`), so use a character
class or `:` where casing may vary.

**`Set-Cookie` values are queryable — but only via regex, and aggregations hide
them.** Bucketing `headers.value` over a population returns a `<REDACTED>`
placeholder in place of cookie values, which makes them *look* unavailable. That
redaction is a display-layer artifact of the aggregation API only: the search
index retains the real values, and `=~` matches them normally.

| Query | Hits |
| --- | --- |
| ``(key="Set-Cookie" and value=~`JSESSIONID`)`` | 1,493,916 |
| ``(key="Set-Cookie" and value=~`expires=Thu, 01-Jan-1970`)`` | 970,062 |
| ``(key="Set-Cookie" and value=~`FESESSIONID`)`` | 70 |
| ``(key="Set-Cookie" and value="<REDACTED>")`` | 0 — placeholder is not a stored value |

Use `=~`, never `=`. An exact match cannot work because each value carries a
unique session ID and timestamp. This makes cookie *names* a first-class
fingerprint: `FESESSIONID` for Atlassian FishEye/Crucible, `JSESSIONID` for Java
servlet apps generally.

Beware generic-looking cookie names — `FESESSIONID` also collides with unrelated
apps using it for "front-end session", so validate incremental hits before
adding a cookie signal to a query.

**General rule: never infer queryability from aggregation output.** The
aggregation API redacts and truncates some values for display, so a field can
look empty, redacted, or low-cardinality in buckets while remaining fully
searchable. When an aggregation looks unusable, test the field with a direct
`=~` search before concluding anything.

## Body field truncation

`host.services.endpoints.http.body` stores only the **first 64KB** for hosts
without a name, and only the **first 6KB** for hosts with a name. A string that
appears late in a large page — a footer, a copyright line, a JS bundle path —
may be absent from the stored body even though it is present on the live host.
A body regex returning 0 is therefore inconclusive, not negative.

## Boolean operators and grouping

`and`, `or`, `not` (case-insensitive), plus parentheses `()` and brackets `{}`.

| Purpose | Query |
| --- | --- |
| Port 8880 open AND an HTTP service on any port | `host.services.port=8880 and host.services.protocol=HTTP` |
| Port 21 open OR FTP on any port | `host.services.port=21 or host.services.protocol=FTP` |
| Not in the United States | `not host.location.country="United States"` |
| Not in the US or India | `not (host.location.country="United States" or host.location.country="India")` |
| Same, using bracket value set | `not (host.location.country: {"United States", "India"})` |
| Services on only ports 80 and 443 | `host.services.port: 80 and host.services.port: 443 and not host.services:(not port:{80, 443})` |

> `and` applies criteria to the record as a whole, not to the same nested object. Use nested field syntax to require matches within a single object.

## Nested fields

Group criteria in parentheses after the nested field name to require all criteria match the *same* object in an array.

| Purpose | Query |
| --- | --- |
| SSH on port 22 | `host.services: (port = "22" and protocol = "SSH")` |
| Apache httpd 2.4.62 | `host.services.software: (product = "httpd" and version = "2.4.62")` |
| nginx `Server` header | `host.services.endpoints.http.headers: (key = "Server" and value = "nginx")` |
| nginx with default HTML title | `host.services: (software.product = "nginx" and endpoints.http.html_title = "Welcome to nginx!")` |

## Ranges

Use `>`, `<`, `>=`, `<=`. Integer and date values must be wrapped in quotes or backticks. Relative time variables (e.g. `now-1d`) are supported.

| Purpose | Query |
| --- | --- |
| Certs added between Oct 20–30, 2024 (inclusive) | `cert.added_at>="2024-10-20" and cert.added_at<="2024-10-30"` |
| Services scanned in the last 24 hours | `host.services.scan_time > "now-1d"` |
| Web endpoints with status 200–204 | `web.endpoints: (http.status_code >= "200" and http.status_code <= "204")` |

## CIDR search

In the web UI, enter a CIDR range in the search bar with no field. To combine with other fields, use `host.ip: "cidrblock"`.

## `twist` function

Finds field values similar to a given value (a narrower-scope dnstwist). Available to all users; less effective on two- or three-character domains.

```
twist([fieldname], `[value]`)
```

Example — find lookalike domains excluding the real one:

```
twist(web.hostname, `censys.io`) and not web.hostname:`censys.io`
```

## Field types

| Type | Description | Examples |
| --- | --- | --- |
| `boolean` | True or false | `True`, `False` |
| `ip` | IP address. Wrap CIDR blocks in quotes/backticks when searching `host.ip` | `1.1.1.1` |
| `ip_range` | Range of IP values | `125.8.0.0/13` |
| `string` | Quoted strings may contain whitespace, keywords, escapes and special characters. Single `'`, double `"` or backticks (backticks only escape backticks). Unquoted strings must match `[a-zA-Z][a-zA-Z0-9._-]*` | `"hello world"`, `hello.world`, `hello-world`, `hello_world` |
| `date` | RFC 3339 timestamp or epoch milliseconds | `2024-10-25T00:00:00-04:00`, `2024-10-25`, `1746618176700` |
| `unsigned_long` | Unsigned 64-bit integer (e.g. `host.services.port`, version fields) | `22`, `3389` |
| `text` | Full-text content, e.g. banners and their hashes, `host.services.software.product`/`.version`/`.cpe` | `HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n`, `1.16.1` |

## Unicode escape sequences

| Sequence | Character |
| --- | --- |
| `\a` | Alert |
| `\b` | Backspace |
| `\e` | Escape character |
| `\f` | Formfeed / page break |
| `\n` | Newline |
| `\r` | Carriage return |
| `\t` | Horizontal tab |
| `\v` | Vertical tab |

## Aliased fields

Aliases search across several fields at once. They **cannot** be used in nested-field queries (e.g. `host.services: (protocol: SSH and product: "OpenSSH")` is invalid), only fields your account can access are included, and you cannot build a report broken down by an alias.

| Alias | Fields included |
| --- | --- |
| `banner` | `host.services.banner`, `host.services.endpoints.banner`, `web.endpoints.banner` |
| `cpe` | `host.hardware.cpe`, `host.hardware.components.cpe`, `host.services.hardware.components.cpe`, `host.services.hardware.cpe`, `host.services.software.components.cpe`, `host.services.software.cpe`, `host.operating_system.components.cpe`, `host.operating_system.cpe`, `host.services.operating_systems.components.cpe`, `host.services.operating_systems.cpe`, `web.operating_systems.components.cpe`, `web.operating_systems.cpe`, `web.hardware.cpe`, `web.hardware.components.cpe`, `web.software.cpe`, `web.software.components.cpe` |
| `sha256` | `web.endpoints.banner_hash_sha256`, `web.endpoints.http.body_hash_sha256`, `web.endpoints.http.favicons.hash_sha256`, `host.services.endpoints.http.body_hash_sha256`, `host.services.endpoints.http.favicons.hash_sha256`, `host.services.endpoints.banner_hash_sha256`, `host.services.banner_hash_sha256`, `cert.fingerprint_sha256`, `host.services.cert.fingerprint_sha256`, `web.cert.fingerprint_sha256` |
| `sha1` | `host.services.redis.git_sha1`, `host.services.cert.fingerprint_sha1`, `host.services.endpoints.http.body_hash_sha1`, `cert.fingerprint_sha1`, `web.cert.fingerprint_sha1`, `web.endpoints.http.body_hash_sha1` |
| `labels` | `host.labels.value`, `host.services.labels.value`, `web.labels.value`, `cert.labels` |
| `product` | `host.hardware.components.product`, `host.hardware.product`, `host.services.hardware.components.product`, `host.services.hardware.product`, `host.services.software.components.product`, `host.services.software.product`, `host.operating_system.components.product`, `host.operating_system.product`, `host.services.operating_systems.components.product`, `host.services.operating_systems.product`, `web.operating_systems.components.product`, `web.operating_systems.product`, `web.hardware.product`, `web.hardware.components.product`, `web.software.components.product`, `web.software.product` |
| `vendor` | `host.hardware.components.vendor`, `host.hardware.vendor`, `host.services.hardware.components.vendor`, `host.services.hardware.vendor`, `host.services.software.components.vendor`, `host.services.software.vendor`, `host.operating_system.components.vendor`, `host.operating_system.vendor`, `host.services.operating_systems.vendor`, `host.services.operating_systems.components.vendor`, `web.hardware.components.vendor`, `web.hardware.vendor`, `web.software.vendor`, `web.software.components.vendor`, `web.operating_systems.vendor`, `web.operating_systems.components.vendor` |
| `vulns` | `host.services.vulns.id`, `web.vulns.id` |
| `vuln_score` | `web.vulns.metrics.cvss_v31.score`, `web.vulns.metrics.cvss_v40.score`, `web.vulns.metrics.cvss_v30.score`, `host.services.vulns.metrics.cvss_v30.score`, `host.services.vulns.metrics.cvss_v31.score`, `host.services.vulns.metrics.cvss_v40.score` |
| `threats` | `host.services.threats.name`, `web.threats.name` |
| `screenshots` | `host.services.screenshots.handle` |
| `org` | `host.whois.organization.name`, `host.autonomous_system.organization`, `host.services.cert.parsed.subject.organization`, `host.services.cert.parsed.issuer.organization`, `web.cert.parsed.subject.organization`, `web.cert.parsed.issuer.organization`, `cert.parsed.subject.organization`, `cert.parsed.issuer.organization` |
