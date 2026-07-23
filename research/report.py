from research.models import (
    CompanyAnalysis,
    ResearchReport,
)


def build_report(analysis: CompanyAnalysis) -> ResearchReport:
    """
    Convert CompanyAnalysis into a reusable ResearchReport.
    No calculations.
    No formatting.
    """

    return ResearchReport(
        snapshot=analysis.snapshot,
        financials=analysis.financials,
        valuation=analysis.valuation,

        score=analysis.score,

        strengths=analysis.strengths,
        weaknesses=analysis.weaknesses,
        risks=analysis.risks,
        growth_drivers=analysis.growth_drivers,

        confidence=analysis.confidence,
    )