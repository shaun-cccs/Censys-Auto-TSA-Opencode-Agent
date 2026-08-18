# Leads and fan-out - how discovery is parallelised

Owned by the orchestrators (`censys-tsa`, `censys-tsa-auto`). Every subagent is
bound by the return contract at the bottom.

## Quick card

**The cost model.** A Censys call takes about a second. An agent turn takes tens
of seconds. A TSA issues 100-300 calls. So wall-clock time is very nearly *the
number of serial turns*, and everything below exists to reduce that number - not
to reduce the number of queries.

**Two levers, in order:**

1. **Batch within a turn.** Independent calls go out together - `tsa probe`,
   `tsa candidates`, `tsa batch`, or several tool calls in one message.
2. **Fan out across workers.** Independent *hypotheses* go to separate subagents,
   invoked **as parallel task calls in a single message**. Measured on opencode
   1.18.18: two workers each sleeping 6s started 0.48s apart and overlapped for
   5.5 of those 6 seconds. Issued in separate messages they would have taken
   twice as long, because a task call blocks until its worker returns.

**The shape of a discovery phase:**

```
orchestrator:  tsa probe '<seed>'                     1 call, 1 turn
orchestrator:  derive 2-4 leads from what it showed
orchestrator:  spawn 4 @censys-fingerprint AT ONCE    one per lead
   worker A ─┐
   worker B ─┼─ each: ≤8 Censys calls, own verdict, own leads[]
   worker C ─┤
   worker D ─┘
orchestrator:  merge verdicts, decide the base query
orchestrator:  refine wave ONLY for leads marked needs_refinement (max 3 waves)
```

**Hard limits, and they are limits, not targets:**

| Thing | Limit |
| --- | --- |
| workers per wave | 4 (never more than 6) |
| waves per phase | 3 |
| Censys calls per lead worker | 8 |
| Censys calls per recon worker | 15 |
| Censys calls per deep-dive family worker | 20 |

**Never sleep. Never poll. Never wait for a background job.** A task call returns
when the worker is done; a bash call returns when the command exits. There is
nothing else in flight, so a `sleep` is pure dead time. If a worker comes back
without its `STATUS:` line, treat it as partial and move on - do not re-invoke it
hoping for more.

**A lead returned independently by 3+ workers is a directive, not a note.**
Workers share no context, so convergence is not imitation - it is three
independent searches pointing at the same gap. Run it in the next wave, or record
why you overrode it. This is the one case that outranks "don't spawn a wave for a
lead that cannot change the base query".

**A worker ends its message with a status line, always:**

```
STATUS: DONE      | PARTIAL <why> | BLOCKED <why>
```

## What a lead is

A lead is **one testable hypothesis about how this product can be identified**,
small enough for a handful of queries and independent enough that testing it does
not need the answer to another lead.

```json
{
  "id": "hardware-tree",
  "hypothesis": "The appliance is tagged under host.services.hardware rather than software",
  "seed_query": "host.services.hardware.product=\"secure_mobile_access\"",
  "fields": ["host.services.hardware.vendor", "host.services.hardware.version"],
  "why": "probe showed an empty software tree and 10,287 hosts in hardware",
  "call_cap": 8
}
```

Good leads are **structurally different from each other**, because that is what
makes them worth running in parallel:

- one per tag tree the probe showed something in (software / hardware / OS)
- one per evidence family (favicon+title / certificate+JARM / path+header /
  redirect+SSO)
- one to disambiguate sibling product lines that share a codebase
- one for version derivation, when the target names a version or a CVE
- one to test the *inverse* - what a promising signal misses

Bad leads: "check everything about this product", "look at more fields", or two
leads whose first query is identical. Splitting on nothing costs a worker and
teaches you nothing.

## What comes back, and what you do with it

Each worker returns a verdict, evidence **with numbers**, two or three example
hosts, and any leads it did not pursue. The orchestrator owns every decision:

- **confirmed** - fold the candidate query into the base query decision
- **rejected** - record it in `caveats`/`signals_rejected` with its reason and
  its count. A rejection with a number is evidence; a rejection without one is a
  guess
- **inconclusive** - either it needs one refinement lead, or it is a caveat. Not
  both, and never a third wave on the same hypothesis
- **new leads** - queue them for the next wave, deduplicated against everything
  already run. **Do not spawn a wave for a lead whose answer cannot change the
  base query** - that is where fan-out stops paying
- **a lead returned independently by three or more workers is a directive, not a
  note.** Workers share no context, so convergence cannot be imitation: it means
  three independent searches all pointed at the same gap, and that is the
  strongest routing signal a fan-out can produce. Either run it in the next wave
  or write into `rationale.findings` why you overrode it. Merging such a lead into
  your notes and proceeding to the report is the specific failure this rule
  exists to prevent - it happened on a Cisco ASA/FTD hunt where three of five
  workers independently flagged the VPN control plane as the unexplored layer,
  the orchestrator recorded all three and published anyway, and the signal it
  pointed at was worth 1,661 missing hosts.
  This overrides the "cannot change the base query" test above: three workers
  agreeing is itself evidence that it can.

Distributing the work does **not** distribute the judgement. The rules that need
the whole picture - measure contamination before gating, prefer a coherent signal
ungated, measure the symmetric difference before replacing a fingerprint - are
the orchestrator's, applied to the merged numbers. A worker reports; the
orchestrator decides.

## Why not one worker per query

Because a worker costs one or two turns just to start - reading its brief and its
references - and a query costs one second. A subagent per query is *slower* than
running the query yourself. Per-query parallelism belongs in `tsa batch`;
per-hypothesis parallelism belongs in subagents. Keep the line there.

## Cost, honestly

Fan-out spends more than a serial pass. Four workers exploring four leads will
sometimes explore a lead a serial agent would have abandoned after learning
something from the previous one, and each worker re-reads its references. Expect
noticeably more tokens and somewhat more credits for a large reduction in wall
clock. The call caps above and the credit ceiling are what keep the worst case
bounded - do not raise them to be thorough. Narrow the leads instead.
