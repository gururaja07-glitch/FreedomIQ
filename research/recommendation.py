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
    into float or None.
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
    Generates qualitative insights.

    IMPORTANT:
    BUY / HOLD / SELL comes from the Score Engine.
    This module only explains WHY.
    """

    strengths = []
    weaknesses = []
    risks = []
    growth_drivers = []

    confidence_score = 0

    # =====================================================
    # Valuation (Single Source of Truth)
    # =====================================================

    if valuation.valuation == "Undervalued":
        strengths.append("Attractive valuation")
        confidence_score += 2

    elif valuation.valuation == "Fairly Valued":
        strengths.append("Reasonable valuation")
        confidence_score += 1

    elif valuation.valuation == "Expensive":
        risks.append("Premium valuation")

    # =====================================================
    # Revenue Growth
    # =====================================================

    revenue = _to_float(financials.revenue_growth)

    if revenue is not None:

        if revenue >= 15:
            strengths.append("Strong revenue growth")
            growth_drivers.append("Revenue is growing strongly")
            confidence_score += 2

        elif revenue >= 5:
            strengths.append("Healthy revenue growth")
            growth_drivers.append("Business continues to grow")
            confidence_score += 1

        elif revenue < 0:
            weaknesses.append("Revenue is declining")
            risks.append("Weak top-line growth")

    # =====================================================
    # Profit Growth
    # =====================================================

    profit = _to_float(financials.profit_growth)

    if profit is not None:

        if profit >= 15:
            strengths.append("Strong earnings growth")
            confidence_score += 2

        elif profit >= 5:
            strengths.append("Healthy earnings growth")
            confidence_score += 1

        elif profit < 0:
            weaknesses.append("Profit declined compared to last year")
            risks.append("Weak earnings momentum")

    # =====================================================
    # Operating Margin
    # =====================================================

    margin = _to_float(financials.operating_margin)

    if margin is not None:

        if margin >= 20:
            strengths.append("Excellent operating margin")
            confidence_score += 2

        elif margin >= 10:
            strengths.append("Healthy operating margin")
            confidence_score += 1

        elif margin < 5:
            weaknesses.append("Weak operating margin")

    # =====================================================
    # Confidence
    # =====================================================

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