from research.models import (
    FinancialSummary,
    ValuationSummary,
)


def _to_float(value):
    """
    Converts values like:
    '12.3%'
    '23.6'
    'N/A'
    into float or None
    """
    try:
        return float(str(value).replace("%", "").strip())
    except Exception:
        return None


def generate_recommendation(
    financials: FinancialSummary,
    valuation: ValuationSummary,
):
    """
    Generates qualitative insights from the company's
    financials and valuation.

    Note:
    The investment recommendation (BUY/HOLD/SELL)
    is determined by the FreedomIQ Score Engine
    (score.rating), not by this function.
    """

    strengths = []
    weaknesses = []
    risks = []
    growth_drivers = []

    confidence_score = 0

    # -----------------------
    # PE
    # -----------------------

    pe = _to_float(valuation.pe)

    if pe is not None:

        if pe < 20:
            strengths.append("Attractive valuation")
            confidence_score += 2

        elif pe < 30:
            strengths.append("Reasonable valuation")
            confidence_score += 1

        else:
            risks.append("Premium valuation")

    # -----------------------
    # PEG
    # -----------------------

    peg = _to_float(valuation.peg)

    if peg is not None:

        if peg < 1:
            strengths.append("Growth appears reasonably priced")
            confidence_score += 2

    # -----------------------
    # Revenue Growth
    # -----------------------

    revenue = _to_float(financials.revenue_growth)

    if revenue is not None:

        if revenue > 15:
            strengths.append("Strong revenue growth")
            growth_drivers.append("Revenue is growing strongly")
            confidence_score += 2

        elif revenue < 0:
            weaknesses.append("Revenue is declining")

    # -----------------------
    # Profit Growth
    # -----------------------

    profit = _to_float(financials.profit_growth)

    if profit is not None:

        if profit > 10:
            strengths.append("Healthy earnings growth")
            growth_drivers.append("Profit is growing consistently")
            confidence_score += 2

        elif profit < 0:
            weaknesses.append("Profit declined compared to last year")

    # -----------------------
    # Operating Margin
    # -----------------------

    margin = _to_float(financials.operating_margin)

    if margin is not None:

        if margin > 10:
            strengths.append("Healthy operating margin")
            confidence_score += 1

    # -----------------------
    # Confidence
    # -----------------------

    if confidence_score >= 6:
        confidence = "High"

    elif confidence_score >= 3:
        confidence = "Medium"

    else:
        confidence = "Low"

    return (
        strengths,
        weaknesses,
        risks,
        growth_drivers,
        confidence,
    )