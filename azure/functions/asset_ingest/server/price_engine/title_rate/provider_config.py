from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TitleRateProviderConfig:
    provider_enabled: bool
    provider_type: str
    dry_run_mode: bool
    approval_required: bool


def load_title_rate_provider_config() -> TitleRateProviderConfig:
    return TitleRateProviderConfig(
        provider_enabled=_bool_env("TITLE_RATE_PROVIDER_ENABLED", False),
        provider_type=os.getenv("TITLE_RATE_PROVIDER_TYPE", "stub").strip().lower() or "stub",
        dry_run_mode=_bool_env("TITLE_RATE_DRY_RUN_MODE", True),
        approval_required=_bool_env("TITLE_RATE_APPROVAL_REQUIRED", False),
    )


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}
