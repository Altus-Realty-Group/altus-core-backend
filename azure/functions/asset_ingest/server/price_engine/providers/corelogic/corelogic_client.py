from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from server.price_engine.providers.corelogic.corelogic_config import CoreLogicConfig
from server.price_engine.providers.corelogic.corelogic_models import mock_property_intelligence


@dataclass(frozen=True)
class CoreLogicRequest:
    property_address: str
    operator: str


class CoreLogicClient:
    def __init__(self, config: CoreLogicConfig) -> None:
        self._config = config

    def build_request(self, *, property_address: str, operator: str) -> CoreLogicRequest:
        return CoreLogicRequest(property_address=property_address, operator=operator)

    def retry_policy(self) -> dict[str, int]:
        return {"max_attempts": 3, "backoff_seconds": 2}

    def fetch_property_intelligence(self, request: CoreLogicRequest) -> dict[str, Any]:
        self._log_request(request)
        if not self._config.provider_enabled or self._config.dry_run or not self._config.paid_request_confirmation:
            return {
                "mode": "mock",
                "request": {"propertyAddress": request.property_address, "operator": request.operator},
                "data": mock_property_intelligence().to_dict(),
            }

        raise RuntimeError("Real CoreLogic calls are disabled in this scaffold build")

    def _log_request(self, request: CoreLogicRequest) -> None:
        if self._config.request_logging:
            logging.info(
                "corelogic_request property_address=%s operator=%s dry_run=%s provider_enabled=%s paid_confirmation=%s",
                request.property_address,
                request.operator,
                self._config.dry_run,
                self._config.provider_enabled,
                self._config.paid_request_confirmation,
            )
