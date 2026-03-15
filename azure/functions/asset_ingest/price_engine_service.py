from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from server.price_engine.exceptions import PriceEngineError
from server.price_engine.deal_inputs import build_deal_inputs
from server.price_engine.deal_metrics import calculate_metrics


def calculate_price_engine(payload: dict[str, Any]) -> dict[str, Any]:
    deal_inputs = build_deal_inputs(payload)
    try:
        metrics = calculate_metrics(deal_inputs)
    except ValueError as exc:
        raise PriceEngineError("CALCULATION_FAILED", str(exc)) from exc

    return {
        # Preserve the existing public contract while sourcing values from the new deterministic core.
        "MAO": _round_currency(metrics.mao),
        "IRR": _round_percent(metrics.irr),
        "CoC": _round_percent(metrics.cash_on_cash_return),
        "CashToClose": _round_currency(metrics.cash_to_close),
        "Profit": _round_currency(metrics.profit),
        "RiskScore": _round_integer(Decimal(metrics.risk_score)),
    }


def _decimal_field(
    payload: dict[str, Any],
    field_name: str,
    *,
    required: bool = True,
    default: Decimal | None = None,
) -> Decimal:
    value = payload.get(field_name)
    if value is None:
        if required:
            raise PriceEngineError("VALIDATION_FAILED", f"{field_name} is required")
        return default if default is not None else Decimal("0")

    try:
        return Decimal(str(value)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    except Exception as exc:
        raise PriceEngineError("VALIDATION_FAILED", f"{field_name} must be numeric") from exc


def _round_currency(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _round_percent(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _round_integer(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
