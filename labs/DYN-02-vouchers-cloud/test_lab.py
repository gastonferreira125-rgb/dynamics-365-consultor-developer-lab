"""Tests del laboratorio ficticio: ejecutar con unittest desde Codespaces."""
import unittest
from lab import create_demo_db, get_voucher, detect_fixed_dimension_mismatches, voucher_balance


class VoucherLabTests(unittest.TestCase):
    def setUp(self):
        self.db = create_demo_db()

    def tearDown(self):
        self.db.close()

    def test_join_produces_two_account_entries(self):
        self.assertEqual(len(get_voucher(self.db, "USMF", "VCH-2026-001")), 2)

    def test_correct_fixed_cost_center_on_expense(self):
        rows = get_voucher(self.db, "USMF", "VCH-2026-001")
        expense = next(row for row in rows if row["MainAccount"] == "606300")
        self.assertEqual(expense["CostCenter"], "008")

    def test_company_scope_prevents_duplicate_voucher_mixup(self):
        self.assertEqual(get_voucher(self.db, "USMF", "VCH-2026-001")[0]["HeaderRecId"], 1001)
        self.assertEqual(get_voucher(self.db, "DEMF", "VCH-2026-001")[0]["HeaderRecId"], 2001)

    def test_debits_and_credits_balance(self):
        for company, voucher in [
            ("USMF", "VCH-2026-001"),
            ("USMF", "VCH-2026-002"),
            ("DEMF", "VCH-2026-001")
        ]:
            self.assertAlmostEqual(voucher_balance(self.db, company, voucher), 0.0)

    def test_one_intentional_fixed_dimension_discrepancy(self):
        mismatches = detect_fixed_dimension_mismatches(self.db)
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0]["SubledgerVoucher"], "VCH-2026-002")
        self.assertEqual(mismatches[0]["Actual"], "009")
        self.assertEqual(mismatches[0]["Expected"], "008")


if __name__ == "__main__":
    unittest.main()
