#!/usr/bin/env python3
"""Non-interactive Censys TSA driver. Reached as `tsa run`.

Runs the `censys-tsa-auto` opencode agent against a target and emits the
resulting report spec as JSON on stdout.

Everything is relative to the CURRENT DIRECTORY, not to the kit: the agent runs
with `--dir $PWD`, and the durable output contract is
``./reports/<slug>.spec.json`` - the same schema `tsa report --template` defines.
We deliberately do not parse ``opencode run --format json`` event output, which
is a raw event stream and not a result object.

Examples
--------
    tsa run "Ivanti EPMM"
    tsa run --cve CVE-2024-21762
    tsa run --cve CVE-2024-21762 --product "Fortinet FortiOS"
    tsa run --country Australia "Flowise"
    tsa run --allow-web --deep-dive --budget 50 "Ivanti EPMM"
    tsa run --slug lobehub-2.2.13 "LobeHub 2.2.13"

For an INTERACTIVE run with the startup capability interview, use the opencode
TUI and switch to the `censys-tsa` agent. This wrapper cannot host the
interview: `opencode run` has no UI for the `question` tool, so an interactive
agent would hang waiting for an answer.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

#  The kit's own directory - used for nothing but locating this file, and
#  emphatically not as a working directory. A user runs `tsa run` from their own
#  project, and the artifacts belong there, next to the work.
KIT = Path(__file__).resolve().parent.parent

#  Where the agent runs and where we look for its output.
WORKDIR = Path(os.environ.get("CENSYS_TSA_WORKDIR") or Path.cwd()).resolve()
REPORTS = Path(os.environ.get("CENSYS_TSA_REPORT_DIR") or (WORKDIR / "reports"))

AUTO_AGENT = "censys-tsa-auto"


def slugify(text: str) -> str:
    """Lowercase, hyphenated, filesystem-safe.

    Dots are preserved so version numbers survive intact, matching the existing
    reports/ naming convention (`lobechat-1.123.1`, `jellyfin-media-system-10.11.0`).
    Replacing them would silently fork the naming scheme and break diffs against
    previously written specs.
    """
    slug = re.sub(r"[^a-z0-9.]+", "-", text.lower()).strip("-.")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "assessment"


def extract_spec(text: str):
    """Recover the last parseable TSA spec from an agent's output.

    Only used with --no-reports, where nothing is written to disk. Scans for
    ```json fenced blocks, newest first, and returns the first one that looks
    like a spec. Returns None if nothing qualifies.
    """
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, re.S)
    # The event stream escapes newlines inside JSON strings; try those too.
    blocks += re.findall(r"```json\\n(\{.*?\})\\n```", text, re.S)
    for raw in reversed(blocks):
        candidate = raw.replace("\\n", "\n").replace('\\"', '"')
        for attempt in (raw, candidate):
            try:
                obj = json.loads(attempt)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and "baseline" in obj:
                return obj
    return None


VERSION_IN_TARGET = re.compile(r"\d+\.\d+")
CVE_IN_TARGET = re.compile(r"\bCVE-\d{4}-\d{4,}\b", re.I)


def wants_version_breakdown(args: argparse.Namespace) -> tuple[bool, str]:
    """Decide whether a per-version distribution should be produced.

    Off by default. On when the user asked, when a CVE drives the run, or when
    the target names a specific version - in those cases version work is the
    point of the assessment rather than an expensive extra.

    The version test is a regex for a dotted number, so a product whose *name*
    contains one could over-trigger. That fails cheap: you get a table you did
    not need, and the resolved capability set is echoed before any credit is
    spent. Over-triggering beats silently skipping a versioned target.
    """
    if args.version_breakdown:
        return True, "requested with --version-breakdown"
    if args.cve:
        return True, "CVE target: version work is intrinsic"
    # A CVE can also arrive as the positional target rather than via --cve.
    # Its ID contains no dotted number, so the version regex below misses it.
    if args.target and CVE_IN_TARGET.search(args.target):
        return True, "CVE named in the target: version work is intrinsic"
    for text in (args.target, args.product):
        if text and VERSION_IN_TARGET.search(text):
            return True, f"target names a version ({text!r})"
    return False, "baseline only"


def build_capabilities(args: argparse.Namespace) -> str:
    """Serialise capabilities for the TSA_CAPABILITIES env var the plugin reads.

    Defaults are fail-closed: no network, no deep dive, no version breakdown.
    Only report-writing is on by default, because reports/<slug>.spec.json is
    this wrapper's output contract.

    Pacing is the exception to fail-closed, because it is a throughput knob and
    not a safety capability: the default is `fast`, which is bounded an order of
    magnitude above a whole run but never stalls one. `--rate none` removes
    pacing entirely; credits are capped separately by --budget.
    """
    breakdown, _ = wants_version_breakdown(args)
    # With no file written there is nothing for this wrapper to read, so the
    # fenced json block becomes the only way to recover the spec. Independent of
    # that, --print-spec asks for the block alongside the files.
    print_spec = args.print_spec or args.no_reports
    return " ".join(
        [
            f"webfetch={'on' if args.allow_web else 'off'}",
            f"websearch={'on' if args.allow_web else 'off'}",
            f"endpoint={'on' if args.allow_endpoint_check else 'off'}",
            f"deepdive={'always' if args.deep_dive else 'never'}",
            f"versionbreakdown={'on' if breakdown else 'off'}",
            f"reports={'off' if args.no_reports else 'on'}",
            f"printspec={'on' if print_spec else 'off'}",
            f"rate={args.rate}",
            f"budget={args.budget if args.budget else 0}",
        ]
    )


def apply_rate_profile(rate: str) -> str:
    """Persist the pacing profile before the agent starts.

    Done here rather than left to the agent on purpose. Pacing is read from a
    state file by every Censys subcommand in every subagent, so it has to be set
    before the first call - and an unattended run has nobody to notice that the
    agent skipped the step. `tsa limits` is the only way to set it; this wrapper
    knows where `tsa` is because it was invoked through it.
    """
    tsa = shutil.which("tsa") or str(KIT / "bin" / "tsa")
    try:
        proc = subprocess.run(
            [tsa, "limits", rate, "--by", "tsa run"],
            capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"could not set pacing ({exc}); the tools will use their own default"
    if proc.returncode != 0:
        return f"could not set pacing: {(proc.stderr or '').strip()[:120]}"
    return f"pacing profile set to {rate}"


def build_prompt(args: argparse.Namespace, slug: str, capabilities: str) -> str:
    if args.cve and args.product:
        target = f"{args.cve}, scoped to the product {args.product}"
    elif args.cve:
        target = args.cve
    else:
        target = args.target

    lines = [
        f"Compute a Threat Surface Assessment for: {target}",
        "",
        f"CAPABILITIES: {capabilities}",
        "",
    ]

    lines += [
        "This is an unattended run. There is no user to ask. Do not attempt",
        "any capability that is off above - the plugin will block it. Record",
        "every skipped gate in `caveats`.",
        "",
    ]

    lines += [
        f"Country scope for the second count: {args.country}",
        f"Use the slug `{slug}` for all output files.",
        "",
    ]

    if args.no_reports:
        lines += [
            "Report writing is disabled. Do NOT invoke @censys-report.",
            "Still print the normal compact summary - product, baseline query and",
            "counts, widened query if any, basis and credits, caveats - and simply",
            "omit the `Full report:` line.",
        ]
    else:
        lines += [
            "You MUST finish by invoking @censys-report so that",
            f"reports/{slug}.spec.json and reports/{slug}.md exist on disk.",
            "A run that produces no spec file is a failed run.",
        ]

    if args.print_spec or args.no_reports:
        lines += [
            "",
            "Below the summary, append the fully assembled spec as a single JSON",
            "object inside a ```json fenced block. The block is in addition to the",
            "summary, never instead of it.",
        ]

    if args.note:
        lines += ["", f"Additional context from the caller: {args.note}"]
    return "\n".join(lines)


def main() -> int:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa assess"), not this file, which is not on their PATH.
    p = argparse.ArgumentParser(
        prog=os.environ.get("CENSYS_TSA_PROG", "tsa run"),
        description="Run a Censys TSA non-interactively and emit the report spec as JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("target", nargs="?", help="Product, vendor or appliance to assess")
    p.add_argument("--cve", help="CVE ID to drive or scope the assessment")
    p.add_argument("--product", help="Product to scope a --cve run to")
    p.add_argument("--country", default="Canada", help="Country for the second count")
    p.add_argument("--slug", help="Output slug (default: derived from the target)")
    p.add_argument("--note", help="Extra context to pass through to the agent")
    p.add_argument("--model", help="Override the model, as provider/model")
    p.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Seconds to allow the agent run before giving up",
    )
    p.add_argument(
        "--keep-going",
        action="store_true",
        help="Emit the spec even if the agent run exited non-zero",
    )
    p.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the generated prompt and exit without running anything",
    )

    caps = p.add_argument_group(
        "capabilities",
        "All default to OFF (fail-closed) except --reports. The network and budget "
        "capabilities are hard-enforced by the tsa-capabilities plugin across every "
        "subagent. --version-breakdown is advisory only: a version aggregation is "
        "indistinguishable from any other, so nothing blocks it.",
    )
    caps.add_argument(
        "--allow-web",
        action="store_true",
        help="Enable webfetch + websearch, unlocking step 3b and step 0b tier-2b",
    )
    caps.add_argument(
        "--allow-endpoint-check",
        action="store_true",
        help="Allow the agent to ask you to run a request against a host you own",
    )
    caps.add_argument(
        "--deep-dive",
        action="store_true",
        help="Pre-authorise the step 8 signature hunt",
    )
    caps.add_argument(
        "--budget",
        type=int,
        metavar="N",
        help="Ceiling on estimated Censys credits; a coarse circuit-breaker, not an accountant",
    )
    caps.add_argument(
        "--rate",
        choices=("none", "fast", "standard"),
        default="fast",
        help="Censys request pacing. none = no pacing at all; fast = bounded but "
             "never in the way; standard = the original conservative pacing, which "
             "is below what one assessment needs and will stall it",
    )
    caps.add_argument(
        "--version-breakdown",
        action="store_true",
        help="Produce a per-version distribution table (auto-on for --cve or a versioned target)",
    )
    caps.add_argument(
        "--no-reports",
        action="store_true",
        help="Do not write reports/<slug>.*; recover the spec from the agent's message instead",
    )
    caps.add_argument(
        "--print-spec",
        action="store_true",
        help="Also print the spec as a json block below the summary (implied by --no-reports)",
    )
    args = p.parse_args()

    if not args.target and not args.cve:
        p.error("give a target, or --cve, or both")
    if args.product and not args.cve:
        p.error("--product only makes sense together with --cve")
    if shutil.which("opencode") is None:
        print("error: `opencode` is not on PATH", file=sys.stderr)
        return 127

    slug = args.slug or slugify(args.target or args.product or args.cve)
    spec_path = REPORTS / f"{slug}.spec.json"
    capabilities = build_capabilities(args)
    prompt = build_prompt(args, slug, capabilities)

    if args.print_prompt:
        _, why = wants_version_breakdown(args)
        print(f"# TSA_CAPABILITIES={capabilities}")
        print(f"# version breakdown: {why}\n")
        print(prompt)
        return 0

    agent = AUTO_AGENT
    cmd = [
        "opencode", "run",
        "--agent", agent,
        "--dir", str(WORKDIR),
        "--format", "json",
        "--title", f"TSA {slug}",
    ]
    cmd.append("--auto")
    if args.model:
        cmd += ["--model", args.model]
    cmd.append(prompt)

    # The plugin reads this at session start and enforces it across subagents.
    env = {**os.environ, "TSA_CAPABILITIES": capabilities}

    mtime_before = spec_path.stat().st_mtime if spec_path.exists() else 0.0
    started = time.time()

    print(f"[tsa] agent={agent} slug={slug}", file=sys.stderr)
    print(f"[tsa] caps ={capabilities}", file=sys.stderr)
    print(f"[tsa] {apply_rate_profile(args.rate)}", file=sys.stderr)
    _, why = wants_version_breakdown(args)
    print(f"[tsa] version breakdown: {why}", file=sys.stderr)
    if args.no_reports:
        print("[tsa] reports disabled: spec comes from the agent's final message", file=sys.stderr)
    else:
        print(f"[tsa] spec ={spec_path}", file=sys.stderr)

    try:
        if args.no_reports:
            # Need the agent's own output to recover the spec, so capture it.
            # Live progress is sacrificed only on this less-common path.
            proc = subprocess.run(
                cmd, cwd=WORKDIR, capture_output=True, text=True,
                timeout=args.timeout, env=env,
            )
            sys.stderr.write(proc.stdout or "")
            sys.stderr.write(proc.stderr or "")
            captured = (proc.stdout or "") + (proc.stderr or "")
        else:
            # The event stream goes to stderr so stdout stays a clean JSON channel.
            proc = subprocess.run(
                cmd, cwd=WORKDIR, stdout=sys.stderr, stderr=sys.stderr,
                timeout=args.timeout, env=env,
            )
            captured = ""
    except subprocess.TimeoutExpired:
        print(f"[tsa] timed out after {args.timeout}s", file=sys.stderr)
        return 124

    elapsed = time.time() - started
    print(f"[tsa] agent exited {proc.returncode} after {elapsed:.0f}s", file=sys.stderr)

    if proc.returncode != 0 and not args.keep_going:
        return proc.returncode

    if args.no_reports:
        spec = extract_spec(captured)
        if spec is None:
            print(
                "[tsa] FAILED: --no-reports was set but no parseable ```json spec "
                "was found in the agent's output.",
                file=sys.stderr,
            )
            return 1
        print(
            "[tsa] WARNING: spec recovered from the agent's message, not from a "
            "rendered file. It has not been validated by tsa_report.py.",
            file=sys.stderr,
        )
    else:
        if not spec_path.exists():
            print(
                f"[tsa] FAILED: the agent produced no {spec_path.name}. "
                "The spec file is the output contract; treat this run as failed.",
                file=sys.stderr,
            )
            return 1
        if spec_path.stat().st_mtime <= mtime_before:
            print(
                f"[tsa] FAILED: {spec_path.name} exists but was not rewritten by this run.",
                file=sys.stderr,
            )
            return 1
        try:
            spec = json.loads(spec_path.read_text())
        except json.JSONDecodeError as exc:
            print(f"[tsa] FAILED: {spec_path.name} is not valid JSON: {exc}", file=sys.stderr)
            return 1

    missing = [k for k in ("product", "baseline") if k not in spec]
    if missing:
        print(f"[tsa] FAILED: spec is missing required keys: {missing}", file=sys.stderr)
        return 1

    json.dump(spec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
