from __future__ import annotations

import logging
from datetime import datetime, timezone

from server.price_engine.title_rate.provider_config import TitleRateProviderConfig
from server.price_engine.title_rate.provider_registry import build_title_rate_registry
from server.price_engine.exceptions import TitleRateProviderError


class TitleRateProviderManager:
    def __init__(self, config: TitleRateProviderConfig) -> None:
        self._config = config
        self._registry = build_title_rate_registry()

    def resolve_provider(self):
        if not self._config.provider_enabled:
            raise TitleRateProviderError(
                "TITLE_RATE_PROVIDER_NOT_CONFIGURED",
                "No approved title-rate provider is configured.",
                {"providerEnabled": False},
            )

        provider = self._registry.get(self._config.provider_type)
        if provider is None:
            raise TitleRateProviderError(
                "UNSUPPORTED_TITLE_RATE_PROVIDER",
                "Configured title-rate provider is not supported in this build.",
                {"provider": self._config.provider_type},
            )
        return provider

    def quote(self, request, *, operator: str | None = None):
        operator_name = operator or str(request.provider_context.get("operator") or "unknown")
        self._log_request(request, operator_name)

        if self._config.approval_required and not request.provider_context.get("approvalReceived"):
            raise TitleRateProviderError(
                "TITLE_RATE_PROVIDER_APPROVAL_REQUIRED",
                "Title-rate provider approval is required before this request can proceed.",
                {"provider": self._config.provider_type},
            )

        provider = self.resolve_provider()
        return provider.quote(request)

    def _log_request(self, request, operator: str) -> None:
        logging.info(
            "title_rate_provider_request provider_name=%s timestamp=%s request_parameters=%s operator=%s dry_run=%s",
            self._config.provider_type,
            datetime.now(timezone.utc).isoformat(),
            request.provider_context,
            operator,
            self._config.dry_run_mode,
        )
