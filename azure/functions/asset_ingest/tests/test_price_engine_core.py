import json
import pathlib
import sys
import unittest
from decimal import Decimal

ROOT = pathlib.Path(__file__).resolve().parents[4]
FUNCTION_ROOT = ROOT / "azure" / "functions" / "asset_ingest"
if str(FUNCTION_ROOT) not in sys.path:
    sys.path.insert(0, str(FUNCTION_ROOT))

from price_engine_service import calculate_price_engine
from server.price_engine.deal_inputs import build_deal_inputs
from server.price_engine.deal_metrics import calculate_metrics


class PriceEngineCoreTests(unittest.TestCase):
    def test_core_metrics_match_success_fixture(self) -> None:
        payload = json.loads(
            (ROOT / "docs" / "contracts" / "fixtures" / "price_engine_calculate" / "success_request.json").read_text(
                encoding="utf-8"
            )
        )

        metrics = calculate_price_engine(payload)

        self.assertEqual(
            metrics,
            {
                "MAO": 117000.0,
                "IRR": 140.36,
                "CoC": 31.48,
                "CashToClose": 61000.0,
                "Profit": 55000.0,
                "RiskScore": 54,
            },
        )

    def test_internal_core_exposes_cash_on_cash_return_name(self) -> None:
        payload = {
            "strategy": "rental_hold",
            "purchasePrice": 180000,
            "afterRepairValue": 240000,
            "rehabCost": 20000,
            "holdingCosts": 6000,
            "closingCosts": 5000,
            "cashAvailable": 80000,
            "rentMonthly": 2400,
            "operatingExpenseMonthly": 950,
            "loanAmount": 135000,
            "reserves": 5000,
            "points": 3000,
            "holdingMonths": 10,
        }

        inputs = build_deal_inputs(payload)
        metrics = calculate_metrics(inputs)

        self.assertEqual(metrics.mao, Decimal("143000.00"))
        self.assertEqual(metrics.cash_to_close, Decimal("78000.00"))
        self.assertEqual(metrics.cash_on_cash_return, Decimal("22.31"))
        self.assertEqual(metrics.profit, Decimal("29000.00"))
        self.assertIsInstance(metrics.risk_score, int)


if __name__ == "__main__":
    unittest.main()
