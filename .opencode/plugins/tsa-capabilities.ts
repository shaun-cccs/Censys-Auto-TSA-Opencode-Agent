/**
 * TSA capability negotiation and enforcement.
 *
 * WHY THIS EXISTS
 * ---------------
 * opencode resolves agent permissions statically, from config plus agent
 * frontmatter, at load time. The Task tool accepts only a prompt. So an
 * orchestrator agent genuinely cannot hand a tool to a subagent at invocation
 * time - there is no runtime API for it.
 *
 * This plugin supplies the missing runtime layer. `censys-tsa` interviews the
 * user once at the start of a run, records the answers via the
 * `tsa_capabilities` tool, and this plugin then enforces those answers across
 * every subagent for the rest of the session.
 *
 * HOW CAPABILITIES REACH A SUBAGENT
 * ---------------------------------
 * Subagents run in child sessions with their own session IDs, so state keyed by
 * session ID does not propagate on its own. Each tool call is walked back up
 * the `Session.parentID` chain to its root session, and capabilities are keyed
 * by that root. Verified: a `bash` call inside a `censys-report` child session
 * resolves to the orchestrator's root session at depth 2.
 *
 * FAIL CLOSED
 * -----------
 * A session with no registered capabilities gets DEFAULTS, which have every
 * network capability off. Forgetting to run the interview cannot silently
 * grant web access.
 *
 * THE BUDGET IS A CIRCUIT-BREAKER, NOT AN ACCOUNTANT
 * --------------------------------------------------
 * Censys credit cost is not knowable from the command line alone -
 * `--suggest-fields` issues one request per field, and a paged search costs one
 * credit per extra 100 results. The costs below are deliberate over-estimates
 * whose only job is to stop a runaway loop. The orchestrator still measures
 * real spend with `utils/censys_credits.py`, per references/credits.md. Neither
 * layer pretends to be the other.
 *
 * ONE CAPABILITY IS ADVISORY, NOT ENFORCED: versionBreakdown
 * ----------------------------------------------------------
 * Every other capability here is hard-enforced, because each maps to a distinct
 * tool this plugin can intercept and throw on. `versionBreakdown` does not. A
 * per-version distribution is produced by `censys_aggregate.py` - the same tool
 * used for all legitimate fingerprinting work - so there is no signature to
 * block on without also blocking step 1, 2, 3 and 8.
 *
 * It is carried here so it is visible, queryable and stated in the run summary,
 * but it is a behavioural directive honoured by the agent prompts, not a gate.
 * The credit budget is the only real backstop against an expensive breakdown.
 * Do not assume a `versionBreakdown: false` guarantees no version aggregation
 * happened - verify it in the report.
 *
 * REPRODUCIBILITY NOTE
 * --------------------
 * This file imports `@opencode-ai/plugin`, which requires `.opencode/package.json`.
 * opencode auto-generates `.opencode/.gitignore` which ignores that file, so it
 * must be force-added:  git add -f .opencode/package.json
 */

import { type Plugin, tool } from "@opencode-ai/plugin"

type DeepDive = "always" | "never" | "after"

type Caps = {
  webfetch: boolean
  websearch: boolean
  endpointValidation: boolean
  deepDive: DeepDive
  versionBreakdown: boolean
  writeReports: boolean
  /** Also print the assembled spec as a fenced json block in the final message.
   *  Independent of writeReports: a run can write a file, print the spec, both,
   *  or neither. bin/tsa forces this on when no file is written, because then
   *  the block is the only way it can recover the spec. */
  printSpec: boolean
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
  registered: false,
  callBudget: null,
  callsUsed: 0,
  source: "default (fail-closed)",
}

/** Over-estimated Censys costs, for the circuit-breaker only. */
function censysCost(command: string): number {
  if (!command) return 0
  if (/censys_aggregate\.py/.test(command)) {
    if (/--suggest-fields/.test(command)) return 15 // one request per field
    if (/--compare-levels/.test(command)) return 2 // doubles the cost
    return 1
  }
  if (/censys_tsa\.py/.test(command)) return 2 // two counts
  if (/censys_query\.py/.test(command)) return 1
  return 0 // cve_lookup, censys_credits, tsa_report are all free
}

function summarise(c: Caps): string {
  const budget = c.callBudget === null ? "uncapped" : `${c.callsUsed}/${c.callBudget} used`
  return [
    `web research   : ${c.webfetch || c.websearch ? "ENABLED" : "disabled"} (webfetch=${c.webfetch}, websearch=${c.websearch})`,
    `endpoint check : ${c.endpointValidation ? "ENABLED" : "disabled"}`,
    `deep dive      : ${c.deepDive}`,
    `version brkdwn : ${c.versionBreakdown ? "ENABLED" : "disabled"}  (advisory - not plugin-enforced)`,
    `write reports  : ${c.writeReports}`,
    `print spec     : ${c.printSpec}`,
    `censys budget  : ${budget}`,
    `source         : ${c.source}`,
  ].join("\n")
}

/** Parse the TSA_CAPABILITIES env var used by the unattended bin/tsa path. */
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
      case "budget": {
        const n = Number(v)
        caps.callBudget = Number.isFinite(n) && n > 0 ? n : null
        break
      }
    }
  }
  return caps
}

export const TsaCapabilities: Plugin = async ({ client }) => {
  const byRoot = new Map<string, Caps>()
  const rootMemo = new Map<string, string>()
  const envCaps = fromEnv()

  async function rootOf(sessionID: string): Promise<string> {
    const hit = rootMemo.get(sessionID)
    if (hit) return hit
    let cur = sessionID
    for (let i = 0; i < 12; i++) {
      try {
        const res: any = await client.session.get({ path: { id: cur } })
        const parent = (res?.data ?? res)?.parentID
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

  const blocked = (what: string, why: string, fix: string) =>
    new Error(
      `[tsa-capabilities] ${what} is DISABLED for this TSA run.\n` +
        `Reason: ${why}\n` +
        `${fix}\n` +
        `Do not retry this call. Record the limitation in the run's caveats and ` +
        `continue with the evidence you can legitimately obtain.`,
    )

  return {
    tool: {
      tsa_capabilities: tool({
        description:
          "Record or read the capability set for this TSA run. `censys-tsa` calls this once " +
          "with action='set' immediately after interviewing the user, before any Censys call. " +
          "Any agent may call it with action='get' to learn what it is permitted to do. " +
          "Capabilities are enforced by the plugin across all subagents; they are not advisory.",
        args: {
          action: tool.schema.enum(["set", "get"]).describe("'set' to record, 'get' to read"),
          webfetch: tool.schema.boolean().optional().describe("allow fetching URLs (gates step 3b)"),
          websearch: tool.schema.boolean().optional().describe("allow web search (gates step 3b)"),
          endpointValidation: tool.schema.boolean().optional()
            .describe("allow asking the user to run a request against a host they own (principle 7)"),
          deepDive: tool.schema.enum(["always", "never", "after"]).optional()
            .describe("'after' = ask once the baseline report is on screen; 'always' = pre-authorised; 'never' = skip"),
          versionBreakdown: tool.schema.boolean().optional()
            .describe(
              "produce a per-version distribution table. Off by default; on when the target " +
              "names a version or is a CVE. ADVISORY ONLY - see the plugin header.",
            ),
          writeReports: tool.schema.boolean().optional()
            .describe("write reports/<slug>.spec.json and .md at the end"),
          printSpec: tool.schema.boolean().optional()
            .describe(
              "also print the assembled spec as a fenced json block after the summary. " +
              "Independent of writeReports - both can be true.",
            ),
          callBudget: tool.schema.number().optional()
            .describe("ceiling on estimated Censys credits for this run; omit or 0 for uncapped"),
        },
        async execute(args, context) {
          const { root, caps } = await capsFor(context.sessionID)
          if (args.action === "get") {
            return `Capabilities for this TSA run:\n${summarise(caps)}`
          }
          if (args.webfetch !== undefined) caps.webfetch = args.webfetch
          if (args.websearch !== undefined) caps.websearch = args.websearch
          if (args.endpointValidation !== undefined) caps.endpointValidation = args.endpointValidation
          if (args.deepDive !== undefined) caps.deepDive = args.deepDive
          if (args.versionBreakdown !== undefined) caps.versionBreakdown = args.versionBreakdown
          if (args.writeReports !== undefined) caps.writeReports = args.writeReports
          if (args.printSpec !== undefined) caps.printSpec = args.printSpec
          if (args.callBudget !== undefined) caps.callBudget = args.callBudget > 0 ? args.callBudget : null
          caps.source = `interview by ${context.agent}`
          caps.registered = true
          byRoot.set(root, caps)
          return `Capabilities registered and now enforced for every subagent in this run:\n${summarise(caps)}`
        },
      }),
    },

    /**
     * Hard enforcement. Fires for every tool call in every session, including
     * subagent child sessions. Throwing here blocks the call outright,
     * regardless of what the agent's static permissions say.
     */
    "tool.execute.before": async (input, output) => {
      if (input.tool === "tsa_capabilities") return
      const { caps } = await capsFor(input.sessionID)

      if (input.tool === "webfetch" && !caps.webfetch) {
        throw blocked(
          "webfetch",
          "the user did not authorise web research for this run (step 3b is gated).",
          "Skip step 3b and any release-artifact research, and rely on Censys evidence only.",
        )
      }
      if (input.tool === "websearch" && !caps.websearch) {
        throw blocked(
          "websearch",
          "the user did not authorise web research for this run (step 3b is gated).",
          "Skip step 3b and any release-artifact research, and rely on Censys evidence only.",
        )
      }
      if (input.tool === "question" && caps.registered && !caps.endpointValidation) {
        // Gated ONLY after capabilities have been registered. The startup
        // interview necessarily runs before registration and necessarily talks
        // about endpoint validation - gating it there blocked the very question
        // that configures this flag, which is exactly what happened in practice.
        //
        // The pattern matches a concrete probe COMMAND, not prose about the
        // topic. An earlier version matched the phrase "user-operated endpoint"
        // and so blocked the interview's own question header. Note the plugin
        // sees JSON.stringify of the whole payload - headers, option labels and
        // descriptions included - so anything that merely discusses the feature
        // will be in scope. Match tools, not talk.
        //
        // This is only a backstop. censys-fingerprint is already instructed not
        // to ask when the capability is off, and the failure it guards against
        // is mild: a question the user can simply decline.
        const text = JSON.stringify(output?.args ?? {}).toLowerCase()
        if (/\bcurl\s+-|\bcurl\s+http|\bwget\s|--include\b|-i\s+https?:\/\//.test(text)) {
          throw blocked(
            "user-operated endpoint validation",
            "the user did not authorise being asked to probe a host for this run.",
            "Report the version evidence as unverified and say so plainly in the caveats.",
          )
        }
      }
      if (input.tool === "bash") {
        const cost = censysCost(String(output?.args?.command ?? ""))
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
    },

    // NOTE: there is deliberately no "permission.ask" hook.
    //
    // The obvious design is to leave webfetch/websearch as "ask" in each agent's
    // frontmatter and have a permission.ask hook resolve them at runtime. That
    // does not work: an "ask" permission inside a SUBAGENT hangs forever under
    // `opencode run`, because --auto does not reach subagent sessions and there
    // is no UI to prompt in. Measured, not guessed - with "ask" the subagent
    // never returns; with "allow" it completes immediately.
    //
    // So every agent that may touch the network is "allow" statically, and
    // tool.execute.before above is the sole gate. It fires for every tool call
    // in every session regardless of permission config, so enforcement is
    // identical interactive and unattended, and nothing is ever prompted twice.
    //
    // Consequence worth knowing: if this plugin fails to load, nothing is
    // enforced. That is why the orchestrators call `tsa_capabilities` as their
    // first action - if the tool is missing the run fails loudly at step -1
    // rather than silently proceeding with the network wide open.
  }
}
