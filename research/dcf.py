"""
=========================================================
FreedomIQ DCF Valuation Engine
=========================================================
"""

from research.models import (
    Snapshot,
    FinancialSummary,
)

from research.dcf_config import (
    HIGH_GROWTH,
    MEDIUM_GROWTH,
    LOW_GROWTH,
    YEARS,
)


class DCFEngine:

    def __init__(
        self,
        snapshot: Snapshot,
        financials: FinancialSummary,
    ):
        self.snapshot = snapshot
        self.financials = financials

    # -----------------------------------------------------
    # Helper
    # -----------------------------------------------------

    def _number(self, value):

        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        try:
            return float(str(value).replace("%", "").replace(",", "").strip())
        except Exception:
            return None

    # -----------------------------------------------------
    # Growth Selection
    # -----------------------------------------------------

    def choose_growth_rate(self):
        """
        Select growth assumption based on
        recent revenue growth.
        """

        revenue_growth = self._number(
            self.financials.revenue_growth
        )

        if revenue_growth is None:
            return MEDIUM_GROWTH

        if revenue_growth >= 15:
            return HIGH_GROWTH

        elif revenue_growth >= 8:
            return MEDIUM_GROWTH

        return LOW_GROWTH

    # -----------------------------------------------------
    # Base Free Cash Flow
    # -----------------------------------------------------

    def get_base_fcf(self):
        return self._number(self.financials.free_cash_flow)

    # -----------------------------------------------------
    # Forecast Cash Flows
    # -----------------------------------------------------

    def forecast_cashflows(self):
        """
        Forecast Free Cash Flow for the next
        configured number of years.
        """

        base_fcf = self.get_base_fcf()

        if base_fcf is None:
            return []

        growth = self.choose_growth_rate()

        forecasts = []

        current_fcf = base_fcf

        for year in range(1, YEARS + 1):

            current_fcf *= (1 + growth)

            forecasts.append(
                {
                    "year": year,
                    "fcf": current_fcf,
                }
            )

        return forecasts

    # -----------------------------------------------------

    def calculate_terminal_value(self):
        return None

    def discount_cashflows(self):
        return None

    def intrinsic_value_per_share(self):
        return None

    def margin_of_safety(self):
        return None

    def verdict(self):
        return None