---
name: censys-tsa
description: Use when the user wants a Censys Threat Surface Assessment - how many hosts on the internet expose a given product, vendor, appliance or CVE, and how many of those are in one country. Triggers on "TSA", "threat surface", "exposed hosts", "how many hosts run X", "Censys query for X", "Shodan-style count", or a bare CVE ID with an exposure question. Routes to the censys-tsa agent; do not attempt the workflow yourself.
---

# Censys Threat Surface Assessment

This machine has a Censys TSA toolkit installed: five agents, a capability
plugin, and a `tsa` command. **Do not try to do this work yourself** - hand it
over.

## What to do

Tell the user to switch to the `censys-tsa` agent and name the target, or invoke
it directly if you can:

```
@censys-tsa Ivanti EPMM
@censys-tsa CVE-2024-21762
```

`censys-tsa` is interactive: it opens by asking five questions about what it is
allowed to do (web research, endpoint validation, deep dive, credit budget,
report output) and then runs the assessment, delegating fingerprinting, the
signature hunt, and report writing to its own subagents.

For an unattended run - CI, a batch of targets, no questions asked - use the
command instead:

```bash
tsa run "Ivanti EPMM"                       # writes ./reports/ivanti-epmm.{spec.json,md}
tsa run --cve CVE-2024-21762 --deep-dive
```

## What it produces

A validated Censys Platform query, a global host count and a country-scoped host
count, both excluding honeypots, with the counting basis and credits spent stated
explicitly - plus a written report under `./reports/` unless told otherwise.

## Anything else

```bash
tsa help        # every subcommand
tsa doctor      # verify the install, credentials included
tsa ref         # the workflow references, if you are curious how it works
```

Two things worth knowing before you touch any of it:

- **Every count comes from Censys data.** Nothing in this toolkit contacts an
  assessed host, and neither should you: no `curl`, no browser, no scanner
  against any IP or hostname that comes out of a query.
- **Censys calls cost credits.** `tsa search` and `tsa agg` are 1 each, `tsa
  assess` is 2. Do not loop over them exploratively; that is what the agents'
  budget gate exists to prevent.
