from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class CoreLogicConfig:
    provider_enabled: bool
    dry_run: bool
    paid_request_confirmation: bool
    request_limit: int
    request_logging: bool


def load_corelogic_config() -> CoreLogicConfig:
    return CoreLogicConfig(
        provider_enabled=_bool_env("CORELOGIC_PROVIDER_ENABLED", False),
        dry_run=_bool_env("CORELOGIC_DRY_RUN", True),
        paid_request_confirmation=_bool_env("CORELOGIC_PAID_REQUEST_CONFIRMATION", False),
        request_limit=_int_env("CORELOGIC_REQUEST_LIMIT", 25),
        request_logging=_bool_env("CORELOGIC_REQUEST_LOGGING", True),
    )


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default
