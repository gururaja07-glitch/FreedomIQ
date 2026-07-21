from research.models import (
    CompanyAnalysis,
)

from research.snapshot import get_company_snapshot
from research.valuation import get_valuation
from research.financials import get_financials
from research.recommendation import generate_recommendation


def analyze_company(company_name: str) -> CompanyAnalysis:
    """
    Returns a structured company analysis.
    """

    # Get company snapshot and Yahoo Finance data
    snapshot, info = get_company_snapshot(company_name)

    # Extract valuation
    valuation = get_valuation(info)

    # Extract financials
    financials = get_financials(info)

    # Generate recommendation
    (
        strengths,
        weaknesses,
        risks,
        growth_drivers,
        recommendation,
        confidence,
    ) = generate_recommendation(
        financials,
        valuation,
    )

    return CompanyAnalysis(
        snapshot=snapshot,
        financials=financials,
        valuation=valuation,
        strengths=strengths,
        weaknesses=weaknesses,
        risks=risks,
        growth_drivers=growth_drivers,
        recommendation=recommendation,
        confidence=confidence,
    )