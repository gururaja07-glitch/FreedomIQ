"""
=========================================================
FreedomIQ DCF Valuation Engine
=========================================================
"""

from research.models import (
    Snapshot,
    FinancialSummary,
    DCFResult,
)

from research.dcf_config import (
    YEARS,
    DISCOUNT_RATE,
    TERMINAL_GROWTH,
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

    def _number(self, value):

        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        try:
            return float(
                str(value)
                .replace("%", "")
                .replace(",", "")
                .strip()
            )
        except Exception:
            return None

    # -----------------------------------------------------

    def choose_growth_rate(self):

        growth = self._number(
            self.financials.revenue_growth
        )

        if growth is None:
            return MEDIUM_GROWTH

        if growth >= 15:
            return HIGH_GROWTH

        if growth >= 8:
            return MEDIUM_GROWTH

        return LOW_GROWTH

    # -----------------------------------------------------

    def get_base_fcf(self):

        return self._number(
            self.financials.free_cash_flow
        )

    # -----------------------------------------------------

    def forecast_cashflows(self):

        base = self.get_base_fcf()

        if base is None:
            return []

        growth = self.choose_growth_rate()

        cashflows = []

        current = base

        for year in range(1, YEARS + 1):

            current *= (1 + growth)

            cashflows.append(
                {
                    "year": year,
                    "fcf": current,
                }
            )

        return cashflows

    # -----------------------------------------------------

    def discount_cashflows(self):

        discounted = []

        total = 0.0

        for row in self.forecast_cashflows():

            pv = (
                row["fcf"] /
                ((1 + DISCOUNT_RATE) ** row["year"])
            )

            total += pv

            discounted.append(
                {
                    "year": row["year"],
                    "fcf": row["fcf"],
                    "pv": pv,
                }
            )

        return discounted, total

    # -----------------------------------------------------

    def calculate_terminal_value(self):

        forecasts = self.forecast_cashflows()

        if not forecasts:
            return 0.0

        final_fcf = forecasts[-1]["fcf"]

        terminal = (
            final_fcf *
            (1 + TERMINAL_GROWTH)
        ) / (
            DISCOUNT_RATE - TERMINAL_GROWTH
        )

        return terminal

    # -----------------------------------------------------

    def discount_terminal_value(self):

        terminal = self.calculate_terminal_value()

        return terminal / (
            (1 + DISCOUNT_RATE) ** YEARS
        )

    # -----------------------------------------------------

    def enterprise_value(self):

        _, forecast_pv = self.discount_cashflows()

        terminal_pv = self.discount_terminal_value()

        return forecast_pv + terminal_pv

    # -----------------------------------------------------

    def calculate(self):

        forecasts = self.forecast_cashflows()

        discounted = []

        forecast_pv = 0.0

        for row in forecasts:

            pv = (
                row["fcf"] /
                ((1 + DISCOUNT_RATE) ** row["year"])
            )

            forecast_pv += pv

            discounted.append(
                {
                    "year": row["year"],
                    "fcf": row["fcf"],
                    "pv": pv,
                }
            )

        if forecasts:
            final_fcf = forecasts[-1]["fcf"]

            terminal_value = (
                final_fcf *
                (1 + TERMINAL_GROWTH)
            ) / (
                DISCOUNT_RATE - TERMINAL_GROWTH
            )

            discounted_terminal = (
                terminal_value /
                ((1 + DISCOUNT_RATE) ** YEARS)
            )
        else:
            terminal_value = 0.0
            discounted_terminal = 0.0

        enterprise_value = (
            forecast_pv +
            discounted_terminal
        )

        return DCFResult(

            forecast_cashflows=forecasts,

            discounted_cashflows=discounted,

            forecast_pv=forecast_pv,

            terminal_value=terminal_value,

            discounted_terminal_value=discounted_terminal,

            enterprise_value=enterprise_value,

            assumptions={
                "growth_rate": self.choose_growth_rate(),
                "discount_rate": DISCOUNT_RATE,
                "terminal_growth": TERMINAL_GROWTH,
                "years": YEARS,
            },
        )