#!/usr/bin/env python3
"""Guards that keep this kit installable on someone else's machine.

Every test here corresponds to a way this kit was, at some point, not portable:

- prompts that named `python utils/x.py` - wrong from any directory but the
  kit's own, and there is no `python` at all on many machines
- prompts that named an absolute path, which freezes the install location
- a capability plugin whose governed-agent list drifted from the agents on disk
- an installer whose link set drifted from what the agents actually need

All static or filesystem-level: no opencode, no Censys, no network.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.helpers import (
    AGENT_DIR,
    AGENTS,
    BIN_TSA,
    body,
    flat,
    frontmatter,
    INSTALL_SH,
    PLUGIN_TS,
    REFERENCES,
    ROOT,
    SKILL_DIR,
    shipped_prompts,
    tsa,
)

UTILS = ROOT / "utils"


class NoPathsInShippedProse(unittest.TestCase):
    """Rule 1 of the contributor guide, mechanised.

    The agents run inside a user's project, so a relative path resolves against
    the wrong directory and an absolute path pins the kit to wherever it
    happened to be built. Both are banned outright; `tsa ref` and `tsa doc`
    exist precisely so that reading this kit's own documentation needs neither.
    """

    #  `reports/` is the deliberate exception: it is where output goes, relative
    #  to the user's own working directory, and saying so is the point.
    ALLOWED = ("reports/",)

    def shipped(self):
        return shipped_prompts()

    @staticmethod
    def prose(path):
        """A file's shipped prose, with HTML comments blanked out.

        Comments are addressed to whoever edits the file, not to the model, and
        a provenance note or a "regenerate with gen_agents.py" hint is allowed
        to name a repo path. Blanked rather than removed so line numbers in
        assertions still point at the real line.
        """
        text = path.read_text()
        return re.sub(
            r"<!--.*?-->",
            lambda m: re.sub(r"[^\n]", " ", m.group(0)),
            text,
            flags=re.S,
        )

    def test_no_absolute_paths(self):
        #  No `~/.censys*` exemption. There used to be one, and it cost 45
        #  minutes: `references/workspace.md` named the rate-state file by path,
        #  a `censys-deepdive` subagent dutifully read it, and reading outside
        #  the workspace raised an `external_directory` permission prompt that no
        #  subagent has a UI to answer. State files are reached through
        #  `tsa budget` and `tsa credits`; see rule 4 of the contributor guide.
        pattern = re.compile(r"(/home/|/Users/|/opt/|\$HOME/|~/)")
        for path in self.shipped():
            for lineno, line in enumerate(self.prose(path).splitlines(), 1):
                with self.subTest(file=path.name, line=lineno):
                    self.assertIsNone(
                        pattern.search(line),
                        f"{path.name}:{lineno} names an absolute path: {line.strip()!r}",
                    )

    def test_no_script_paths(self):
        """`utils/`, `docs/` and `references/` must never appear as paths."""
        pattern = re.compile(r"\b(utils|docs|references|scripts)/")
        for path in self.shipped():
            for lineno, line in enumerate(self.prose(path).splitlines(), 1):
                with self.subTest(file=path.name, line=lineno):
                    self.assertIsNone(
                        pattern.search(line),
                        f"{path.name}:{lineno} names a kit path: {line.strip()!r}. "
                        "Use a `tsa` subcommand instead.",
                    )

    def test_no_interpreter_invocations(self):
        """No `python`, no `pip`. `tsa` decides how to run things."""
        pattern = re.compile(r"(?<![-\w])(python3?|pip3?)\s")
        for path in self.shipped():
            for lineno, line in enumerate(self.prose(path).splitlines(), 1):
                with self.subTest(file=path.name, line=lineno):
                    self.assertIsNone(
                        pattern.search(line),
                        f"{path.name}:{lineno} invokes an interpreter: {line.strip()!r}",
                    )

    def test_no_cd(self):
        """A `cd` in a prompt is a path in disguise."""
        for path in self.shipped():
            for lineno, line in enumerate(self.prose(path).splitlines(), 1):
                with self.subTest(file=path.name, line=lineno):
                    self.assertFalse(
                        line.strip().startswith("cd "),
                        f"{path.name}:{lineno} changes directory: {line.strip()!r}",
                    )


class PrinciplesAreGenerated(unittest.TestCase):
    """The seven principles have one source and five copies. Keep them equal.

    They cannot simply be read at runtime: a globally installed kit has no
    project AGENTS.md, and "always loaded" has to mean *in the system prompt*.
    """

    def test_in_sync(self):
        proc = subprocess.run(
            ["python3", str(ROOT / "scripts" / "gen_agents.py"), "--check"],
            cwd=ROOT, capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_every_agent_carries_them(self):
        source = (REFERENCES / "principles.md").read_text()
        sentinel = "never contact assessed hosts directly"
        self.assertIn(sentinel, source)
        for agent in AGENTS:
            with self.subTest(agent=agent):
                self.assertIn(sentinel, (AGENT_DIR / f"{agent}.md").read_text())

    def test_source_is_not_itself_shipped_with_a_path(self):
        """principles.md is a reference like any other: no paths in the body."""
        body = (REFERENCES / "principles.md").read_text()
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)  # maintainer notes are exempt
        self.assertNotIn("utils/", body)
        self.assertNotIn("/home/", body)


class PluginScope(unittest.TestCase):
    """The plugin is installed globally, so its reach must be exact.

    It fires `tool.execute.before` for every tool call in every session on the
    machine and its defaults are fail-closed. If the governed-agent list ever
    drifts from the agents on disk, the failure is silent and severe in both
    directions: an unlisted agent runs ungated, and a stale name means nothing
    at all. So the list is checked against the filesystem.
    """

    def setUp(self):
        self.source = PLUGIN_TS.read_text()

    def governed_agents(self):
        match = re.search(r"const TSA_AGENTS = new Set\(\[(.*?)\]\)", self.source, re.S)
        self.assertIsNotNone(match, "TSA_AGENTS is missing from the plugin")
        return set(re.findall(r'"([^"]+)"', match.group(1)))

    def test_governed_agents_match_the_agent_files(self):
        on_disk = {p.stem for p in AGENT_DIR.glob("*.md")}
        self.assertEqual(self.governed_agents(), on_disk)

    def test_enforcement_is_scoped(self):
        """The gate must run before any capability check, or the plugin polices
        every unrelated project on the machine."""
        hook = re.search(
            r'"tool\.execute\.before": async \(input, output\) => \{(.*?)\n      if \(input\.tool === "webfetch"',
            self.source, re.S,
        )
        self.assertIsNotNone(hook, "the enforcement hook changed shape")
        self.assertIn("governed(input.sessionID)", hook.group(1))

    def test_agent_is_learned_from_the_chat_hooks(self):
        """`tool.execute.before` is not told the agent; these hooks are."""
        self.assertIn('"chat.message"', self.source)
        self.assertIn('"chat.params"', self.source)
        self.assertIn("recordAgent", self.source)

    def test_state_is_shared_across_plugin_instances(self):
        """This file loads twice for anyone who clones the kit AND installs it:
        once from ~/.config/opencode/plugin/ and once from the checkout's own
        .opencode/plugin/. With per-instance state, the instance whose tool
        registration lost would keep blocking calls the user just authorised."""
        self.assertIn("globalThis", self.source)
        self.assertIn("sharedState()", self.source)
        self.assertNotIn("const byRoot = new Map", self.source)

    def test_internal_agents_are_not_mistaken_for_the_real_one(self):
        """opencode's `title` agent runs inside another agent's session."""
        match = re.search(r"const INTERNAL_AGENTS = new Set\(\[(.*?)\]\)", self.source, re.S)
        self.assertIsNotNone(match)
        self.assertIn("title", re.findall(r'"([^"]+)"', match.group(1)))


class Shim(unittest.TestCase):
    """`bin/tsa` is the only interface to the kit. It must be complete."""

    def dispatch_table(self):
        """Map subcommand -> script, parsed out of the shim's case statement."""
        source = BIN_TSA.read_text()
        block = source.split("case $command in", 1)[1]
        table = {}
        for names, kind, script in re.findall(
            r"^\s+([\w |]+?)\)\s+run_(dep|stdlib) (\S+\.py)", block, re.M
        ):
            for name in names.split("|"):
                table[name.strip()] = script
        return table

    def test_posix_sh_syntax(self):
        for shell in ("sh", "dash", "bash"):
            if not shutil.which(shell):
                continue
            with self.subTest(shell=shell):
                proc = subprocess.run([shell, "-n", str(BIN_TSA)], capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_every_dispatched_script_exists(self):
        table = self.dispatch_table()
        self.assertTrue(table, "no subcommands parsed out of the shim")
        for command, script in table.items():
            with self.subTest(command=command):
                self.assertTrue((UTILS / script).exists(), f"{script} is missing")

    def test_every_entrypoint_is_reachable(self):
        """A util nobody can run is a util the agents cannot use."""
        dispatched = set(self.dispatch_table().values())
        for path in sorted(UTILS.glob("*.py")):
            with self.subTest(script=path.name):
                self.assertIn(path.name, dispatched)

    def test_sdk_and_stdlib_scripts_are_routed_correctly(self):
        """Only the scripts that import the SDK may need uv.

        `tsa report` and `tsa cve` are the offline half of this kit; routing
        either through uv would make rendering a report impossible on a machine
        with no dependencies installed.
        """
        source = BIN_TSA.read_text()
        block = source.split("case $command in", 1)[1]
        for names, kind, script in re.findall(
            r"^\s+([\w |]+?)\)\s+run_(dep|stdlib) (\S+\.py)", block, re.M
        ):
            text = (UTILS / script).read_text()
            needs_sdk = "censys_platform" in text or "from censys_query import" in text
            with self.subTest(script=script):
                self.assertEqual(
                    kind, "dep" if needs_sdk else "stdlib",
                    f"{script} is routed through run_{kind} but "
                    f"{'needs' if needs_sdk else 'does not need'} the SDK",
                )

    def test_help_and_home_work_from_anywhere(self):
        with tempfile.TemporaryDirectory() as elsewhere:
            proc = tsa("help", cwd=elsewhere)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("tsa assess", proc.stdout)
            proc = tsa("home", cwd=elsewhere)
            self.assertEqual(proc.stdout.strip(), str(ROOT))

    def test_resolves_itself_through_a_symlink(self):
        """The whole design rests on this: the shim is invoked via a symlink in
        ~/.local/bin and must still find the kit."""
        with tempfile.TemporaryDirectory() as tmp:
            link = Path(tmp) / "tsa"
            link.symlink_to(BIN_TSA)
            proc = subprocess.run(
                [str(link), "home"], capture_output=True, text=True, cwd=tmp, timeout=60
            )
            self.assertEqual(proc.stdout.strip(), str(ROOT), proc.stderr)

    def test_unknown_subcommand_fails_loudly(self):
        proc = tsa("nonsense")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unknown subcommand", proc.stderr)


class RefAndDoc(unittest.TestCase):
    """The agents read the kit's documentation through these two subcommands."""

    def test_every_reference_is_printable(self):
        for path in sorted(REFERENCES.glob("*.md")):
            with self.subTest(reference=path.stem):
                proc = tsa("ref", path.stem)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertGreater(len(proc.stdout), 200)

    def test_ref_listing_covers_every_reference(self):
        listing = tsa("ref").stdout
        for path in sorted(REFERENCES.glob("*.md")):
            with self.subTest(reference=path.stem):
                self.assertIn(path.stem, listing)

    def test_every_referenced_ref_name_exists(self):
        """A prompt telling an agent to run `tsa ref nope` wastes a turn."""
        names = {p.stem for p in REFERENCES.glob("*.md")}
        for path in shipped_prompts():
            for name in re.findall(r"tsa ref ([a-z][a-z-]*)", path.read_text()):
                with self.subTest(file=path.name, name=name):
                    self.assertIn(name, names)

    def test_every_doc_alias_resolves(self):
        aliases = re.findall(
            r"^\s+([\w |-]+?)\)\s+printf '%s\\n' \"\$DOCS", BIN_TSA.read_text(), re.M
        )
        self.assertTrue(aliases)
        for group in aliases:
            for alias in group.split("|"):
                alias = alias.strip()
                with self.subTest(alias=alias):
                    proc = tsa("doc", alias, "--grep", "host")
                    self.assertIn(proc.returncode, (0, 1), proc.stderr)
                    self.assertNotIn("no such doc", proc.stderr)

    def test_every_referenced_doc_name_exists(self):
        aliases = set()
        for group in re.findall(
            r"^\s+([\w |-]+?)\)\s+printf '%s\\n' \"\$DOCS", BIN_TSA.read_text(), re.M
        ):
            aliases.update(a.strip() for a in group.split("|"))
        for path in shipped_prompts():
            for name in re.findall(r"tsa doc ([a-z][a-z-]*)", path.read_text()):
                with self.subTest(file=path.name, name=name):
                    self.assertIn(name, aliases)


class PromptMatchesItsPermissions(unittest.TestCase):
    """A prompt that misdescribes its own frontmatter is worse than silent.

    `censys-tsa-auto` shipped for a while telling itself that "the `question` and
    `webfetch` tools are denied to you by design" while its frontmatter said
    `webfetch: allow` and the rest of the same file explained how `--allow-web`
    enables web research. An agent that believes a granted capability is denied
    quietly declines work the caller asked and paid for, and no static check
    noticed - which is what this class is for.
    """

    NETWORK_TOOLS = ("webfetch", "websearch")

    def frontmatter_action(self, agent, tool):
        perms = frontmatter(agent).get("permission", {}) or {}
        return perms.get(tool)

    def test_no_agent_claims_a_granted_tool_is_denied(self):
        for agent in AGENTS:
            text = flat(body(agent))
            for tool in self.NETWORK_TOOLS:
                if self.frontmatter_action(agent, tool) != "allow":
                    continue
                with self.subTest(agent=agent, tool=tool):
                    #  Prose that puts the tool and a denial in the same clause.
                    #  Deliberately narrow: "blocked if you were not granted it"
                    #  is correct and must keep passing.
                    claim = re.search(
                        rf"\b{tool}\b[^.]{{0,80}}\b(is|are) denied|"
                        rf"\bdenied[^.]{{0,80}}\b{tool}\b",
                        text,
                    )
                    self.assertIsNone(
                        claim,
                        f"{agent}.md says {tool} is denied, but its frontmatter "
                        f"allows it and the plugin gates it per run: "
                        f"{claim.group(0) if claim else ''!r}",
                    )

    def test_agents_denied_the_network_say_so(self):
        """The converse: censys-report is off the network and must know it."""
        for agent in AGENTS:
            if self.frontmatter_action(agent, "webfetch") != "deny":
                continue
            with self.subTest(agent=agent):
                found = re.search(
                    r"(?i)(no Censys calls|never calls Censys|no research)",
                    flat(body(agent)),
                )
                self.assertIsNotNone(
                    found,
                    f"{agent}.md is denied the network but never says so",
                )

    def test_question_is_described_correctly(self):
        """`question` is the one tool that really is denied outright, and only
        in the unattended agents - where there is nobody to answer.

        Assertions are written as searches with short messages on purpose: an
        assertRegex failure here would dump the whole 6 KB prompt into the test
        output, which buries the one line that is wrong.
        """
        for agent in AGENTS:
            action = self.frontmatter_action(agent, "question")
            text = flat(body(agent))
            with self.subTest(agent=agent):
                if action == "deny" and agent == "censys-tsa-auto":
                    self.assertIsNotNone(
                        re.search(r"(?i)`question` tool is denied", text),
                        f"{agent}.md denies `question` in frontmatter but never "
                        "tells the agent so, and it has no user to ask",
                    )
                if action == "allow":
                    claim = re.search(r"(?i)`question`[^.]{0,40}is denied", text)
                    self.assertIsNone(
                        claim,
                        f"{agent}.md may ask questions but says: "
                        f"{claim.group(0) if claim else ''!r}",
                    )


class Skill(unittest.TestCase):
    """The discovery skill is how a user's own agent finds the kit."""

    def test_lives_where_opencode_looks(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())

    def test_frontmatter_name_matches_the_directory(self):
        text = (SKILL_DIR / "SKILL.md").read_text()
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(match, "SKILL.md needs frontmatter")
        name = re.search(r"^name:\s*(\S+)", match.group(1), re.M)
        self.assertIsNotNone(name, "SKILL.md needs a name")
        self.assertEqual(name.group(1), SKILL_DIR.name)

    def test_has_a_description(self):
        """Skills without one are filtered out and never surfaced to a model."""
        text = (SKILL_DIR / "SKILL.md").read_text()
        match = re.search(r"^description:\s*(.+)$", text, re.M)
        self.assertIsNotNone(match)
        self.assertGreater(len(match.group(1)), 60, "describe what AND when")

    def test_hands_off_rather_than_reimplementing(self):
        body = (SKILL_DIR / "SKILL.md").read_text()
        self.assertIn("@censys-tsa", body)


class Installer(unittest.TestCase):
    """install.sh against a throwaway HOME. Creates nothing outside it."""

    def install(self, *extra, home):
        env = {
            "HOME": home,
            "CENSYS_TSA_CONFIG_DIR": f"{home}/.config/opencode",
            "CENSYS_TSA_BIN_DIR": f"{home}/bin",
            #  Skip `uv sync` and the opencode warm-up: this test is about the
            #  link set, and both would touch the network.
            "CENSYS_TSA_PYTHON": "/usr/bin/python3",
            "PATH": "/usr/bin:/bin",
        }
        return subprocess.run(
            ["sh", str(INSTALL_SH), *extra],
            capture_output=True, text=True, timeout=180, env=env, cwd=str(ROOT),
        )

    def expected_links(self, home):
        config = Path(home) / ".config" / "opencode"
        return {
            **{config / "agent" / f"{a}.md": AGENT_DIR / f"{a}.md" for a in AGENTS},
            config / "plugin" / "tsa-capabilities.ts": PLUGIN_TS,
            config / "skill" / "censys-tsa": SKILL_DIR,
            Path(home) / "bin" / "tsa": BIN_TSA,
        }

    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as home:
            proc = self.install("--dry-run", home=home)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("Dry run", proc.stdout)
            self.assertFalse((Path(home) / ".config").exists())

    def test_installs_exactly_the_expected_links(self):
        with tempfile.TemporaryDirectory() as home:
            proc = self.install(home=home)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            for link, target in self.expected_links(home).items():
                with self.subTest(link=link.name):
                    self.assertTrue(link.is_symlink(), f"{link} is not a symlink")
                    self.assertEqual(Path(os.readlink(link)), target)

    def test_is_idempotent(self):
        with tempfile.TemporaryDirectory() as home:
            self.install(home=home)
            proc = self.install(home=home)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            for link in self.expected_links(home):
                self.assertTrue(link.is_symlink())

    def test_refuses_to_clobber_a_stranger(self):
        """Someone else's censys-tsa.md is not ours to delete."""
        with tempfile.TemporaryDirectory() as home:
            agent_dir = Path(home) / ".config" / "opencode" / "agent"
            agent_dir.mkdir(parents=True)
            intruder = agent_dir / "censys-tsa.md"
            intruder.write_text("---\ndescription: mine\n---\nhands off\n")
            proc = self.install(home=home)
            self.assertEqual(intruder.read_text(), "---\ndescription: mine\n---\nhands off\n")
            self.assertIn("not created by this kit", proc.stdout)

    def test_uninstall_removes_only_its_own_links(self):
        with tempfile.TemporaryDirectory() as home:
            self.install(home=home)
            stranger = Path(home) / ".config" / "opencode" / "agent" / "someone-else.md"
            stranger.write_text("mine\n")
            proc = self.install("--uninstall", home=home)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            for link in self.expected_links(home):
                with self.subTest(link=link.name):
                    self.assertFalse(link.exists() or link.is_symlink())
            self.assertTrue(stranger.exists())

    def test_doctor_reports_missing_credentials_without_printing_them(self):
        with tempfile.TemporaryDirectory() as home:
            self.install(home=home)
            proc = self.install("--doctor", home=home)
            self.assertIn("CENSYS_PERSONAL_ACCESS_TOKEN", proc.stdout)
            self.assertNotEqual(proc.returncode, 0, "missing credentials must fail")

    def test_doctor_checks_the_plugin_can_resolve_its_import(self):
        """A plugin that cannot resolve @opencode-ai/plugin loads as nothing,
        silently, and then enforces nothing at all.

        The check must start from the plugin's *real* path. Resolution does, and
        a check that walked up from the symlink's own directory in the config
        tree would pass in precisely the case it exists to catch.
        """
        source = INSTALL_SH.read_text()
        self.assertIn("plugin_import_resolves", source)
        self.assertIn('real_path_of "$1"', source)

    def test_uninstall_leaves_another_installs_bridge_alone(self):
        """The bridge symlink lives in the kit, but belongs to one config dir.

        Uninstalling from a throwaway directory - which is what the tests above
        do - must not delete the live install's bridge and silently stop its
        plugin from loading.
        """
        source = INSTALL_SH.read_text()
        bridge_block = source.split('if [ -L "$KIT/node_modules" ]; then', 1)
        self.assertEqual(len(bridge_block), 2, "the bridge cleanup changed shape")
        self.assertIn('"$CONFIG_DIR/node_modules"', bridge_block[1][:400])

    def test_installer_tests_did_not_disturb_this_install(self):
        """Belt and braces for the bug above: if this kit has a bridge, the
        suite must not have removed it."""
        bridge = ROOT / "node_modules"
        if not bridge.is_symlink():
            self.skipTest("this kit has no dependency bridge")
        self.assertTrue(
            bridge.resolve(strict=False).name == "node_modules",
            "the bridge symlink was mangled",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
