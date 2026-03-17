from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from server.price_engine.exceptions import PriceEngineError


_ALLOWED_STRATEGIES = {"flip", "rental_hold", "brrrr"}
_DEFAULT_LTV = {
    "flip": Decimal("0.80"),
    "rental_hold": Decimal("0.75"),
    "brrrr": Decimal("0.70"),
}


@dataclass(frozen=True)
class DealInputs:
    strategy: str
    purchase_price: Decimal
    after_repair_value: Decimal
    rehab_cost: Decimal
    holding_costs: Decimal
    closing_costs: Decimal
    cash_available: Decimal
    rent_monthly: Decimal
    operating_expense_monthly: Decimal
    selling_costs: Decimal
    reserves: Decimal
    points: Decimal
    loan_amount: Decimal
    financed_ltv: Decimal
    holding_months: int
    interest_rate_annual: Decimal
    amortization_months: int
    target_profit_margin: Decimal


def build_deal_inputs(payload: dict[str, Any]) -> DealInputs:
    strategy = payload.get("strategy")
    if strategy not in _ALLOWED_STRATEGIES:
        raise PriceEngineError("UNSUPPORTED_STRATEGY_MODE", "strategy must be flip, rental_hold, or brrrr")

    purchase_price = _decimal_field(payload, "purchasePrice")
    after_repair_value = _decimal_field(payload, "afterRepairValue")
    rehab_cost = _decimal_field(payload, "rehabCost")
    holding_costs = _decimal_field(payload, "holdingCosts")
    closing_costs = _decimal_field(payload, "closingCosts")
    cash_available = _decimal_field(payload, "cashAvailable")
    rent_monthly = _decimal_field(payload, "rentMonthly", required=False, default=Decimal("0"))
    operating_expense_monthly = _decimal_field(payload, "operatingExpenseMonthly", required=False, default=Decimal("0"))
    selling_costs = _decimal_field(payload, "sellingCosts", required=False, default=closing_costs)
    reserves = _decimal_field(payload, "reserves", required=False, default=Decimal("0"))
    holding_months = _int_field(payload, "holdingMonths", default=12, minimum=1)
    financed_ltv = _decimal_field(payload, "financedLtv", required=False, default=_DEFAULT_LTV[strategy])
    if financed_ltv < Decimal("0") or financed_ltv > Decimal("1"):
        raise PriceEngineError("VALIDATION_FAILED", "financedLtv must be between 0 and 1")

    implied_loan_amount = purchase_price * financed_ltv
    loan_amount = _decimal_field(payload, "loanAmount", required=False, default=implied_loan_amount)
    points = _decimal_field(payload, "points", required=False, default=Decimal("0"))
    points_rate = _decimal_field(payload, "pointsRate", required=False, default=Decimal("0"))
    if points == Decimal("0") and points_rate > Decimal("0"):
        points = loan_amount * points_rate

    interest_rate_annual = _decimal_field(payload, "interestRateAnnual", required=False, default=Decimal("0.08"))
    amortization_months = _int_field(payload, "amortizationMonths", default=360, minimum=1)
    target_profit_margin = _decimal_field(payload, "targetProfitMargin", required=False, default=Decimal("0.10"))

    numeric_fields = (
        purchase_price,
        after_repair_value,
        rehab_cost,
        holding_costs,
        closing_costs,
        cash_available,
        rent_monthly,
        operating_expense_monthly,
        selling_costs,
        reserves,
        points,
        loan_amount,
        interest_rate_annual,
        target_profit_margin,
    )
    if min(numeric_fields) < Decimal("0"):
        raise PriceEngineError("VALIDATION_FAILED", "numeric inputs must be non-negative")

    if loan_amount > purchase_price:
        raise PriceEngineError("VALIDATION_FAILED", "loanAmount cannot exceed purchasePrice")

    return DealInputs(
        strategy=strategy,
        purchase_price=purchase_price,
        after_repair_value=after_repair_value,
        rehab_cost=rehab_cost,
        holding_costs=holding_costs,
        closing_costs=closing_costs,
        cash_available=cash_available,
        rent_monthly=rent_monthly,
        operating_expense_monthly=operating_expense_monthly,
        selling_costs=selling_costs,
        reserves=reserves,
        points=points,
        loan_amount=loan_amount,
        financed_ltv=financed_ltv,
        holding_months=holding_months,
        interest_rate_annual=interest_rate_annual,
        amortization_months=amortization_months,
        target_profit_margin=target_profit_margin,
    )


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
        return Decimal(str(value))
    except Exception as exc:
        raise PriceEngineError("VALIDATION_FAILED", f"{field_name} must be numeric") from exc


def _int_field(payload: dict[str, Any], field_name: str, *, default: int, minimum: int) -> int:
    value = payload.get(field_name)
    if value is None:
        return default

    try:
        parsed = int(value)
    except Exception as exc:
        raise PriceEngineError("VALIDATION_FAILED", f"{field_name} must be an integer") from exc

    if parsed < minimum:
        raise PriceEngineError("VALIDATION_FAILED", f"{field_name} must be at least {minimum}")
    return parsed
