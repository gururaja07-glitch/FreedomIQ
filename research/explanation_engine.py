"""
=========================================================
FreedomIQ Explanation Engine
---------------------------------------------------------
Centralized narrative generation for research reports.
=========================================================
"""

from research.models import (
    CompanySnapshot,
    FinancialSummary,
    ValuationSummary,
    InvestmentScore,
)

from research.utils import safe_float


class ExplanationEngine:
    """
    Generates analyst-style explanations from research data.
    """

    def __init__(
        self,
        snapshot: CompanySnapshot,
        financials: FinancialSummary,
        valuation: ValuationSummary,
        score: InvestmentScore,
    ):
        self.snapshot = snapshot
        self.financials = financials
        self.valuation = valuation
        self.score = score

    # -----------------------------------------------------
    # Helper
    # -----------------------------------------------------

    def _number(self, value):
        """
        Converts values like:
        '13.90%'
        '10.21'
        'N/A'
        into float.
        """

        if value is None:
            return None

        return safe_float(str(value).replace("%", "").strip())

    # -----------------------------------------------------
    # Executive Summary
    # -----------------------------------------------------

    def executive_summary(self):
        """
        Generates a concise executive summary.
        """

        company = self.snapshot.company
        rating = self.score.rating
        total = self.score.total

        parts = []

        parts.append(
            f"{company} is a {rating.lower()} rated company with a FreedomIQ score of {total}/100."
        )

        if self.score.profitability >= 15:
            parts.append("The business demonstrates strong profitability.")

        if self.score.growth >= 15:
            parts.append("Growth indicators remain healthy.")
        elif self.score.growth <= 5:
            parts.append("Growth appears to be slowing.")

        if self.score.valuation >= 15:
            parts.append("Current valuation appears attractive.")
        elif self.score.valuation <= 5:
            parts.append("Valuation does not appear particularly attractive.")

        if self.score.financial_strength >= 15:
            parts.append("The balance sheet looks financially strong.")

        parts.append(
            f"Overall, FreedomIQ assigns a {rating.upper()} recommendation based on the available financial data."
        )

        return " ".join(parts)

    # -----------------------------------------------------
    # Strengths
    # -----------------------------------------------------

    def strengths(self):
        """
        Generates company strengths.
        """

        strengths = []

        # Valuation

        if self.valuation.valuation == "Undervalued":
            strengths.append("Attractive valuation")

        elif self.valuation.valuation == "Fairly Valued":
            strengths.append("Reasonable valuation")

        # Revenue Growth

        revenue = self._number(self.financials.revenue_growth)

        if revenue is not None:

            if revenue >= 15:
                strengths.append("Strong revenue growth")

            elif revenue >= 5:
                strengths.append("Healthy revenue growth")

        # Profit Growth

        profit = self._number(self.financials.profit_growth)

        if profit is not None:

            if profit >= 15:
                strengths.append("Strong earnings growth")

            elif profit >= 5:
                strengths.append("Healthy earnings growth")

        # Operating Margin

        margin = self._number(self.financials.operating_margin)

        if margin is not None:

            if margin >= 20:
                strengths.append("Excellent operating margin")

            elif margin >= 10:
                strengths.append("Healthy operating margin")

        return strengths

    # -----------------------------------------------------
    # Weaknesses
    # -----------------------------------------------------

    def weaknesses(self):
        return []

    # -----------------------------------------------------
    # Risks
    # -----------------------------------------------------

    def risks(self):
        return []

    # -----------------------------------------------------
    # Growth Drivers
    # -----------------------------------------------------

    def growth_drivers(self):
        return []

    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    def confidence(self):
        return "Medium"

           # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    def confidence(self):
        return "Medium"

        # -----------------------------------------------------
    # Investment Thesis
    # -----------------------------------------------------

    def investment_thesis(self):
        """
        Generates an analyst-style investment thesis.
        """

        company = self.snapshot.company

        revenue = self._number(self.financials.revenue_growth)
        profit = self._number(self.financials.profit_growth)
        roe = self._number(self.financials.roe)
        margin = self._number(self.financials.operating_margin)

        parts = []

        # -------------------------------------------------
        # Opening
        # -------------------------------------------------

        parts.append(f"{company} ")

        # -------------------------------------------------
        # Profitability
        # -------------------------------------------------

        if roe is not None and roe >= 20:
            parts.append(
                "is a financially strong business generating excellent returns on shareholder capital."
            )
        elif margin is not None and margin >= 20:
            parts.append(
                "maintains excellent operating profitability."
            )
        else:
            parts.append(
                "shows adequate business profitability."
            )

        # -------------------------------------------------
        # Growth
        # -------------------------------------------------

        if revenue is not None and profit is not None:

            if revenue >= 10 and profit >= 10:
                parts.append(
                    "Both revenue and earnings continue to grow at a healthy pace."
                )

            elif revenue >= 10 and profit < 10:
                parts.append(
                    "Revenue continues to grow well, although earnings growth has moderated."
                )

            elif revenue < 5 and profit < 5:
                parts.append(
                    "Growth remains subdued and will require close monitoring."
                )

        # -------------------------------------------------
        # Financial Strength
        # -------------------------------------------------

        if self.score.financial_strength >= 15:
            parts.append(
                "The balance sheet remains strong."
            )

        # -------------------------------------------------
        # Valuation
        # -------------------------------------------------

        if self.valuation.valuation == "Undervalued":
            parts.append(
                "Current valuation appears attractive."
            )

        elif self.valuation.valuation == "Fairly Valued":
            parts.append(
                "Current valuation appears reasonable."
            )

        else:
            parts.append(
                "Current valuation appears expensive."
            )

        # -------------------------------------------------
        # Conclusion
        # -------------------------------------------------

        parts.append(
            f"Overall, these characteristics support a {self.score.rating.upper()} recommendation."
        )

        return " ".join(parts)