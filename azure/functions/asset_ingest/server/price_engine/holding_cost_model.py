from __future__ import annotations

from decimal import Decimal

from server.price_engine.deal_inputs import DealInputs


def down_payment(inputs: DealInputs) -> Decimal:
    return inputs.purchase_price - inputs.loan_amount


def cash_to_close(inputs: DealInputs) -> Decimal:
    return down_payment(inputs) + inputs.rehab_cost + inputs.points + inputs.closing_costs + inputs.reserves


def monthly_burn(inputs: DealInputs) -> Decimal:
    base_holding = inputs.holding_costs / Decimal(inputs.holding_months)
    return base_holding + inputs.operating_expense_monthly
