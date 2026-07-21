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

    strengths = []
    weaknesses = []
    risks = []
    growth_drivers = []

    score = 0

    # -----------------------
    # PE
    # -----------------------

    pe = _to_float(valuation.pe)

    if pe is not None:

        if pe < 20:
            strengths.append("Attractive valuation")
            score += 2

        elif pe < 30:
            strengths.append("Reasonable valuation")
            score += 1

        else:
            risks.append("Premium valuation")

    # -----------------------
    # PEG
    # -----------------------

    peg = _to_float(valuation.peg)

    if peg is not None:

        if peg < 1:
            strengths.append("Growth appears reasonably priced")
            score += 2

    # -----------------------
    # Revenue Growth
    # -----------------------

    revenue = _to_float(financials.revenue_growth)

    if revenue is not None:

        if revenue > 15:
            strengths.append("Strong revenue growth")
            score += 2

        elif revenue < 0:
            weaknesses.append("Revenue is declining")

    # -----------------------
    # Profit Growth
    # -----------------------

    profit = _to_float(financials.profit_growth)

    if profit is not None:

        if profit > 10:
            strengths.append("Healthy earnings growth")
            score += 2

        elif profit < 0:
            weaknesses.append("Profit declined compared to last year")
            score -= 1

    # -----------------------
    # Operating Margin
    # -----------------------

    margin = _to_float(financials.operating_margin)

    if margin is not None:

        if margin > 10:
            strengths.append("Healthy operating margin")
            score += 1

    # -----------------------
    # Final Recommendation
    # -----------------------

    if score >= 6:
        recommendation = "STRONG BUY"
        confidence = "High"

    elif score >= 4:
        recommendation = "BUY"
        confidence = "High"

    elif score >= 2:
        recommendation = "HOLD"
        confidence = "Medium"

    else:
        recommendation = "SELL"
        confidence = "Medium"

    return (
        strengths,
        weaknesses,
        risks,
        growth_drivers,
        recommendation,
        confidence,
    )