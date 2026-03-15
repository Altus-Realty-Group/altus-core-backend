from __future__ import annotations

from decimal import Decimal

from server.price_engine.deal_inputs import DealInputs


def solve_mao(inputs: DealInputs) -> Decimal:
    return (inputs.after_repair_value * Decimal("0.70")) - inputs.rehab_cost - inputs.closing_costs
