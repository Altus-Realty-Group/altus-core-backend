from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from server.price_engine.deal_inputs import DealInputs
from server.price_engine.holding_cost_model import cash_to_close, monthly_burn
from server.price_engine.offer_price_solver import solve_mao
from server.price_engine.rent_model import annual_cash_flow, monthly_cash_flow
from server.price_engine.repair_cost_model import rehab_ratio


@dataclass(frozen=True)
class PriceEngineMetrics:
    mao: Decimal
    irr: Decimal
    cash_on_cash_return: Decimal
    cash_to_close: Decimal
    profit: Decimal
    risk_score: int


def calculate_metrics(inputs: DealInputs) -> PriceEngineMetrics:
    calculated_cash_to_close = cash_to_close(inputs)
    if calculated_cash_to_close <= Decimal("0"):
        raise ValueError("cash_to_close must be positive")

    monthly_income = monthly_cash_flow(inputs)
    annual_income = annual_cash_flow(inputs)
    mao = solve_mao(inputs)
    profit = inputs.after_repair_value - inputs.purchase_price - inputs.rehab_cost - inputs.holding_costs - inputs.selling_costs
    coc = (annual_income / calculated_cash_to_close) * Decimal("100")
    terminal_value = inputs.after_repair_value - inputs.selling_costs - inputs.loan_amount
    irr = _annualized_irr(
        [-calculated_cash_to_close]
        + [monthly_income for _ in range(max(inputs.holding_months - 1, 0))]
        + [monthly_income + terminal_value]
    )
    risk_score = _risk_score(inputs, calculated_cash_to_close)

    return PriceEngineMetrics(
        mao=_round_currency(mao),
        irr=_round_percent(irr),
        cash_on_cash_return=_round_percent(coc),
        cash_to_close=_round_currency(calculated_cash_to_close),
        profit=_round_currency(profit),
        risk_score=risk_score,
    )


def _annualized_irr(cashflows: list[Decimal]) -> Decimal:
    def npv(rate: Decimal) -> Decimal:
        total = Decimal("0")
        for index, cashflow in enumerate(cashflows):
            total += cashflow / ((Decimal("1") + rate) ** index)
        return total

    low = Decimal("-0.9999")
    high = Decimal("10")
    low_npv = npv(low)
    high_npv = npv(high)
    if low_npv == 0:
        monthly_rate = low
    elif high_npv == 0:
        monthly_rate = high
    elif low_npv * high_npv > 0:
        monthly_rate = Decimal("0")
    else:
        monthly_rate = Decimal("0")
        for _ in range(200):
            monthly_rate = (low + high) / Decimal("2")
            mid_npv = npv(monthly_rate)
            if abs(mid_npv) < Decimal("0.0000001"):
                break
            if low_npv * mid_npv <= 0:
                high = monthly_rate
                high_npv = mid_npv
            else:
                low = monthly_rate
                low_npv = mid_npv

    annual_rate = ((Decimal("1") + monthly_rate) ** Decimal("12")) - Decimal("1")
    return annual_rate * Decimal("100")


def _risk_score(inputs: DealInputs, calculated_cash_to_close: Decimal) -> int:
    purchase_ltv = Decimal("0") if inputs.purchase_price == 0 else inputs.loan_amount / inputs.purchase_price
    ltv_risk = _bounded_linear_risk(purchase_ltv, safe=Decimal("0.50"), risky=Decimal("0.85"))
    rehab_risk = _bounded_linear_risk(rehab_ratio(inputs), safe=Decimal("0.10"), risky=Decimal("0.35"))

    annual_noi = annual_cash_flow(inputs)
    annual_debt_service = _annual_debt_service(inputs.loan_amount, inputs.interest_rate_annual, inputs.amortization_months)
    if annual_debt_service <= Decimal("0"):
        dcr_risk = Decimal("0")
    else:
        dcr = annual_noi / annual_debt_service
        dcr_risk = _inverse_bounded_risk(dcr, safe=Decimal("1.50"), risky=Decimal("0.75"))

    reserve_cash = max(inputs.cash_available - calculated_cash_to_close, Decimal("0"))
    burn = monthly_burn(inputs)
    reserve_months = Decimal("12") if burn <= Decimal("0") else reserve_cash / burn
    reserve_risk = _inverse_bounded_risk(reserve_months, safe=Decimal("6"), risky=Decimal("0"))

    weighted = (
        (ltv_risk * Decimal("0.35"))
        + (rehab_risk * Decimal("0.25"))
        + (dcr_risk * Decimal("0.20"))
        + (reserve_risk * Decimal("0.20"))
    )
    return int(max(Decimal("0"), min(Decimal("100"), weighted)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _annual_debt_service(loan_amount: Decimal, annual_rate: Decimal, amortization_months: int) -> Decimal:
    if loan_amount <= Decimal("0") or annual_rate <= Decimal("0"):
        return Decimal("0")

    monthly_rate = annual_rate / Decimal("12")
    numerator = loan_amount * monthly_rate
    denominator = Decimal("1") - ((Decimal("1") + monthly_rate) ** Decimal(-amortization_months))
    if denominator == Decimal("0"):
        return Decimal("0")
    monthly_payment = numerator / denominator
    return monthly_payment * Decimal("12")


def _bounded_linear_risk(value: Decimal, *, safe: Decimal, risky: Decimal) -> Decimal:
    if value <= safe:
        return Decimal("0")
    if value >= risky:
        return Decimal("100")
    return ((value - safe) / (risky - safe)) * Decimal("100")


def _inverse_bounded_risk(value: Decimal, *, safe: Decimal, risky: Decimal) -> Decimal:
    if value >= safe:
        return Decimal("0")
    if value <= risky:
        return Decimal("100")
    return ((safe - value) / (safe - risky)) * Decimal("100")


def _round_currency(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _round_percent(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
