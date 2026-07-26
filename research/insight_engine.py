"""
=========================================================
FreedomIQ Insight Engine
---------------------------------------------------------
Generates analytical insights from financial metrics.
=========================================================
"""

from research.models import (
    FinancialSummary,
    ValuationSummary,
    InvestmentScore,
)
from research.utils import safe_float


class InsightEngine:
    """
    Generates analytical insights from financial data.
    """

    def __init__(
        self,
        financials: FinancialSummary,
        valuation: ValuationSummary,
        score: InvestmentScore,
    ):
        self.financials = financials
        self.valuation = valuation
        self.score = score

    # -----------------------------------------------------
    # Helper
    # -----------------------------------------------------

    def _number(self, value):
        if value is None:
            return None

        return safe_float(str(value).replace("%", "").strip())

    # -----------------------------------------------------
    # Growth Insight
    # -----------------------------------------------------

    def growth_insight(self):
        """
        Analyses the relationship between revenue and earnings growth.
        """

        revenue = self._number(self.financials.revenue_growth)
        profit = self._number(self.financials.profit_growth)

        if revenue is None or profit is None:
            return "Growth data is insufficient for detailed analysis."

        if revenue >= 10 and profit >= 10:
            return (
                "Revenue and earnings are both growing at a healthy pace, "
                "indicating balanced business expansion."
            )

        if revenue >= 10 and profit < 10:
            return (
                "Revenue continues to grow well, although earnings growth has "
                "moderated, suggesting possible margin pressure or increased costs."
            )

        if revenue < 5 and profit < 5:
            return (
                "Both revenue and earnings growth remain subdued and should be "
                "monitored closely."
            )

        if profit > revenue:
            return (
                "Earnings are growing faster than revenue, indicating improving "
                "operational efficiency."
            )

        return "Growth trends appear stable."