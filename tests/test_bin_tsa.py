#!/usr/bin/env python3
"""Unit tests for bin/tsa - the unattended TSA driver.

Pure functions only: no opencode, no Censys, no network. Fast.

Run::

    python -m unittest tests.test_bin_tsa -v
"""

from __future__ import annotations

import argparse
import subprocess
import unittest

from tests.helpers import ROOT, flat, load_bin_tsa

tsa = load_bin_tsa()


def args(**overrides) -> argparse.Namespace:
    """A Namespace matching bin/tsa's parsed args, with test overrides."""
    base = dict(
        target=None, cve=None, product=None, country="Canada", slug=None, note=None,
        model=None, timeout=3600, keep_going=False, print_prompt=False,
        allow_web=False, allow_endpoint_check=False, deep_dive=False,
        budget=None, version_breakdown=False, no_reports=False, print_spec=False,
    )
    base.update(overrides)
    return argparse.Namespace(**base)


class Slugify(unittest.TestCase):
    """Slugs must match the naming convention of the existing reports/.

    Dots are preserved so version numbers survive. Replacing them would fork
    the naming scheme and silently break diffs against previously written
    specs - the expected values below are real filenames from the source repo.
    """

    CASES = [
        ("LobeChat 1.123.1", "lobechat-1.123.1"),
        ("Jellyfin Media System 10.11.0", "jellyfin-media-system-10.11.0"),
        ("LobeHub 2.2.13", "lobehub-2.2.13"),
        ("Ivanti EPMM", "ivanti-epmm"),
        ("Cisco SD-WAN Manager", "cisco-sd-wan-manager"),
        ("SonicWall SMA 1000", "sonicwall-sma-1000"),
        ("CVE-2024-21762", "cve-2024-21762"),
        ("  Trailing dots...  ", "trailing-dots"),
        ("Multiple   spaces", "multiple-spaces"),
        ("!!!", "assessment"),
    ]

    def test_slugs(self):
        for source, expected in self.CASES:
            with self.subTest(source=source):
                self.assertEqual(tsa.slugify(source), expected)

    def test_slug_is_filesystem_safe(self):
        for source, _ in self.CASES:
            with self.subTest(source=source):
                slug = tsa.slugify(source)
                self.assertNotIn("/", slug)
                self.assertNotIn(" ", slug)
                self.assertFalse(slug.startswith("."), "would create a hidden file")


class VersionBreakdown(unittest.TestCase):
    """Off by default; on when version work is the point of the assessment.

    Gating the distribution *table* only - version scoping for a CVE stays
    mandatory regardless, because that is what makes the count correct.
    """

    def test_off_for_a_plain_product(self):
        for target in ["Ivanti EPMM", "Cisco SD-WAN", "Flowise", "Log4j 2"]:
            with self.subTest(target=target):
                on, why = tsa.wants_version_breakdown(args(target=target))
                self.assertFalse(on, f"{target!r} should not trigger a breakdown ({why})")

    def test_on_when_target_names_a_version(self):
        for target in ["LobeChat 1.123.1", "CUPS 1.4", "Jellyfin 10.11.0"]:
            with self.subTest(target=target):
                on, why = tsa.wants_version_breakdown(args(target=target))
                self.assertTrue(on)
                self.assertIn("version", why)

    def test_on_for_a_cve_flag(self):
        on, why = tsa.wants_version_breakdown(args(cve="CVE-2024-21762"))
        self.assertTrue(on)
        self.assertIn("CVE", why)

    def test_on_for_a_cve_as_positional_target(self):
        """A CVE id has no dotted number, so the version regex alone misses it."""
        on, why = tsa.wants_version_breakdown(args(target="CVE-2024-21762"))
        self.assertTrue(on, "a CVE named in the target must still trigger")
        self.assertIn("CVE", why)

    def test_on_when_explicitly_requested(self):
        on, why = tsa.wants_version_breakdown(args(target="Flowise", version_breakdown=True))
        self.assertTrue(on)
        self.assertIn("--version-breakdown", why)

    def test_on_when_product_scope_names_a_version(self):
        on, _ = tsa.wants_version_breakdown(
            args(cve=None, target="thing", product="Fortinet FortiOS 7.2")
        )
        self.assertTrue(on)


class Capabilities(unittest.TestCase):
    """The serialised capability string is the contract with the plugin."""

    def parse(self, capability_string: str) -> dict:
        return dict(pair.split("=", 1) for pair in capability_string.split())

    def test_defaults_are_fail_closed(self):
        caps = self.parse(tsa.build_capabilities(args(target="Ivanti EPMM")))
        self.assertEqual(caps["webfetch"], "off")
        self.assertEqual(caps["websearch"], "off")
        self.assertEqual(caps["endpoint"], "off")
        self.assertEqual(caps["deepdive"], "never")
        self.assertEqual(caps["versionbreakdown"], "off")
        self.assertEqual(caps["budget"], "0")

    def test_reports_default_on(self):
        """reports/<slug>.spec.json is bin/tsa's output contract."""
        caps = self.parse(tsa.build_capabilities(args(target="x")))
        self.assertEqual(caps["reports"], "on")

    def test_allow_web_sets_both_network_capabilities(self):
        caps = self.parse(tsa.build_capabilities(args(target="x", allow_web=True)))
        self.assertEqual(caps["webfetch"], "on")
        self.assertEqual(caps["websearch"], "on")

    def test_print_spec_is_independent_of_writing_files(self):
        """All four combinations must be expressible."""
        combos = {
            (False, False): ("on", "off"),   # default: files, no block
            (True, False): ("on", "on"),     # both: files and block
            (False, True): ("off", "on"),    # no file, so the block is forced on
            (True, True): ("off", "on"),
        }
        for (print_spec, no_reports), (reports, printspec) in combos.items():
            with self.subTest(print_spec=print_spec, no_reports=no_reports):
                caps = self.parse(tsa.build_capabilities(
                    args(target="x", print_spec=print_spec, no_reports=no_reports)
                ))
                self.assertEqual(caps["reports"], reports)
                self.assertEqual(caps["printspec"], printspec)

    def test_no_reports_forces_the_spec_block(self):
        """Without a file, the block is the only way bin/tsa can recover the spec."""
        caps = self.parse(tsa.build_capabilities(args(target="x", no_reports=True)))
        self.assertEqual(caps["printspec"], "on")

    def test_each_flag_maps_to_its_capability(self):
        caps = self.parse(tsa.build_capabilities(args(
            target="x", allow_endpoint_check=True, deep_dive=True,
            budget=50, no_reports=True,
        )))
        self.assertEqual(caps["endpoint"], "on")
        self.assertEqual(caps["deepdive"], "always")
        self.assertEqual(caps["budget"], "50")
        self.assertEqual(caps["reports"], "off")

    def test_keys_match_what_the_plugin_parses(self):
        """Guards against a rename on one side of the contract only."""
        from tests.helpers import PLUGIN_TS

        emitted = set(self.parse(tsa.build_capabilities(args(target="x"))))
        plugin_source = PLUGIN_TS.read_text()
        for key in emitted:
            with self.subTest(key=key):
                self.assertIn(
                    f'case "{key}"', plugin_source,
                    f"bin/tsa emits {key!r} but the plugin has no case for it",
                )


class Prompt(unittest.TestCase):
    def test_prompt_carries_the_capability_line(self):
        caps = tsa.build_capabilities(args(target="Ivanti EPMM"))
        prompt = tsa.build_prompt(args(target="Ivanti EPMM"), "ivanti-epmm", caps)
        self.assertIn(f"CAPABILITIES: {caps}", prompt)

    def test_cve_is_not_duplicated(self):
        a = args(cve="CVE-2024-21762")
        prompt = tsa.build_prompt(a, "cve-2024-21762", tsa.build_capabilities(a))
        self.assertNotIn("CVE CVE-", prompt)

    def test_cve_scoped_to_product_names_both(self):
        a = args(cve="CVE-2024-21762", product="Fortinet FortiOS")
        prompt = tsa.build_prompt(a, "fortinet-fortios", tsa.build_capabilities(a))
        self.assertIn("CVE-2024-21762", prompt)
        self.assertIn("Fortinet FortiOS", prompt)

    def test_reports_on_demands_the_spec_file(self):
        a = args(target="x")
        prompt = tsa.build_prompt(a, "x", tsa.build_capabilities(a))
        self.assertIn("@censys-report", prompt)
        self.assertIn("reports/x.spec.json", prompt)

    def test_no_reports_forbids_the_report_agent(self):
        a = args(target="x", no_reports=True)
        prompt = tsa.build_prompt(a, "x", tsa.build_capabilities(a))
        self.assertIn("Do NOT invoke @censys-report", prompt)
        self.assertIn("```json", prompt)

    def test_no_reports_still_demands_the_summary(self):
        """The JSON block is for the wrapper; the summary is for the human.

        writeReports controls whether a file is written, never whether the
        compact summary is printed.
        """
        a = args(target="x", no_reports=True)
        prompt = tsa.build_prompt(a, "x", tsa.build_capabilities(a))
        self.assertIn("compact summary", prompt)
        self.assertIn("in addition to the summary, never instead of it", flat(prompt))

    def test_a_plain_run_does_not_ask_for_a_json_block(self):
        a = args(target="x")
        prompt = tsa.build_prompt(a, "x", tsa.build_capabilities(a))
        self.assertNotIn("```json", prompt)

    def test_print_spec_asks_for_the_block_alongside_the_files(self):
        """The 'both' option: durable artifact AND the spec inline."""
        a = args(target="x", print_spec=True)
        prompt = tsa.build_prompt(a, "x", tsa.build_capabilities(a))
        self.assertIn("@censys-report", prompt, "files must still be written")
        self.assertIn("```json", prompt, "the spec block must also be requested")
        self.assertIn("in addition to the summary", flat(prompt))


class ExtractSpec(unittest.TestCase):
    """--no-reports recovers the spec from the agent's message, not from disk."""

    def test_plain_fenced_block(self):
        text = 'blah\n```json\n{"product":"X","baseline":{"query":"q"}}\n```\nmore'
        self.assertEqual(tsa.extract_spec(text)["product"], "X")

    def test_escaped_event_stream_form(self):
        """`opencode run --format json` escapes newlines inside JSON strings."""
        text = r'{"text":"```json\n{\"product\":\"Y\",\"baseline\":{}}\n```"}'
        self.assertEqual(tsa.extract_spec(text)["product"], "Y")

    def test_skips_a_block_that_is_not_a_spec(self):
        text = '```json\n{"not":"aspec"}\n```\n```json\n{"product":"Z","baseline":{}}\n```'
        self.assertEqual(tsa.extract_spec(text)["product"], "Z")

    def test_prefers_a_spec_over_a_later_decoy(self):
        text = '```json\n{"product":"A","baseline":{}}\n```\n```json\n{"decoy":true}\n```'
        self.assertEqual(tsa.extract_spec(text)["product"], "A")

    def test_returns_none_when_absent(self):
        self.assertIsNone(tsa.extract_spec("no json here"))

    def test_returns_none_on_malformed_json(self):
        self.assertIsNone(tsa.extract_spec('```json\n{"baseline": oops}\n```'))


class CommandLine(unittest.TestCase):
    """End-to-end CLI smoke tests. --print-prompt must stay side-effect free:
    no agent run, no model tokens, no Censys."""

    def run_tsa(self, *argv) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bin/tsa", *argv], cwd=ROOT, capture_output=True, text=True, timeout=60
        )

    def test_help_exits_clean(self):
        self.assertEqual(self.run_tsa("--help").returncode, 0)

    def test_print_prompt_for_a_versioned_target(self):
        proc = self.run_tsa("--print-prompt", "LobeChat 1.123.1")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("versionbreakdown=on", proc.stdout)
        self.assertIn("lobechat-1.123.1", proc.stdout)

    def test_print_prompt_for_a_plain_target(self):
        proc = self.run_tsa("--print-prompt", "Ivanti EPMM")
        self.assertIn("versionbreakdown=off", proc.stdout)
        self.assertIn("ivanti-epmm", proc.stdout)

    def test_requires_a_target(self):
        self.assertNotEqual(self.run_tsa("--print-prompt").returncode, 0)

    def test_product_without_cve_is_rejected(self):
        proc = self.run_tsa("--print-prompt", "--product", "X", "thing")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("--product", proc.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
