import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[3]
FUNCTION_ROOT = ROOT / "azure" / "functions" / "asset_ingest"
if str(FUNCTION_ROOT) not in sys.path:
    sys.path.insert(0, str(FUNCTION_ROOT))

from server.price_engine.providers.corelogic.corelogic_provider import CoreLogicProvider


class CoreLogicScaffoldTests(unittest.TestCase):
    def test_corelogic_provider_returns_deterministic_mock_response(self) -> None:
        response = CoreLogicProvider().get_property_intelligence(
            property_address="123 Main St",
            operator="tester",
        )

        self.assertEqual(response.provider, "corelogic")
        self.assertEqual(response.mode, "mock")
        self.assertEqual(
            response.property_intelligence,
            {
                "AVM": 245000,
                "FloodZone": "X",
                "ParcelId": "MO-JACKSON-000123456",
                "Beds": 3,
                "Baths": 2.0,
                "SqFt": 1680,
                "YearBuilt": 1998,
            },
        )


if __name__ == "__main__":
    unittest.main()
