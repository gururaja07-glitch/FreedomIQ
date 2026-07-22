from research.models import (
    InvestmentScore,
    ValuationSummary,
    FinancialSummary,
)

from research.rules import (
    VALUATION_WEIGHT,
    GROWTH_WEIGHT,
    PROFITABILITY_WEIGHT,
    FINANCIAL_STRENGTH_WEIGHT,
    BUSINESS_QUALITY_WEIGHT,
    PE_EXCELLENT,
    PE_GOOD,
    PB_EXCELLENT,
    PEG_EXCELLENT,
    REVENUE_GROWTH_EXCELLENT,
    REVENUE_GROWTH_GOOD,
    PROFIT_GROWTH_EXCELLENT,
    PROFIT_GROWTH_GOOD,
    OPERATING_MARGIN_EXCELLENT,
    OPERATING_MARGIN_GOOD,
    DEBT_EQUITY_LOW,
    DEBT_EQUITY_MEDIUM,
    STRONG_BUY_SCORE,
    BUY_SCORE,
    HOLD_SCORE,
    REDUCE_SCORE,
    FIVE_STAR,
    FOUR_STAR,
    THREE_STAR,
    TWO_STAR,
    ONE_STAR,
)


def _to_float(value) -> float | None:
    """Convert string values like '12.5%', '1,234', 'N/A' into float."""

    if value is None:
        return None

    value = str(value).replace("%", "").replace(",", "").strip()

    if value in ("", "-", "N/A", "None"):
        return None

    try:
        return float(value)
    except ValueError:
        return None


# ==========================================================
# Valuation
# ==========================================================

def _score_valuation(
    valuation: ValuationSummary,
) -> tuple[int, list[str]]:

    score = 0
    reasons = []

    pe = _to_float(valuation.pe)
    pb = _to_float(valuation.pb)
    peg = _to_float(valuation.peg)

    if pe is not None:

        if pe < PE_EXCELLENT:
            score += 8
            reasons.append("Excellent PE valuation")

        elif pe < PE_GOOD:
            score += 5
            reasons.append("Reasonable PE valuation")

    if pb is not None:

        if pb < PB_EXCELLENT:
            score += 6
            reasons.append("Low Price-to-Book ratio")

    if peg is not None:

        if peg < PEG_EXCELLENT:
            score += 6
            reasons.append("PEG below 1 indicates attractive growth valuation")

    return min(score, VALUATION_WEIGHT), reasons


# ==========================================================
# Growth
# ==========================================================

def _score_growth(
    financials: FinancialSummary,
) -> tuple[int, list[str]]:

    score = 0
    reasons = []

    revenue = _to_float(financials.revenue_growth)
    earnings = _to_float(financials.profit_growth)

    if revenue is not None:

        if revenue > REVENUE_GROWTH_EXCELLENT:
            score += 10
            reasons.append("Strong revenue growth")

        elif revenue > REVENUE_GROWTH_GOOD:
            score += 5
            reasons.append("Healthy revenue growth")

    if earnings is not None:

        if earnings > PROFIT_GROWTH_EXCELLENT:
            score += 10
            reasons.append("Strong earnings growth")

        elif earnings > PROFIT_GROWTH_GOOD:
            score += 5
            reasons.append("Healthy earnings growth")

    return min(score, GROWTH_WEIGHT), reasons


# ==========================================================
# Profitability
# ==========================================================

def _score_profitability(
    financials: FinancialSummary,
) -> tuple[int, list[str]]:

    score = 0
    reasons = []

    margin = _to_float(financials.operating_margin)

    if margin is not None:

        if margin > OPERATING_MARGIN_EXCELLENT:
            score += 20
            reasons.append("Excellent operating margin")

        elif margin > OPERATING_MARGIN_GOOD:
            score += 15
            reasons.append("Healthy operating margin")

        elif margin > 5:
            score += 10
            reasons.append("Positive operating margin")

    return min(score, PROFITABILITY_WEIGHT), reasons


# ==========================================================
# Financial Strength
# ==========================================================

def _score_financial_strength(
    financials: FinancialSummary,
) -> tuple[int, list[str]]:

    score = 0
    reasons = []

    debt = _to_float(financials.debt_equity)

    if debt is not None:

        if debt < DEBT_EQUITY_LOW:
            score += 20
            reasons.append("Comfortable debt level")

        elif debt < DEBT_EQUITY_MEDIUM:
            score += 15
            reasons.append("Manageable debt level")

        else:
            score += 5
            reasons.append("High debt level")

    return min(score, FINANCIAL_STRENGTH_WEIGHT), reasons


# ==========================================================
# Rating
# ==========================================================

def _get_rating(total: int) -> tuple[str, str]:

    if total >= STRONG_BUY_SCORE:
        return "Strong Buy", FIVE_STAR

    if total >= BUY_SCORE:
        return "Buy", FOUR_STAR

    if total >= HOLD_SCORE:
        return "Hold", THREE_STAR

    if total >= REDUCE_SCORE:
        return "Reduce", TWO_STAR

    return "Sell", ONE_STAR


# ==========================================================
# Public API
# ==========================================================

def calculate_score(
    valuation: ValuationSummary,
    financials: FinancialSummary,
) -> InvestmentScore:

    valuation_score, valuation_reasons = _score_valuation(valuation)

    growth_score, growth_reasons = _score_growth(financials)

    profitability_score, profitability_reasons = (
        _score_profitability(financials)
    )

    financial_score, financial_reasons = (
        _score_financial_strength(financials)
    )

    business_quality_score = BUSINESS_QUALITY_WEIGHT // 2

    reasons = (
        valuation_reasons
        + growth_reasons
        + profitability_reasons
        + financial_reasons
    )

    total = (
        valuation_score
        + growth_score
        + profitability_score
        + financial_score
        + business_quality_score
    )

    rating, stars = _get_rating(total)

    score = InvestmentScore(
    valuation=valuation_score,
    growth=growth_score,
    profitability=profitability_score,
    financial_strength=financial_score,
    business_quality=business_quality_score,
    total=total,
    stars=stars,
    rating=rating,
    reasons=reasons,
    )

    return score