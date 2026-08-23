import math
import unittest

from prototypes.kdence_mvp import (
    ActualsRecord,
    Property,
    buy_box_screen,
    record_variance,
    run_stress_tests,
    shade_line,
    underwrite,
)


class KdenceMvpTest(unittest.TestCase):
    def make_property(self, **overrides):
        values = {
            "deal_id": "DEAL-TEST",
            "address": "123 Test St",
            "neighborhood": "Morris Park",
            "unit_count": 3,
            "purchase_price": 750_000,
            "gross_scheduled_rent_annual": 96_000,
            "rent_source": "verified",
            "legal_unit_count_verified": True,
        }
        values.update(overrides)
        return Property(**values)

    def test_buy_box_passes_primary_three_family(self):
        prop = self.make_property(neighborhood="Pelham Bay", unit_count=3)

        self.assertTrue(buy_box_screen(prop))
        self.assertIn("primary target area", prop.pipeline_log[-1])

    def test_buy_box_fails_watchlist_area(self):
        prop = self.make_property(neighborhood="Riverdale")

        self.assertFalse(buy_box_screen(prop))
        self.assertIn("watchlist-only", prop.pipeline_log[-1])

    def test_underwrite_calculates_dscr_and_cash_flow(self):
        prop = self.make_property(
            purchase_price=750_000,
            gross_scheduled_rent_annual=96_000,
            vacancy_pct=0.05,
            opex_pct=0.10,
            down_payment_pct=0.25,
            interest_rate=0.07,
            loan_term_years=30,
        )

        result = underwrite(prop)

        self.assertEqual(result.effective_gross_income, 91_200)
        self.assertEqual(result.operating_expenses, 9_120)
        self.assertEqual(result.noi, 82_080)
        self.assertTrue(math.isclose(result.annual_debt_service, 44_907.9184, rel_tol=1e-6))
        self.assertTrue(math.isclose(result.dscr, 1.827740, rel_tol=1e-6))
        self.assertEqual(result.cash_required_to_close, 187_500)

    def test_stress_tests_reduce_downside_dscr(self):
        prop = self.make_property()

        results = run_stress_tests(prop)

        self.assertEqual(set(results), {"base", "stress", "downside", "severe"})
        self.assertLess(results["downside"].dscr, results["base"].dscr)
        self.assertLess(results["severe"].dscr, results["downside"].dscr)

    def test_shade_line_holds_listing_rent_after_financial_gates_pass(self):
        prop = self.make_property(rent_source="listing")
        uw = underwrite(prop)
        stress_results = run_stress_tests(prop)

        flag, reason = shade_line(prop, uw, stress_results)

        self.assertEqual(flag, "HOLD")
        self.assertIn("unverified listing claim", reason)

    def test_shade_line_rejects_low_dscr(self):
        prop = self.make_property(purchase_price=950_000, gross_scheduled_rent_annual=60_000)
        uw = underwrite(prop)
        stress_results = run_stress_tests(prop)

        flag, reason = shade_line(prop, uw, stress_results)

        self.assertEqual(flag, "REJECT")
        self.assertIn("below the policy minimum", reason)

    def test_record_variance_preserves_underwritten_and_actual_noi(self):
        prop = self.make_property()
        uw = underwrite(prop)
        actuals = ActualsRecord(deal_id=prop.deal_id, period="2026-08", actual_noi=75_000)

        variance = record_variance(uw, actuals)

        self.assertEqual(variance["deal_id"], prop.deal_id)
        self.assertEqual(variance["period"], "2026-08")
        self.assertEqual(variance["underwritten_noi"], uw.noi)
        self.assertEqual(variance["actual_noi"], 75_000)
        self.assertTrue(math.isclose(variance["variance_pct"], (75_000 - uw.noi) / uw.noi))


if __name__ == "__main__":
    unittest.main()
