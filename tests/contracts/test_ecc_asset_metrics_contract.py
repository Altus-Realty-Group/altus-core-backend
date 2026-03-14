from __future__ import annotations

import json
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FUNCTION_ROOT = ROOT / 'azure' / 'functions' / 'asset_ingest'
FIXTURE_ROOT = ROOT / 'docs' / 'contracts' / 'fixtures' / 'ecc_asset_metrics'

if str(FUNCTION_ROOT) not in sys.path:
    sys.path.insert(0, str(FUNCTION_ROOT))


class FakeHttpResponse:
    def __init__(self, body, status_code=200, headers=None, mimetype=None):
        self._body = body if isinstance(body, bytes) else str(body).encode('utf-8')
        self.status_code = status_code
        self.headers = headers or {}
        self.mimetype = mimetype

    def get_body(self) -> bytes:
        return self._body


fake_func_module = types.SimpleNamespace(
    HttpResponse=FakeHttpResponse,
    HttpRequest=object,
)
fake_azure_module = types.SimpleNamespace(functions=fake_func_module)
sys.modules.setdefault('azure', fake_azure_module)
sys.modules.setdefault('azure.functions', fake_func_module)

import ecc_asset_metrics_handler  # noqa: E402


class FakeRequest:
    def __init__(self, params: dict[str, str] | None = None):
        self.params = params or {}


def load_fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURE_ROOT / name).read_text(encoding='utf-8'))


class EccAssetMetricsContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_build_asset_metrics = ecc_asset_metrics_handler.build_asset_metrics

    def tearDown(self) -> None:
        ecc_asset_metrics_handler.build_asset_metrics = self.original_build_asset_metrics

    def test_success_contract_matches_fixture(self) -> None:
        response = ecc_asset_metrics_handler.handle_ecc_asset_metrics(
            FakeRequest({'assetId': 'asset-001', 'windowDays': '30'}),
            lambda: {'x-altus-build-sha': 'test-sha'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['x-altus-build-sha'], 'test-sha')
        self.assertEqual(response.headers['x-ecc-handler'], 'ecc-asset-metrics')
        self.assertEqual(response.headers['x-ecc-domain-signature'], 'ecc.asset.metrics.v1')
        self.assertEqual(
            json.loads(response.get_body().decode('utf-8')),
            load_fixture('success_response.json'),
        )

    def test_required_fields_and_deterministic_values(self) -> None:
        payload = json.loads(
            ecc_asset_metrics_handler.handle_ecc_asset_metrics(
                FakeRequest({'assetId': 'asset-001', 'windowDays': '30'}),
                lambda: {'x-altus-build-sha': 'test-sha'},
            ).get_body().decode('utf-8')
        )

        data = payload['data']
        self.assertEqual(data['assetId'], 'asset-001')
        self.assertEqual(data['windowDays'], 30)
        self.assertEqual(data['occupancyRate'], 0.22)
        self.assertEqual(data['maintenanceCostRatio'], 0.19)
        self.assertEqual(data['collectionsRate'], 0.94)
        self.assertEqual(data['delinquentUnits'], 4)
        self.assertEqual(data['openWorkOrders'], 6)
        self.assertEqual(data['netOperatingIncome'], 24000.0)
        self.assertEqual(data['currency'], 'USD')
        self.assertIsNone(data['lastUpdatedAt'])

    def test_validation_failure_missing_asset_id_matches_fixture(self) -> None:
        response = ecc_asset_metrics_handler.handle_ecc_asset_metrics(
            FakeRequest({}),
            lambda: {'x-altus-build-sha': 'test-sha'},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['x-ecc-handler'], 'ecc-asset-metrics')
        self.assertEqual(response.headers['x-ecc-domain-signature'], 'ecc.asset.metrics.v1')
        self.assertEqual(
            json.loads(response.get_body().decode('utf-8')),
            load_fixture('error_missing_asset_id_response.json'),
        )

    def test_validation_failure_invalid_window_days_matches_fixture(self) -> None:
        response = ecc_asset_metrics_handler.handle_ecc_asset_metrics(
            FakeRequest({'assetId': 'asset-001', 'windowDays': '366'}),
            lambda: {'x-altus-build-sha': 'test-sha'},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.get_body().decode('utf-8')),
            load_fixture('error_invalid_window_days_response.json'),
        )

    def test_internal_error_contract_matches_fixture(self) -> None:
        def broken_build_asset_metrics(asset_id: str, window_days: int) -> dict[str, object]:
            raise RuntimeError('boom')

        ecc_asset_metrics_handler.build_asset_metrics = broken_build_asset_metrics

        response = ecc_asset_metrics_handler.handle_ecc_asset_metrics(
            FakeRequest({'assetId': 'asset-001'}),
            lambda: {'x-altus-build-sha': 'test-sha'},
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.headers['x-ecc-handler'], 'ecc-asset-metrics')
        self.assertEqual(response.headers['x-ecc-domain-signature'], 'ecc.asset.metrics.v1')
        self.assertEqual(
            json.loads(response.get_body().decode('utf-8')),
            load_fixture('error_internal_response.json'),
        )


if __name__ == '__main__':
    unittest.main()
