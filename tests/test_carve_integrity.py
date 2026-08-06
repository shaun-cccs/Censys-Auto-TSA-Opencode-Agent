#!/usr/bin/env python3
"""The references/ carve must stay a faithful copy of SKILL.md.

references/ is carved verbatim from the canonical censys-auto-tsa skill. The
whole design depends on that: agent prompts are thin routers over the carve, so
if a line goes missing the workflow silently loses a rule with nothing to
signal it.

Every non-blank source line must appear verbatim somewhere in AGENTS.md or
references/, unless it is on one of two explicit lists:

  DROPPED         - deliberately not carried over, with a reason
  KNOWN_REWRITES  - intentionally edited, by source line number

Adding a line to either list is a decision. Leaving a line unaccounted for is a
bug. If this test fails after you edit references/, the fix is almost always to
revert the reference edit and put the change in an agent prompt instead.

Run::

    python -m unittest tests.test_carve_integrity -v
"""

from __future__ import annotations

import unittest

from tests.helpers import AGENT_DIR, REFERENCES, ROOT, SKILL_MD

# Source lines intentionally not carried into this project.
DROPPED = {
    **{n: "YAML frontmatter - this is a project, not a skill" for n in range(1, 5)},
    **{n: "skill-sync maintenance block - N/A here" for n in range(87, 97)},
}

# Source lines intentionally edited. Mostly the workspace path rewrite and the
# ask_user -> question tool rename.
KNOWN_REWRITES = {
    6,     # "# Censys Auto TSA" title -> project title in AGENTS.md
    64,    # "## Workspace" heading rewritten
    66, 67,  # repo path prose rewritten for this project
    77,    # reports/ table row rewritten
    85,    # "run from the repository root" rewritten
    101,   # cd <old repo>            -> cd <this project>
    118,   # bare "## Workflow" H2, no parent document here
    131, 182, 439, 485, 637, 945, 960, 1028, 1137, 1231, 1341, 1370, 1402,
    1429, 1455,
    1006,  # ask_user -> question
}


class CarveIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SKILL_MD.exists():
            raise unittest.SkipTest(
                f"canonical skill not present at {SKILL_MD}; carve tests skipped"
            )
        cls.source = SKILL_MD.read_text().splitlines()
        cls.haystack = set()
        for path in [ROOT / "AGENTS.md", *sorted(REFERENCES.glob("*.md"))]:
            cls.haystack.update(path.read_text().splitlines())

    def test_every_source_line_is_accounted_for(self):
        unaccounted = []
        for lineno, line in enumerate(self.source, 1):
            if not line.strip() or lineno in DROPPED:
                continue
            if line in self.haystack or lineno in KNOWN_REWRITES:
                continue
            unaccounted.append((lineno, line))

        self.assertEqual(
            unaccounted,
            [],
            "SKILL.md lines missing from the carve with no recorded reason.\n"
            "Either restore them to references/, or add them to DROPPED or "
            "KNOWN_REWRITES with a justification:\n"
            + "\n".join(f"  {n:5}| {l}" for n, l in unaccounted[:20]),
        )

    def test_rewrite_list_has_no_dead_entries(self):
        """A rewrite entry that now matches verbatim is stale bookkeeping."""
        stale = [
            n
            for n in sorted(KNOWN_REWRITES)
            if n <= len(self.source) and self.source[n - 1] in self.haystack
        ]
        self.assertEqual(
            stale,
            [],
            f"KNOWN_REWRITES lines that now match verbatim and should be removed: {stale}",
        )

    def test_no_stale_workspace_paths(self):
        """The carve must not point at the repo it was copied from."""
        offenders = []
        for path in sorted(REFERENCES.glob("*.md")):
            for i, line in enumerate(path.read_text().splitlines(), 1):
                if "Censys Auto TSA" in line and not line.lstrip().startswith(
                    ("the canonical skill", "Provenance:")
                ):
                    offenders.append(f"{path.name}:{i}: {line.strip()}")
        self.assertEqual(
            offenders,
            [],
            "references/ still points at the source repo outside a provenance "
            "note:\n" + "\n".join(offenders),
        )

    def test_ask_user_tool_is_fully_renamed(self):
        """opencode's tool is `question`; `ask_user` does not exist here."""
        offenders = [
            f"{p.name}:{i}"
            for p in sorted(REFERENCES.glob("*.md"))
            for i, line in enumerate(p.read_text().splitlines(), 1)
            if "ask_user" in line
        ]
        self.assertEqual(offenders, [], f"stale ask_user references: {offenders}")

    def test_references_are_not_empty(self):
        for path in sorted(REFERENCES.glob("*.md")):
            with self.subTest(reference=path.name):
                self.assertGreater(
                    len(path.read_text().splitlines()), 20,
                    f"{path.name} looks truncated",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
