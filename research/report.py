from research.models import (
    CompanyAnalysis,
    ResearchReport,
)

from research.summary import generate_summary


def build_report(analysis: CompanyAnalysis) -> ResearchReport:
    """
    Convert CompanyAnalysis into a reusable ResearchReport.
    No calculations.
    No formatting.
    """

    summary = generate_summary(
        analysis.snapshot,
        analysis.financials,
        analysis.valuation,
        analysis.score,
    )
    print("SUMMARY:", repr(summary))
    return ResearchReport(
        snapshot=analysis.snapshot,
        financials=analysis.financials,
        valuation=analysis.valuation,

        score=analysis.score,

        summary=summary,

        strengths=analysis.strengths,
        weaknesses=analysis.weaknesses,
        risks=analysis.risks,
        growth_drivers=analysis.growth_drivers,

        confidence=analysis.confidence,
    )