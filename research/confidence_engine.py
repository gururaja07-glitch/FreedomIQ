"""
FreedomIQ Confidence Engine

Generates confidence rating for the recommendation.
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

        # -----------------------------------------------------
        # Financial Data Completeness
        # -----------------------------------------------------

        core_fields = [
            self.financials.revenue_growth,
            self.financials.profit_growth,
            self.financials.roe,
            self.financials.debt_equity,
            self.financials.operating_margin,
            self.financials.free_cash_flow,
        ]

        available = sum(
            value not in (None, "", "N/A")
            for value in core_fields
        )

        total_fields = len(core_fields)

        if available == total_fields:

            score += 1

            reasons.append(
                f"Complete financial data available "
                f"({available}/{total_fields} core metrics)."
            )

        elif available >= 4:

            reasons.append(
                f"Partial financial data available "
                f"({available}/{total_fields} core metrics)."
            )

        else:

            reasons.append(
                f"Limited financial data available "
                f"({available}/{total_fields} core metrics)."
            )

        # -----------------------------------------------------
        # Strong profitability
        # -----------------------------------------------------

        if self.score.profitability >= 15:

            score += 1

            reasons.append(
                "Strong profitability metrics."
            )

        # -----------------------------------------------------
        # Strong financial position
        # -----------------------------------------------------

        if self.score.financial_strength >= 15:

            score += 1

            reasons.append(
                "Healthy financial position."
            )

        # -----------------------------------------------------
        # Valuation available
        # -----------------------------------------------------

        if self.valuation.valuation != "Unknown":

            score += 1

            reasons.append(
                "Valuation analysis available."
            )

        # -----------------------------------------------------
        # Final confidence
        # -----------------------------------------------------

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