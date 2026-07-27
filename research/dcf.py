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
        except:
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

    def get_base_fcf(self):
        return self.financials.free_cash_flow

    def forecast_cashflows(self):
        return None

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