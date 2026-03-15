from __future__ import annotations

from typing import Any


def build_title_rate_registry() -> dict[str, Any]:
    from title_rate_provider import MockTitleRateProvider, StubTitleRateProvider

    return {
        "stub": StubTitleRateProvider(),
        "corelogic_title": MockTitleRateProvider(
            provider_key="corelogic_title",
            warning="Mock CoreLogic title provider only. No vendor logic or paid request is active.",
        ),
        "title_window_calculator": MockTitleRateProvider(
            provider_key="title_window_calculator",
            warning="Mock title window calculator only. No browser automation or scraping is active.",
        ),
    }
