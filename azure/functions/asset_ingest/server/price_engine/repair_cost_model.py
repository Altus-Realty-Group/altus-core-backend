from __future__ import annotations

from decimal import Decimal

from server.price_engine.deal_inputs import DealInputs


def rehab_ratio(inputs: DealInputs) -> Decimal:
    if inputs.after_repair_value == 0:
        return Decimal("0")
    return inputs.rehab_cost / inputs.after_repair_value
