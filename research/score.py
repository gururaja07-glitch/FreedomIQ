from research.models import InvestmentScore, ValuationSummary, FinancialSummary


def _to_float(value: str) -> float | None:
    """
    Converts values like:
    '12.5%'
    '23.6'
    'N/A'
    ''
    into float or None.
    """
    if value is None:
        return None

    value = str(value).replace("%", "").replace(",", "").strip()

    if value in ("", "N/A", "None", "-"):
        return None

    try:
        return float(value)
    except ValueError:
        return None


def calculate_score(
    valuation: ValuationSummary,
    financials: FinancialSummary
):

    valuation_score = 0
    growth_score = 0
    profitability_score = 0
    financial_strength_score = 0
    business_quality_score = 10     # Neutral for now

    reasons = []

    # -----------------------------------
    # Valuation
    # -----------------------------------

    pe = _to_float(valuation.pe)
    pb = _to_float(valuation.pb)
    peg = _to_float(valuation.peg)

    if pe is not None:

        if pe < 20:
            valuation_score += 8
            reasons.append("PE below 20")

        elif pe < 30:
            valuation_score += 5
            reasons.append("PE in reasonable range")

    if pb is not None:

        if pb < 3:
            valuation_score += 6
            reasons.append("Low Price-to-Book")

    if peg is not None:

        if peg < 1:
            valuation_score += 6
            reasons.append("PEG below 1")

    valuation_score = min(20, valuation_score)

    # -----------------------------------
    # Growth
    # -----------------------------------

    revenue = _to_float(financials.revenue_growth)
    earnings = _to_float(financials.profit_growth)

    if revenue is not None:

        if revenue > 20:
            growth_score += 10
            reasons.append("Strong revenue growth")

        elif revenue > 10:
            growth_score += 5

    if earnings is not None:

        if earnings > 20:
            growth_score += 10
            reasons.append("Strong earnings growth")

        elif earnings > 10:
            growth_score += 5

    growth_score = min(20, growth_score)

    # -----------------------------------
    # Profitability
    # -----------------------------------

    margin = _to_float(financials.operating_margin)

    if margin is not None:

        if margin > 20:
            profitability_score += 20
            reasons.append("Excellent operating margin")

        elif margin > 10:
            profitability_score += 15
            reasons.append("Healthy operating margin")

        elif margin > 5:
            profitability_score += 10

    profitability_score = min(20, profitability_score)

    # -----------------------------------
    # Financial Strength
    # -----------------------------------

    debt = _to_float(financials.debt_equity)

    if debt is not None:

        if debt < 50:
            financial_strength_score += 20
            reasons.append("Comfortable debt level")

        elif debt < 100:
            financial_strength_score += 15

        else:
            financial_strength_score += 5

    financial_strength_score = min(20, financial_strength_score)

    total = (
        valuation_score
        + growth_score
        + profitability_score
        + financial_strength_score
        + business_quality_score
    )

    if total >= 90:
        rating = "Strong Buy"
        stars = "★★★★★"

    elif total >= 75:
        rating = "Buy"
        stars = "★★★★☆"

    elif total >= 60:
        rating = "Hold"
        stars = "★★★☆☆"

    elif total >= 40:
        rating = "Reduce"
        stars = "★★☆☆☆"

    else:
        rating = "Sell"
        stars = "★☆☆☆☆"

    score = InvestmentScore(
        valuation=valuation_score,
        growth=growth_score,
        profitability=profitability_score,
        financial_strength=financial_strength_score,
        business_quality=business_quality_score,
        total=total,
        stars=stars,
        rating=rating,
    )

    return score, reasons