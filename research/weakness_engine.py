"""
=========================================================
FreedomIQ Weakness Engine
---------------------------------------------------------
Identifies company-specific weaknesses from financial data.
=========================================================
"""

from research.models import (
    FinancialSummary,
    ValuationSummary,
)

from research.utils import safe_float


class WeaknessEngine:

    def __init__(self, financials: FinancialSummary, valuation: ValuationSummary):
        self.financials = financials
        self.valuation = valuation

    # -----------------------------------------------------
    # Helper
    # -----------------------------------------------------

    def _number(self, value):
        if value is None:
            return None

        return safe_float(str(value).replace("%", "").strip())

    # -----------------------------------------------------
    # Weakness Analysis
    # -----------------------------------------------------

    def weaknesses(self):
        """
        Returns a list of identified weaknesses.
        """

        weaknesses = []

        revenue = self._number(self.financials.revenue_growth)
        profit = self._number(self.financials.profit_growth)
        peg = self._number(self.valuation.peg)

        # Earnings lag revenue
        if (
            revenue is not None
            and profit is not None
            and revenue >= 10
            and profit < revenue / 2
        ):
            weaknesses.append(
                "Earnings growth has moderated despite healthy revenue growth."
            )

        # Expensive valuation
        if self.valuation.valuation == "Overvalued":
            weaknesses.append(
                "Current valuation appears expensive."
            )

        # High PEG
        if peg is not None and peg > 2:
            weaknesses.append(
                "PEG ratio suggests growth may not fully justify the current valuation."
            )

        return weaknesses