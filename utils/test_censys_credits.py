#!/usr/bin/env python3
"""Tests for credit usage tracking (censys_credits + censys_tsa integration).

Run with::

    python -m unittest test_censys_credits -v
"""

from __future__ import annotations

import unittest
from datetime import date, timedelta
from unittest import mock

import censys_credits as cc
import censys_tsa


class FakeResponse:
    """Mimics an SDK response envelope's ``model_dump``."""

    def __init__(self, result):
        self._result = result

    def model_dump(self, **_kwargs):
        return {"result": {"result": self._result}}


def usage_report(consumed=100, transactions=2, **overrides):
    report = {
        "start_time": "2026-08-04T00:00:00Z",
        "end_time": "2026-08-04T23:59:59Z",
        "granularity": "daily",
        "total_consumed": consumed,
        "total_added": 0,
        "total_expired": 0,
        "transaction_count": transactions,
        "credits_consumed_by_source": {"ui": 0, "api": consumed},
        "periods": [
            {
                "start_date": "2026-08-04T00:00:00Z",
                "end_date": "2026-08-04T23:59:59Z",
                "credits_consumed": consumed,
                "credits_added": 0,
                "credits_expired": 0,
                "transaction_count": transactions,
            }
        ],
    }
    report.update(overrides)
    return report


class FakeAccountManagement:
    def __init__(self, balances, usages):
        self.balances = list(balances)
        self.usages = list(usages)
        self.usage_requests = []

    def get_organization_credits(self, organization_id):
        return FakeResponse({"uid": organization_id, "balance": self.balances.pop(0)})

    def get_organization_credit_usage(self, request):
        self.usage_requests.append(request)
        return FakeResponse(self.usages.pop(0))


class FakeSDK:
    def __init__(self, account_management):
        self.account_management = account_management

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def patch_sdk(account_management):
    return mock.patch.object(
        cc, "SDK", lambda **_kwargs: FakeSDK(account_management)
    )


class TestGetters(unittest.TestCase):
    def test_balance_unwraps_envelope(self):
        am = FakeAccountManagement([5000], [])
        with patch_sdk(am):
            result = cc.get_credit_balance(org_id="org-1", token="t")
        self.assertEqual(result["balance"], 5000)
        self.assertEqual(result["uid"], "org-1")

    def test_usage_defaults_to_today(self):
        am = FakeAccountManagement([], [usage_report()])
        with patch_sdk(am):
            result = cc.get_credit_usage(org_id="org-1", token="t")
        request = am.usage_requests[0]
        self.assertEqual(request["start_date"], cc.today_utc())
        self.assertEqual(request["end_date"], cc.today_utc())
        self.assertEqual(request["granularity"], "daily")
        self.assertIs(request["include_consumer_breakdown"], False)
        self.assertEqual(result["total_consumed"], 100)

    def test_usage_accepts_string_dates_and_flags(self):
        am = FakeAccountManagement([], [usage_report()])
        with patch_sdk(am):
            cc.get_credit_usage(
                start_date="2026-01-01",
                end_date="2026-02-01",
                granularity="monthly",
                include_consumer_breakdown=True,
                org_id="org-1",
                token="t",
            )
        request = am.usage_requests[0]
        self.assertEqual(request["start_date"], date(2026, 1, 1))
        self.assertEqual(request["end_date"], date(2026, 2, 1))
        self.assertEqual(request["granularity"], "monthly")
        self.assertIs(request["include_consumer_breakdown"], True)

    def test_usage_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            cc.get_credit_usage(granularity="hourly")
        with self.assertRaises(ValueError):
            cc.get_credit_usage(start_date="2024-12-31")
        with self.assertRaises(ValueError):
            cc.get_credit_usage(start_date="2026-02-01", end_date="2026-01-01")
        far = (cc.today_utc() - timedelta(days=400)).isoformat()
        with self.assertRaises(ValueError):
            cc.get_credit_usage(start_date=far)

    def test_transient_errors_are_retried(self):
        calls = {"n": 0}

        def flaky():
            calls["n"] += 1
            if calls["n"] < 3:
                raise ConnectionError("boom")
            return "ok"

        with mock.patch.object(cc.time, "sleep"):
            self.assertEqual(cc._call(flaky), "ok")
        self.assertEqual(calls["n"], 3)

    def test_persistent_error_raises_credits_error(self):
        with mock.patch.object(cc.time, "sleep"):
            with self.assertRaises(cc.CreditsError):
                cc._call(lambda: (_ for _ in ()).throw(ConnectionError("down")))


class TestCreditTracker(unittest.TestCase):
    def test_tracks_balance_and_report_deltas(self):
        am = FakeAccountManagement(
            balances=[5000, 4988],
            usages=[usage_report(100, 2), usage_report(112, 4)],
        )
        with patch_sdk(am):
            with cc.CreditTracker(org_id="org-1", token="t") as tracker:
                pass
        summary = tracker.summary()
        self.assertEqual(summary["consumed"], 12)
        self.assertEqual(summary["consumed_by_balance"], 12)
        self.assertEqual(summary["consumed_reported"], 12)
        self.assertEqual(summary["transactions"], 2)
        self.assertEqual(summary["balance_before"], 5000)
        self.assertEqual(summary["balance_after"], 4988)
        self.assertEqual(summary["errors"], [])

    def test_falls_back_to_report_when_balance_missing(self):
        am = FakeAccountManagement(
            balances=[None, None],
            usages=[usage_report(100), usage_report(150)],
        )
        with patch_sdk(am):
            tracker = cc.CreditTracker(org_id="org-1", token="t")
            tracker.start()
            summary = tracker.stop()
        self.assertIsNone(summary["consumed_by_balance"])
        self.assertEqual(summary["consumed"], 50)

    def test_snapshot_failure_is_captured_not_raised(self):
        def boom(**_kwargs):
            raise RuntimeError("network down")

        with mock.patch.object(cc, "SDK", boom), mock.patch.object(cc.time, "sleep"):
            tracker = cc.CreditTracker(org_id="org-1", token="t")
            tracker.start()
            summary = tracker.stop()
        self.assertIsNone(summary["consumed"])
        self.assertEqual(len(summary["errors"]), 2)


class TestFormatting(unittest.TestCase):
    def test_format_usage_includes_totals_and_periods(self):
        text = cc.format_usage(
            usage_report(1234, 7, credits_consumed_by_consumer={"a@b.com": 1234})
        )
        self.assertIn("1,234", text)
        self.assertIn("api=1,234", text)
        self.assertIn("a@b.com", text)
        self.assertIn("2026-08-04", text)

    def test_format_tracker_summary_handles_unknowns(self):
        text = cc.format_tracker_summary(
            {"consumed": None, "errors": ["before_snapshot: nope"]}
        )
        self.assertIn("unknown", text)
        self.assertIn("! before_snapshot", text)


class TestTSAIntegration(unittest.TestCase):
    def setUp(self):
        self.gateway = mock.Mock(calls_made=2)

    def _run(self, track_credits, am=None):
        counts = mock.Mock(
            side_effect=lambda q, *a, **k: {
                "query": q, "url": "u", "total_hits": 10, "errors": []
            }
        )
        ctx = patch_sdk(am) if am else mock.patch.object(cc, "SDK")
        with mock.patch.object(censys_tsa, "count_hits", counts), ctx:
            return censys_tsa.run_tsa(
                "host.services.port: 22",
                self.gateway,
                org_id="org-1",
                track_credits=track_credits,
            )

    def test_credits_attached_by_default(self):
        am = FakeAccountManagement(
            balances=[900, 898], usages=[usage_report(10, 1), usage_report(12, 2)]
        )
        result = self._run(True, am)
        self.assertEqual(result["credits"]["consumed"], 2)
        self.assertIn("Credits used", censys_tsa.format_report(result))

    def test_credits_can_be_disabled(self):
        result = self._run(False)
        self.assertNotIn("credits", result)
        self.assertNotIn("Credits used", censys_tsa.format_report(result))

    def test_credits_flag_defaults_true_and_toggles(self):
        self.assertTrue(censys_tsa.parse_args(["q"]).track_credits)
        self.assertFalse(censys_tsa.parse_args(["q", "--no-credits"]).track_credits)


if __name__ == "__main__":
    unittest.main()
