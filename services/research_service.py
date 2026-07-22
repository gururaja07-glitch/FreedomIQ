from research.models import (
    CompanyAnalysis,
)

from research.snapshot import get_company_snapshot
from research.valuation import get_valuation
from research.financials import get_financials
from research.score import calculate_score
from research.recommendation import generate_recommendation


def analyze_company(company_name: str) -> CompanyAnalysis:
    """
    Returns a structured company analysis.
    """

    # -------------------------------------------------
    # Fetch data
    # -------------------------------------------------

    snapshot, info = get_company_snapshot(company_name)

    valuation = get_valuation(info)

    financials = get_financials(info)

    # -------------------------------------------------
    # FreedomIQ Score
    # -------------------------------------------------

    score = calculate_score(
        valuation,
        financials,
    )

    # -------------------------------------------------
    # AI Explanation
    # -------------------------------------------------

    (
    strengths,
    weaknesses,
    risks,
    growth_drivers,
    confidence,
    ) = generate_recommendation(
    financials,
    valuation,
    )

    # -------------------------------------------------
    # Return Analysis
    # -------------------------------------------------

    return CompanyAnalysis(
        snapshot=snapshot,
        financials=financials,
        valuation=valuation,
        score=score,
        strengths=strengths,
        weaknesses=weaknesses,
        risks=risks,
        growth_drivers=growth_drivers,
        confidence=confidence,
    )