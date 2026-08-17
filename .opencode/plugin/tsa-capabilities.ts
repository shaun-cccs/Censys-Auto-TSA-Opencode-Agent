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
 * SCOPE: THIS PLUGIN IS INSTALLED GLOBALLY AND MUST STAY OUT OF THE WAY
 * --------------------------------------------------------------------
 * `tool.execute.before` fires for every tool call in every session on the
 * machine, and this plugin's defaults are fail-closed. Enforcing unconditionally
 * would therefore block `webfetch` and `websearch` in every unrelated project
 * the user opens - which is precisely what an earlier version of this file did
 * once it was installed into ~/.config/opencode.
 *
 * `tool.execute.before` is not told which agent it is running under (its input
 * is `{ tool, sessionID, callID }` and nothing else). `chat.message` and
 * `chat.params` are, so we learn the agent there and remember it per session.
 * Measured ordering, opencode 1.18.14 - the agent is always known before the
 * first tool call, in parent and child sessions alike:
 *
 *     chat.message  sessionID=ses_A agent=build
 *     chat.params   sessionID=ses_A agent=title      <- internal, ignored
 *     chat.params   sessionID=ses_A agent=build
 *     tool.before   tool=task      sessionID=ses_A
 *     chat.message  sessionID=ses_B agent=explore    <- child session
 *     chat.params   sessionID=ses_B agent=explore
 *     tool.before   tool=bash      sessionID=ses_B
 *
 * Note the `title` agent shares the parent's session ID: opencode's internal
 * agents run in-session, so the agent of a session is a SET, not a single value,
 * and internal names must be filtered out.
 *
 * A session is governed only if its own agent is one of TSA_AGENTS, or - when
 * the agent is somehow unknown - if its root session is a TSA session or has
 * registered capabilities. Everything else returns immediately, so an install
 * of this kit is invisible to the rest of a user's work.
 *
 * FAIL CLOSED
 * -----------
 * Within a governed session, capabilities that were never registered get
 * DEFAULTS, which have every network capability off. Forgetting to run the
 * interview cannot silently grant web access.
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
 * per-version distribution is produced by `tsa agg` - the same command used for
 * all legitimate fingerprinting work - so there is no signature to block on
 * without also blocking step 1, 2, 3 and 8.
 *
 * It is carried here so it is visible, queryable and stated in the run summary,
 * but it is a behavioural directive honoured by the agent prompts, not a gate.
 * The credit budget is the only real backstop against an expensive breakdown.
 * Do not assume a `versionBreakdown: false` guarantees no version aggregation
 * happened - verify it in the report.
 *
 * REPRODUCIBILITY NOTE
 * --------------------
 * This file imports `@opencode-ai/plugin`. opencode installs that package into
 * its config directory, but module resolution starts from this file's REAL
 * path, not from the symlink that `install.sh` puts in
 * ~/.config/opencode/plugin/. If the kit lives outside the config directory,
 * install.sh bridges the gap with a `node_modules` symlink at the kit root; see
 * the comment block in install.sh. When resolution fails opencode loads this
 * plugin as nothing, silently, and NOTHING IS ENFORCED - which is why
 * `tsa doctor` checks the resolution chain explicitly.
 *
 * For contributors working inside this repo, the same import is satisfied by
 * `.opencode/package.json`. opencode auto-generates `.opencode/.gitignore`
 * which ignores that file, so it must be force-added:
 *     git add -f .opencode/package.json
 */

import { type Plugin, tool } from "@opencode-ai/plugin"

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
    if (/--wide/.test(command)) return 9 // sample + 3 tag trees + 5 wide fields
    return 4 // sample + the three tag trees
  }
  if (/\btsa\s+batch\b|censys_batch\.py batch/.test(command)) {
    if (/--plan|\s-p\s/.test(command)) return 20 // a file we cannot read
    return 10
  }
  if (/\btsa\s+assess\b|censys_tsa\.py/.test(command)) return 2 // two counts
  if (/\btsa\s+search\b|censys_query\.py/.test(command)) return 1
  return 0 // cve, credits, budget, timeline, report, ref and doc are all free
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

/** State shared across every instance of this plugin in the process.
 *
 *  This file can legitimately be loaded twice: once from
 *  ~/.config/opencode/plugin/ (the global install) and once from a project's own
 *  .opencode/plugin/ - which is exactly what happens to anyone who clones this
 *  kit and then opens it in opencode. Two loads mean two module instances, and
 *  with per-instance state the consequences are silent and confusing: the
 *  `tsa_capabilities` tool registration that wins writes to one instance's map,
 *  while the other instance's `tool.execute.before` hook still sees nothing
 *  registered and blocks a call the user just authorised.
 *
 *  Hanging the maps off globalThis makes the instances agree. */
type SharedState = {
  byRoot: Map<string, Caps>
  rootMemo: Map<string, string>
  agentsBySession: Map<string, Set<string>>
}

const STATE_KEY = "__tsaCapabilitiesState"

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

export const TsaCapabilities: Plugin = async ({ client }) => {
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

  /**
   * Should this plugin police this session at all?
   *
   * Three ways to say yes, in order of cost:
   *
   *  1. the session's own agent is a TSA agent - decisive, no I/O. A TSA
   *     subagent always runs in its own session under its own name.
   *  2. its root session is a TSA session - the case where a TSA orchestrator
   *     delegates to something whose name we do not recognise.
   *  3. capabilities were explicitly registered for its root. Only a TSA
   *     agent's step -1 does that, and doing it deliberately from anywhere else
   *     is an opt-in.
   *
   * Otherwise: no. Every unrelated session on the machine ends here, which is
   * the whole point - this plugin is installed globally and fail-closed, so an
   * unscoped version would block `webfetch` in every project the user opens.
   */
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

  return {
    /**
     * Agent identification. `tool.execute.before` is not given the agent, so
     * these two hooks are the only way to know whose tool call we are looking
     * at. Both fire before the first tool call of a session; see the ordering
     * transcript in this file's header.
     */
    "chat.message": async (input) => {
      recordAgent(input.sessionID, input.agent)
    },
    "chat.params": async (input) => {
      recordAgent(input.sessionID, input.agent)
    },

    tool: {
      tsa_capabilities: tool({
        description:
          "Record or read the capability set for this Censys TSA run. Only relevant to the " +
          "censys-tsa agents; ignore it in any other context. `censys-tsa` calls this once " +
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
          rateLimit: tool.schema.enum(["none", "fast", "standard"]).optional()
            .describe(
              "how fast Censys requests may be issued. NOT enforced here - after " +
              "registering, run `tsa limits <profile>` so every subagent's calls " +
              "pick it up. 'none' = no pacing (credits are still capped).",
            ),
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
          recordAgent(context.sessionID, context.agent)
          const { root, caps } = await capsFor(context.sessionID)
          if (args.action === "get") {
            return `Capabilities for this TSA run:\n${summarise(caps)}`
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
          return (
            `Capabilities registered and now enforced for every subagent in this run:\n${summarise(caps)}\n\n` +
            `NEXT: run \`tsa limits ${caps.rateLimit}\` in a shell now. Pacing lives in ` +
            `the Python tools, not at the tool boundary, so it is the only capability ` +
            `here this plugin cannot apply for you.`
          )
        },
      }),
    },

    /**
     * Hard enforcement. Fires for every tool call in every session on the
     * machine, including subagent child sessions - so the first thing it does is
     * establish that this session is part of a TSA run at all. Throwing here
     * blocks the call outright, regardless of what the agent's static
     * permissions say.
     */
    "tool.execute.before": async (input, output) => {
      if (input.tool === "tsa_capabilities") return
      if (!(await governed(input.sessionID))) return
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
