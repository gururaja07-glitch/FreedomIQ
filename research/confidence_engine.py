"""
=========================================================
FreedomIQ Confidence Engine
---------------------------------------------------------
Generates confidence rating for the recommendation.
=========================================================
"""

from research.models import (
    FinancialSummary,
    ValuationSummary,
    InvestmentScore,
    ConfidenceSummary,
)


class ConfidenceEngine:

    def __init__(
        self,
        financials: FinancialSummary,
        valuation: ValuationSummary,
        score: InvestmentScore,
    ):
        self.financials = financials
        self.valuation = valuation
        self.score = score

    def confidence(self) -> ConfidenceSummary:
        """
        Returns confidence rating and reasons.
        """

        score = 0
        reasons = []

        # Complete financial data
        if self.financials.revenue_growth != "N/A":
            score += 1
            reasons.append("Complete financial data available.")

        # Strong profitability
        if self.score.profitability >= 15:
            score += 1
            reasons.append("Strong profitability metrics.")

        # Strong financial position
        if self.score.financial_strength >= 15:
            score += 1
            reasons.append("Healthy financial position.")

        # Valuation available
        if self.valuation.valuation != "Unknown":
            score += 1
            reasons.append("Valuation analysis available.")

        if score == 4:
            stars = "*****"
            level = "High"

        elif score == 3:
            stars = "****"
            level = "Good"

        elif score == 2:
            stars = "***"
            level = "Medium"

        else:
            stars = "**"
            level = "Low"

        return ConfidenceSummary(
            stars=stars,
            level=level,
            reasons=reasons,
        )