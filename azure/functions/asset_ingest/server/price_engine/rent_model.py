from __future__ import annotations

from decimal import Decimal

from server.price_engine.deal_inputs import DealInputs


def monthly_cash_flow(inputs: DealInputs) -> Decimal:
    return inputs.rent_monthly - inputs.operating_expense_monthly


def annual_cash_flow(inputs: DealInputs) -> Decimal:
    return monthly_cash_flow(inputs) * Decimal("12")
