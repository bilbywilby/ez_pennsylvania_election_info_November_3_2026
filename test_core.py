import copy
import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build_site, finance_check, validate  # noqa: E402
from electoral_calendar import deadline, election_day  # noqa: E402


class Calendar(unittest.TestCase):
    def test_election_days(self):
        self.assertEqual(election_day(2026), date(2026, 11, 3))
        self.assertEqual(election_day(2024), date(2024, 11, 5))
        self.assertEqual(election_day(2028), date(2028, 11, 7))
        for y in range(2000, 2100):
            self.assertEqual(election_day(y).weekday(), 1)  # always a Tuesday

    def test_2026_deadlines(self):
        e = election_day(2026)
        self.assertEqual(deadline("r", e, 15, "23:59").day, date(2026, 10, 19))
        self.assertEqual(deadline("m", e, 7, "17:00").iso, "2026-10-27T17:00:00-04:00")
        # DST ends Nov 1, 2026, so Election Day is EST (UTC-5), not EDT.
        self.assertEqual(deadline("c", e, 0, "20:00").iso, "2026-11-03T20:00:00-05:00")


class Finance(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "data" / "finance_snapshot.json").read_text())

    def test_identities_hold(self):
        self.assertEqual(finance_check.run(), [])

    def test_corrupted_figure_is_caught(self):
        bad = copy.deepcopy(self.data)
        bad["governor"]["shapiro"]["disbursed_latest"]["value"] = 21800000
        p = ROOT / "tests" / "_bad.json"
        p.write_text(json.dumps(bad))
        try:
            self.assertTrue(finance_check.run(p))
        finally:
            p.unlink()

    def test_ratios(self):
        r = finance_check.ratios(self.data["governor"])
        self.assertAlmostEqual(r["raised_2026"], 8.34, places=2)
        self.assertAlmostEqual(r["cash_sep"], 15.23, places=2)


class Site(unittest.TestCase):
    def setUp(self):
        self.el = build_site.load("election.json")
        self.res = build_site.load("resources.json")

    def test_deterministic_and_fresh(self):
        a = build_site.render(self.el, self.res)
        self.assertEqual(a, build_site.render(self.el, self.res))
        self.assertEqual(a, build_site.OUT.read_text(encoding="utf-8"))

    def test_publication_gate(self):
        el = copy.deepcopy(self.el)
        el["deadlines"][0]["status"] = "unverified"
        self.assertNotIn(el["deadlines"][0]["label"], build_site.render(el, self.res))

    def test_validator_rejects_wrong_date(self):
        el = copy.deepcopy(self.el)
        el["deadlines"][0]["date"] = "2026-10-20"
        self.assertTrue(any("rule gives" in m for m in validate.check_election(el)))

    def test_validator_requires_two_sources(self):
        el = copy.deepcopy(self.el)
        el["deadlines"][1]["sources"] = el["deadlines"][1]["sources"][:1]
        self.assertTrue(any(">= 2" in m for m in validate.check_election(el)))

    def test_html_ok(self):
        self.assertEqual(validate.check_html(build_site.OUT), [])


if __name__ == "__main__":
    unittest.main()
