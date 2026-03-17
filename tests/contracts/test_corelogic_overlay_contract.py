from __future__ import annotations

import json
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FUNCTION_ROOT = ROOT / "azure" / "functions" / "asset_ingest"
FIXTURE_ROOT = ROOT / "docs" / "contracts" / "fixtures" / "corelogic_overlay"

if str(FUNCTION_ROOT) not in sys.path:
    sys.path.insert(0, str(FUNCTION_ROOT))


class FakeHttpResponse:
    def __init__(self, body, status_code=200, headers=None, mimetype=None):
        self._body = body if isinstance(body, bytes) else str(body).encode("utf-8")
        self.status_code = status_code
        self.headers = headers or {}
        self.mimetype = mimetype

    def get_body(self) -> bytes:
        return self._body


fake_func_module = types.SimpleNamespace(
    HttpResponse=FakeHttpResponse,
    HttpRequest=object,
)
sys.modules.setdefault("azure.functions", fake_func_module)

from corelogic_overlay_handler import handle_corelogic_overlay  # noqa: E402


def load_fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


class FakeRequest:
    def __init__(self, *, params=None, headers=None):
        self.params = params or {}
        self.headers = headers or {}


class CoreLogicOverlayContractTests(unittest.TestCase):
    def test_success_contract_matches_fixture(self) -> None:
        response = handle_corelogic_overlay(
            FakeRequest(
                params={"address": "1518 Summit Ridge Dr, Kansas City, MO"},
                headers={"x-altus-operator": "contract-test"},
            ),
            lambda: {"x-altus-build-sha": "test-sha"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-altus-build-sha"], "test-sha")
        payload = json.loads(response.get_body().decode("utf-8"))
        self.assertEqual(payload, load_fixture("mock_response.json"))
        self.assertCountEqual(payload.keys(), ["subject", "overlays", "propertyIntelligence", "meta"])
        self.assertCountEqual(payload["subject"].keys(), ["address", "lat", "lng"])
        self.assertIn("corelogicLayerStatus", payload["overlays"])
        self.assertCountEqual(
            payload["propertyIntelligence"].keys(),
            ["avm", "beds", "baths", "sqFt", "yearBuilt"],
        )
        self.assertCountEqual(
            payload["meta"].keys(),
            ["provider", "mock", "approvalRequired"],
        )


if __name__ == "__main__":
    unittest.main()
