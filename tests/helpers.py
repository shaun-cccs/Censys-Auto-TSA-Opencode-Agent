#!/usr/bin/env python3
"""Shared helpers for the test suite.

No third-party test runner: the repo already standardises on ``unittest``
(see ``utils/test_censys_credits.py``), and adding a dependency to run tests
would be a poor trade for a project whose whole point is auditability.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parent.parent

# The canonical skill that references/ was carved from. External to this repo
# and therefore optional - carve tests skip cleanly when it is absent.
SKILL_MD = Path.home() / ".claude" / "skills" / "censys-auto-tsa" / "SKILL.md"

AGENT_DIR = ROOT / ".opencode" / "agent"
PLUGIN_TS = ROOT / ".opencode" / "plugins" / "tsa-capabilities.ts"
REFERENCES = ROOT / "references"

AGENTS = [
    "censys-tsa",
    "censys-tsa-auto",
    "censys-fingerprint",
    "censys-deepdive",
    "censys-report",
]

ORCHESTRATORS = ["censys-tsa", "censys-tsa-auto"]
SUBAGENTS = ["censys-fingerprint", "censys-deepdive", "censys-report"]


def load_bin_tsa():
    """Import ``bin/tsa`` as a module despite it having no .py extension."""
    loader = importlib.machinery.SourceFileLoader("bin_tsa", str(ROOT / "bin" / "tsa"))
    spec = importlib.util.spec_from_loader("bin_tsa", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def frontmatter(agent: str) -> Dict[str, Any]:
    """Parse an agent markdown file's YAML frontmatter."""
    import yaml

    text = (AGENT_DIR / f"{agent}.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise AssertionError(f"{agent}.md has no YAML frontmatter")
    return yaml.safe_load(match.group(1)) or {}


def body(agent: str) -> str:
    """The prompt body of an agent file, frontmatter stripped."""
    text = (AGENT_DIR / f"{agent}.md").read_text()
    return re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)


def flat(text: str) -> str:
    """Collapse all whitespace to single spaces.

    Prompt files are hard-wrapped, so a phrase that reads as one sentence is
    often split across lines. Assertions on prose should not break because a
    sentence was rewrapped.
    """
    return re.sub(r"\s+", " ", text)


def opencode_available() -> bool:
    return shutil.which("opencode") is not None


def resolved_permissions() -> Dict[str, Dict[str, str]]:
    """Ask opencode for each agent's *resolved* permissions.

    Static frontmatter is what we wrote; this is what opencode actually
    computed after merging global config, project config and agent overrides.
    Testing the resolved view is what catches a config that silently loses to
    a higher-precedence rule.

    Returns ``{agent: {permission: action}}`` for wildcard patterns only.
    """
    import json

    out = subprocess.run(
        ["opencode", "agent", "list"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    ).stdout

    result: Dict[str, Dict[str, str]] = {}
    blocks = re.split(r"^(\S+) \((primary|subagent|all)\)$", out, flags=re.M)
    for i in range(1, len(blocks), 3):
        name = blocks[i]
        match = re.search(r"\[.*?\n\]", blocks[i + 2], re.S)
        if not match:
            continue
        perms = json.loads(match.group(0))
        result[name] = {
            p["permission"]: p["action"] for p in perms if p.get("pattern") == "*"
        }
    return result


def ts_regex(name: str) -> str:
    """Extract a literal regex from the plugin's TypeScript source.

    The gating patterns live in TypeScript and cannot be imported here. Rather
    than duplicating them (which would drift silently), the tests read the real
    source. A change to the plugin therefore changes what the tests check.
    """
    source = PLUGIN_TS.read_text()
    patterns = {
        # The body may contain escaped slashes (e.g. https?:\/\/), so match
        # either a non-slash character or any backslash-escaped pair.
        "endpoint_probe": r"if \(/((?:[^/\\]|\\.)+)/\.test\(text\)\)",
    }
    match = re.search(patterns[name], source)
    if not match:
        raise AssertionError(
            f"could not find the {name!r} regex in {PLUGIN_TS.name}; "
            "the test needs updating alongside the plugin"
        )
    return match.group(1)


def censys_cost_simulator():
    """Build a Python callable that mirrors the plugin's ``censysCost``.

    The budget rules are TypeScript and cannot be imported, but asserting on
    the source *text* is fragile - it matches prose in comments as readily as
    real rules. Instead the rules are parsed out of the function body and
    replayed here, so the tests exercise behaviour against real command
    strings and stay honest when the plugin changes.
    """
    source = PLUGIN_TS.read_text()
    match = re.search(
        r"function censysCost\(command: string\): number \{(.*?)\n\}", source, re.S
    )
    if not match:
        raise AssertionError("censysCost is missing from the plugin")

    stripped = re.sub(r"//.*", "", match.group(1))
    lines = [line.strip() for line in stripped.splitlines() if line.strip()]

    def parse(index):
        rules = []
        while index < len(lines):
            line = lines[index]
            if line == "}":
                return rules, index + 1
            if m := re.match(r"if \(!command\) return (\d+)$", line):
                rules.append(("empty", None, int(m.group(1))))
            elif m := re.match(r"if \(/(.+?)/\.test\(command\)\) return (\d+)$", line):
                rules.append(("leaf", m.group(1), int(m.group(2))))
            elif m := re.match(r"if \(/(.+?)/\.test\(command\)\) \{$", line):
                nested, index = parse(index + 1)
                rules.append(("block", m.group(1), nested))
                continue
            elif m := re.match(r"return (\d+)$", line):
                rules.append(("default", None, int(m.group(1))))
            index += 1
        return rules, index

    tree, _ = parse(0)

    def evaluate(command, rules=None):
        for kind, pattern, payload in tree if rules is None else rules:
            if kind == "empty" and not command:
                return payload
            if kind == "leaf" and re.search(pattern, command):
                return payload
            if kind == "block" and re.search(pattern, command):
                return evaluate(command, payload)
            if kind == "default":
                return payload
        return 0

    return evaluate


def run_agent(prompt: str, agent: str = "build", caps: Optional[str] = None,
              timeout: int = 300) -> str:
    """Run a real opencode agent and return its combined output.

    Used only by the live enforcement tests. Costs model tokens but zero Censys
    credits - every prompt is designed so the blocked path throws before any
    Censys call executes.
    """
    env = dict(os.environ)
    if caps is not None:
        env["TSA_CAPABILITIES"] = caps
    else:
        env.pop("TSA_CAPABILITIES", None)

    proc = subprocess.run(
        [
            "opencode", "run",
            "--agent", agent,
            "--dir", str(ROOT),
            "--auto",
            prompt,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    return (proc.stdout or "") + (proc.stderr or "")
