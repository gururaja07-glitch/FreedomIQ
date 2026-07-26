from research.models import (
    CompanyAnalysis,
    ResearchReport,
)

from research.explanation_engine import ExplanationEngine
from research.insight_engine import InsightEngine


def build_report(analysis: CompanyAnalysis) -> ResearchReport:
    """
    Convert CompanyAnalysis into a reusable ResearchReport.

    No calculations.
    No formatting.
    """

    explanation = ExplanationEngine(
        analysis.snapshot,
        analysis.financials,
        analysis.valuation,
        analysis.score,
    )

    insights = InsightEngine(
        analysis.financials,
        analysis.valuation,
        analysis.score,
    )

    return ResearchReport(
        snapshot=analysis.snapshot,
        financials=analysis.financials,
        valuation=analysis.valuation,
        score=analysis.score,

        summary=explanation.executive_summary(),
        investment_thesis=explanation.investment_thesis(),

        strengths=explanation.strengths(),
        weaknesses=analysis.weaknesses,
        risks=analysis.risks,

        # First dynamic insight from the Insight Engine
        growth_drivers=[insights.growth_insight()],

        confidence=analysis.confidence,
    )