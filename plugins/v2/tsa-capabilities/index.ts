/**
 * TSA capability negotiation and enforcement - OpenCode 2 implementation.
 *
 * Same job and same rules as the OpenCode 1 plugin in
 * plugins/v1/tsa-capabilities.ts; read that file's header for the design.
 * Only what differs on OpenCode 2 is described here.
 *
 * WHY TWO FILES
 * -------------
 * OpenCode 2 has a new plugin API and does not run V1 plugins. A single file
 * exporting both shapes only works on V1 1.18.29 and newer, and this kit
 * supports V1 back to 1.18.14. So each major version gets its own entrypoint:
 *
 *   V1  loads  {plugin,plugins}/*.ts       - flat files, not this directory
 *   V2  loads  plugins/<name>/index.ts     - this file
 *
 * The block between the SHARED markers below is a verbatim copy of the V1
 * file's. tests/test_portability.py fails if the two copies drift.
 *
 * WHAT CHANGED ON OPENCODE 2
 * --------------------------
 * - `tool.execute.before` now receives the agent directly, so the V1
 *   chat.message / chat.params bookkeeping is gone.
 * - The shell tool is `shell`, not `bash`.
 * - Code Mode adds an `execute` tool whose sandbox has `fetch`. That is a
 *   network path around `webfetch`, so it is gated by the same capability.
 * - Plugins run in the OpenCode service, not in the `opencode run` process.
 *   TSA_CAPABILITIES only reaches this plugin when the service inherits the
 *   environment, which is why `tsa run` uses `--standalone` on OpenCode 2.
 * - `@opencode/plugin` is provided by OpenCode itself; no node_modules bridge.
 */

import { Plugin } from "@opencode/plugin"

// ---- SHARED: keep identical to plugins/v1/tsa-capabilities.ts ----
type DeepDive = "always" | "never" | "after"
type RateLimit = "none" | "fast" | "standard"

type Caps = {
  webfetch: boolean
  websearch: boolean
  endpointValidation: boolean
  deepDive: DeepDive
  versionBreakdown: boolean
  writeReports: boolean
  /** Also print the assembled spec as a fenced json block in the final message.
   *  Independent of writeReports: a run can write a file, print the spec, both,
   *  or neither. `tsa run` forces this on when no file is written, because then
   *  the block is the only way it can recover the spec. */
  printSpec: boolean
  /** How fast this run may issue Censys requests. Recorded here so it is visible
   *  and queryable, but ENFORCED BY `tsa limits`, which persists the choice where
   *  every subcommand in every subagent reads it. This plugin cannot enforce it:
   *  pacing happens inside a Python process, not at the tool boundary. The
   *  orchestrator must run `tsa limits <profile>` after registering. */
  rateLimit: RateLimit
  /** True once tsa_capabilities action=set has run for this session. The
   *  startup interview happens before that, and must not be gated by the
   *  very flags it is asking the user to choose. */
  registered: boolean
  callBudget: number | null
  callsUsed: number
  source: string
}

const DEFAULTS: Caps = {
  webfetch: false,
  websearch: false,
  endpointValidation: false,
  deepDive: "after",
  versionBreakdown: false,
  writeReports: true,
  printSpec: false,
  // Matches censys_limits.FALLBACK_PROFILE. Not "standard": the original pacing
  // capped the rolling budget below what one assessment issues, so it stalled
  // every real run. "fast" is bounded an order of magnitude above a full run.
  rateLimit: "fast",
  registered: false,
  callBudget: null,
  callsUsed: 0,
  source: "default (fail-closed)",
}

/** The agents this plugin governs. Anything else on the machine is none of its
 *  business. Kept in sync with .opencode/agent/*.md by tests. */
const TSA_AGENTS = new Set([
  "censys-tsa",
  "censys-tsa-auto",
  "censys-fingerprint",
  "censys-deepdive",
  "censys-report",
])

/** opencode's internal agents run inside another agent's session (measured: the
 *  `title` agent reuses the parent session ID). They must never be mistaken for
 *  the session's real agent. */
const INTERNAL_AGENTS = new Set(["title", "summary", "compaction"])

/** Over-estimated Censys costs, for the circuit-breaker only.
 *
 *  Matches the `tsa` subcommands the prompts actually use, and keeps the old
 *  `python utils/*.py` spellings so a hand-typed legacy command is still
 *  counted rather than silently free. Tests assert these patterns cover every
 *  Censys invocation present in the agent prompts and references.
 *
 *  Each rule is ONE regex with alternation, never two `.test()` calls joined by
 *  `||`: tests/helpers.py parses this function out of the source and replays it
 *  in Python rather than duplicating the rules, and that parser reads one
 *  pattern per rule. Keep the shape. */
function censysCost(command: string): number {
  if (!command) return 0
  if (/\btsa\s+agg(regate)?\b|censys_aggregate\.py/.test(command)) {
    if (/--suggest-fields/.test(command)) return 15 // one request per field
    if (/--compare-levels/.test(command)) return 2 // doubles the cost
    return 1
  }
  // The batching entrypoints issue one request per item, and the item count is
  // not recoverable from a command line with any confidence - `--plan` reads a
  // file this hook cannot see, and a repeated flag can appear any number of
  // times. These are therefore deliberately generous flat estimates, sized so a
  // loop that keeps batching trips the breaker rather than slipping under it.
  if (/\btsa\s+candidates\b|censys_batch\.py candidates/.test(command)) {
    if (/--totals/.test(command)) return 24 // 1 + 3 per candidate
    return 16 // 1 + 2 per candidate
  }
  if (/\btsa\s+probe\b|censys_batch\.py probe/.test(command)) {
    // Keep in step with censys_batch.PROBE_TREES + PROBE_PROTOCOL + PROBE_WIDE
    // plus the seed sample. A test derives the real count from those tuples and
    // fails if this drifts below it, because a breaker that under-prices a
    // command is a breaker with a hole in it.
    if (/--wide/.test(command)) return 10 // sample + 3 trees + protocol + 5 wide
    return 5 // sample + the three tag trees + the decoded-protocol bucket
  }
  if (/\btsa\s+batch\b|censys_batch\.py batch/.test(command)) {
    if (/--plan|\s-p\s/.test(command)) return 20 // a file we cannot read
    return 10
  }
  if (/\btsa\s+assess\b|censys_tsa\.py/.test(command)) return 2 // two counts
  if (/\btsa\s+search\b|censys_query\.py/.test(command)) return 1
  return 0 // cve, credits, budget, timeline, report, ref and doc are all free
}

/** The Censys Platform MCP server spends credits that `censysCost` cannot see,
 *  so TSA runs are kept off it and use `tsa`, which the budget counts. Matches a
 *  direct MCP tool call (`censys-platform_aggregate`, `censys_platform_...`) and,
 *  on OpenCode 2, Code Mode code that calls `tools["censys-platform"]`. */
const CENSYS_MCP = /censys[-_]platform/i

function usesCensysMcp(tool: string, args: unknown): boolean {
  if (CENSYS_MCP.test(tool)) return true
  if (tool !== "execute") return false
  const code = String((args as { code?: unknown } | null)?.code ?? "")
  return CENSYS_MCP.test(code)
}

function summarise(c: Caps): string {
  const budget = c.callBudget === null ? "uncapped" : `${c.callsUsed}/${c.callBudget} used`
  return [
    `web research   : ${c.webfetch || c.websearch ? "ENABLED" : "disabled"} (webfetch=${c.webfetch}, websearch=${c.websearch})`,
    `endpoint check : ${c.endpointValidation ? "ENABLED" : "disabled"}`,
    `deep dive      : ${c.deepDive}`,
    `version brkdwn : ${c.versionBreakdown ? "ENABLED" : "disabled"}  (advisory - not plugin-enforced)`,
    `censys pacing  : ${c.rateLimit}  (apply it with \`tsa limits ${c.rateLimit}\` - this plugin cannot)`,
    `write reports  : ${c.writeReports}`,
    `print spec     : ${c.printSpec}`,
    `censys budget  : ${budget}`,
    `source         : ${c.source}`,
  ].join("\n")
}

/** Parse the TSA_CAPABILITIES env var used by the unattended `tsa run` path. */
function fromEnv(): Caps | null {
  const raw = process.env.TSA_CAPABILITIES
  if (!raw) return null
  const caps: Caps = { ...DEFAULTS, source: "TSA_CAPABILITIES env", registered: true }
  for (const pair of raw.split(/[\s,]+/).filter(Boolean)) {
    const [k, v] = pair.split("=")
    const on = v === "on" || v === "true" || v === "yes" || v === "1"
    switch (k) {
      case "webfetch": caps.webfetch = on; break
      case "websearch": caps.websearch = on; break
      case "web": caps.webfetch = on; caps.websearch = on; break
      case "endpoint": caps.endpointValidation = on; break
      case "versionbreakdown": caps.versionBreakdown = on; break
      case "reports": caps.writeReports = on; break
      case "printspec": caps.printSpec = on; break
      case "deepdive":
        caps.deepDive = (["always", "never", "after"].includes(v) ? v : "never") as DeepDive
        break
      case "rate":
        caps.rateLimit = (["none", "fast", "standard"].includes(v) ? v : "fast") as RateLimit
        break
      case "budget": {
        const n = Number(v)
        caps.callBudget = Number.isFinite(n) && n > 0 ? n : null
        break
      }
    }
  }
  return caps
}

// ---- END SHARED ----

/** Kept on globalThis for the same reason as the V1 plugin: a global install
 *  and a checkout opened in OpenCode can load this file twice. */
type SharedState = {
  byRoot: Map<string, Caps>
  rootMemo: Map<string, string>
  agentsBySession: Map<string, Set<string>>
}

const STATE_KEY = "__tsaCapabilitiesStateV2"

function sharedState(): SharedState {
  const holder = globalThis as any
  if (!holder[STATE_KEY]) {
    holder[STATE_KEY] = {
      byRoot: new Map<string, Caps>(),
      rootMemo: new Map<string, string>(),
      agentsBySession: new Map<string, Set<string>>(),
    } satisfies SharedState
  }
  return holder[STATE_KEY] as SharedState
}

const ARG_SCHEMA = {
  type: "object",
  properties: {
    action: { type: "string", enum: ["set", "get"], description: "'set' to record, 'get' to read" },
    webfetch: { type: "boolean", description: "allow fetching URLs (gates step 3b)" },
    websearch: { type: "boolean", description: "allow web search (gates step 3b)" },
    endpointValidation: {
      type: "boolean",
      description: "allow asking the user to run a request against a host they own (principle 7)",
    },
    deepDive: {
      type: "string",
      enum: ["always", "never", "after"],
      description: "'after' = ask once the baseline report is on screen; 'always' = pre-authorised; 'never' = skip",
    },
    rateLimit: {
      type: "string",
      enum: ["none", "fast", "standard"],
      description:
        "how fast Censys requests may be issued. NOT enforced here - after " +
        "registering, run `tsa limits <profile>` so every subagent's calls " +
        "pick it up. 'none' = no pacing (credits are still capped).",
    },
    versionBreakdown: {
      type: "boolean",
      description:
        "produce a per-version distribution table. Off by default; on when the target " +
        "names a version or is a CVE. ADVISORY ONLY - see the plugin header.",
    },
    writeReports: { type: "boolean", description: "write reports/<slug>.spec.json and .md at the end" },
    printSpec: {
      type: "boolean",
      description:
        "also print the assembled spec as a fenced json block after the summary. " +
        "Independent of writeReports - both can be true.",
    },
    callBudget: {
      type: "number",
      description: "ceiling on estimated Censys credits for this run; omit or 0 for uncapped",
    },
  },
  required: ["action"],
  additionalProperties: false,
} as const

type Args = {
  action: "set" | "get"
  webfetch?: boolean
  websearch?: boolean
  endpointValidation?: boolean
  deepDive?: DeepDive
  rateLimit?: RateLimit
  versionBreakdown?: boolean
  writeReports?: boolean
  printSpec?: boolean
  callBudget?: number
}

export default Plugin.define({
  id: "censys-tsa.capabilities",
  async setup(ctx) {
    const { byRoot, rootMemo, agentsBySession } = sharedState()
    const envCaps = fromEnv()

    function recordAgent(sessionID?: string, agent?: string) {
      if (!sessionID || !agent || INTERNAL_AGENTS.has(agent)) return
      let seen = agentsBySession.get(sessionID)
      if (!seen) {
        seen = new Set()
        agentsBySession.set(sessionID, seen)
      }
      seen.add(agent)
    }

    function isTsaSession(sessionID: string): boolean {
      const seen = agentsBySession.get(sessionID)
      if (!seen) return false
      for (const agent of seen) if (TSA_AGENTS.has(agent)) return true
      return false
    }

    async function rootOf(sessionID: string): Promise<string> {
      const hit = rootMemo.get(sessionID)
      if (hit) return hit
      let cur = sessionID
      for (let i = 0; i < 12; i++) {
        try {
          const info: any = await ctx.session.get({ sessionID: cur as any })
          const parent = info?.parentID
          if (!parent) break
          cur = parent
        } catch {
          break // unresolvable: treat the current id as the root
        }
      }
      rootMemo.set(sessionID, cur)
      return cur
    }

    async function capsFor(sessionID: string): Promise<{ root: string; caps: Caps }> {
      const root = await rootOf(sessionID)
      let caps = byRoot.get(root)
      if (!caps) {
        caps = { ...(envCaps ?? DEFAULTS) }
        byRoot.set(root, caps)
      }
      return { root, caps }
    }

    async function governed(sessionID: string): Promise<boolean> {
      if (isTsaSession(sessionID)) return true
      const root = await rootOf(sessionID)
      if (isTsaSession(root)) return true
      return byRoot.get(root)?.registered === true
    }

    const blocked = (what: string, why: string, fix: string) =>
      new Error(
        `[tsa-capabilities] ${what} is DISABLED for this TSA run.\n` +
          `Reason: ${why}\n` +
          `${fix}\n` +
          `Do not retry this call. Record the limitation in the run's caveats and ` +
          `continue with the evidence you can legitimately obtain.`,
      )

    await ctx.tool.transform((editor) => {
      editor.add({
        name: "tsa_capabilities",
        description:
          "Record or read the capability set for this Censys TSA run. Only relevant to the " +
          "censys-tsa agents; ignore it in any other context. `censys-tsa` calls this once " +
          "with action='set' immediately after interviewing the user, before any Censys call. " +
          "Any agent may call it with action='get' to learn what it is permitted to do. " +
          "Capabilities are enforced by the plugin across all subagents; they are not advisory.",
        input: ARG_SCHEMA as any,
        // A direct tool, not a Code Mode one: `execute` is blocked below until
        // web research is authorised, and this tool must be reachable before that.
        options: { codemode: false },
        async execute(input: unknown, context: any) {
          const args = input as Args
          recordAgent(context.sessionID, context.agent)
          const { root, caps } = await capsFor(context.sessionID)
          if (args.action === "get") {
            return { content: `Capabilities for this TSA run:\n${summarise(caps)}` }
          }
          if (args.webfetch !== undefined) caps.webfetch = args.webfetch
          if (args.websearch !== undefined) caps.websearch = args.websearch
          if (args.endpointValidation !== undefined) caps.endpointValidation = args.endpointValidation
          if (args.deepDive !== undefined) caps.deepDive = args.deepDive
          if (args.rateLimit !== undefined) caps.rateLimit = args.rateLimit
          if (args.versionBreakdown !== undefined) caps.versionBreakdown = args.versionBreakdown
          if (args.writeReports !== undefined) caps.writeReports = args.writeReports
          if (args.printSpec !== undefined) caps.printSpec = args.printSpec
          if (args.callBudget !== undefined) caps.callBudget = args.callBudget > 0 ? args.callBudget : null
          caps.source = `interview by ${context.agent}`
          caps.registered = true
          byRoot.set(root, caps)
          return {
            content:
              `Capabilities registered and now enforced for every subagent in this run:\n${summarise(caps)}\n\n` +
              `NEXT: run \`tsa limits ${caps.rateLimit}\` in a shell now. Pacing lives in ` +
              `the Python tools, not at the tool boundary, so it is the only capability ` +
              `here this plugin cannot apply for you.`,
          }
        },
      })
    })

    // Hard enforcement; see "tool.execute.before" in the V1 plugin.
    await ctx.tool.hook("execute.before", async (event) => {
      recordAgent(event.sessionID, event.agent)
      const name = event.tool
      if (name === "tsa_capabilities") return
      if (!(await governed(event.sessionID))) return
      const { caps } = await capsFor(event.sessionID)
      const args: any = event.input ?? {}

      if (usesCensysMcp(name, args)) {
        throw blocked(
          "the Censys MCP server",
          "its calls spend Censys credits outside this run's budget.",
          "Use the `tsa` command in a shell instead (tsa search, tsa agg, tsa assess).",
        )
      }
      if (name === "webfetch" && !caps.webfetch) {
        throw blocked(
          "webfetch",
          "the user did not authorise web research for this run (step 3b is gated).",
          "Skip step 3b and any release-artifact research, and rely on Censys evidence only.",
        )
      }
      if (name === "websearch" && !caps.websearch) {
        throw blocked(
          "websearch",
          "the user did not authorise web research for this run (step 3b is gated).",
          "Skip step 3b and any release-artifact research, and rely on Censys evidence only.",
        )
      }
      if (name === "execute" && !caps.webfetch) {
        throw blocked(
          "Code Mode (execute)",
          "its sandbox can fetch URLs, and the user did not authorise web research for this run.",
          "Use the shell and the `tsa` command instead.",
        )
      }
      if (name === "question" && caps.registered && !caps.endpointValidation) {
        const text = JSON.stringify(args).toLowerCase()
        if (/\bcurl\s+-|\bcurl\s+http|\bwget\s|--include\b|-i\s+https?:\/\//.test(text)) {
          throw blocked(
            "user-operated endpoint validation",
            "the user did not authorise being asked to probe a host for this run.",
            "Report the version evidence as unverified and say so plainly in the caveats.",
          )
        }
      }
      if (name === "shell" || name === "bash") {
        const cost = censysCost(String(args.command ?? ""))
        if (cost > 0 && caps.callBudget !== null) {
          if (caps.callsUsed + cost > caps.callBudget) {
            throw blocked(
              "this Censys call",
              `it would exceed the run's budget (${caps.callsUsed}/${caps.callBudget} estimated credits already used; ` +
                `this call is estimated at ${cost}).`,
              "Stop querying. Report what you have, and state in the caveats that the budget was exhausted.",
            )
          }
          caps.callsUsed += cost
        } else if (cost > 0) {
          caps.callsUsed += cost
        }
      }
    })
  },
})
