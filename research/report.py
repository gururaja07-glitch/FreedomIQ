from research.models import (
    CompanyAnalysis,
    ResearchReport,
)

from research.explanation_engine import ExplanationEngine


from research.models import (
    CompanyAnalysis,
    ResearchReport,
)

from research.explanation_engine import ExplanationEngine


def build_report(analysis: CompanyAnalysis) -> ResearchReport:
    """
    Convert CompanyAnalysis into a reusable ResearchReport.

    No calculations.
    No formatting.
    """

    engine = ExplanationEngine(
        analysis.snapshot,
        analysis.financials,
        analysis.valuation,
        analysis.score,
    )

    return ResearchReport(
        snapshot=analysis.snapshot,
        financials=analysis.financials,
        valuation=analysis.valuation,

        score=analysis.score,

        summary=engine.executive_summary(),
        investment_thesis=engine.investment_thesis(),

        strengths=engine.strengths(),
        weaknesses=analysis.weaknesses,
        risks=analysis.risks,
        growth_drivers=analysis.growth_drivers,

        confidence=analysis.confidence,
    )