"""
FreedomIQ DCF Valuation Engine

Three-scenario DCF with gradual growth fade.

Scenarios:
    Conservative
    Base
    Optimistic

The Base case remains the primary DCF result.
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
    CONSERVATIVE_ADJUSTMENT,
    BASE_ADJUSTMENT,
    OPTIMISTIC_ADJUSTMENT,
    MIN_GROWTH,
    MAX_GROWTH,
    FADE_FACTOR_YEAR_10,
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
    # Number conversion
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
    # Base growth assessment
    # -----------------------------------------------------

    def choose_growth_rate(self):

        growth = self._number(
            self.financials.revenue_growth
        )

        if growth is None:
            return 0.10

        if growth >= 15:
            return 0.15

        if growth >= 8:
            return 0.10

        return 0.05

    # -----------------------------------------------------
    # Growth scenario
    # -----------------------------------------------------

    def _scenario_start_growth(
        self,
        adjustment,
    ):
        """
        Calculate starting growth for a scenario.

        The original FreedomIQ growth assessment remains
        the base starting point.

        Scenario adjustment is then applied.
        """

        base_growth = self.choose_growth_rate()

        growth = base_growth + adjustment

        growth = max(
            MIN_GROWTH,
            min(MAX_GROWTH, growth),
        )

        return growth

    # -----------------------------------------------------
    # Year-by-year growth fade
    # -----------------------------------------------------

    def _growth_for_year(
        self,
        start_growth,
        year,
    ):
        """
        Gradually fade starting growth toward terminal growth.

        Year 1:
            100% of excess growth remains.

        Year 10:
            FADE_FACTOR_YEAR_10 remains.

        Terminal growth is not used as the Year-10 growth;
        it is the perpetual growth rate after the forecast
        period.
        """

        if YEARS <= 1:

            fade_factor = 1.0

        else:

            progress = (
                (year - 1)
                / (YEARS - 1)
            )

            fade_factor = (
                1.0
                - progress
                * (1.0 - FADE_FACTOR_YEAR_10)
            )

        growth = (
            TERMINAL_GROWTH
            + (
                start_growth
                - TERMINAL_GROWTH
            )
            * fade_factor
        )

        return growth

    # -----------------------------------------------------
    # Base FCF
    # -----------------------------------------------------

    def get_base_fcf(self):

        return self._number(
            self.financials.free_cash_flow
        )

    # -----------------------------------------------------
    # Forecast cash flows for one scenario
    # -----------------------------------------------------

    def _forecast_scenario(
        self,
        start_growth,
    ):
        """
        Forecast FCF for one scenario.
        """

        base_fcf = self.get_base_fcf()

        if base_fcf is None:
            return []

        forecasts = []

        current_fcf = base_fcf

        for year in range(1, YEARS + 1):

            growth = self._growth_for_year(
                start_growth,
                year,
            )

            current_fcf *= (
                1 + growth
            )

            forecasts.append(
                {
                    "year": year,
                    "growth": growth,
                    "fcf": current_fcf,
                }
            )

        return forecasts

    # -----------------------------------------------------
    # Discount scenario
    # -----------------------------------------------------

    def _calculate_scenario(
        self,
        name,
        start_growth,
    ):
        """
        Calculate complete DCF for one scenario.
        """

        forecasts = self._forecast_scenario(
            start_growth
        )

        if not forecasts:
            return {
                "scenario": name,
                "status": "Unavailable",
            }

        discounted = []

        forecast_pv = 0.0

        for row in forecasts:

            pv = (
                row["fcf"]
                / (
                    (1 + DISCOUNT_RATE)
                    ** row["year"]
                )
            )

            forecast_pv += pv

            discounted.append(
                {
                    "year": row["year"],
                    "growth": row["growth"],
                    "fcf": row["fcf"],
                    "pv": pv,
                }
            )

        # -------------------------------------------------
        # Terminal value
        # -------------------------------------------------

        final_fcf = forecasts[-1]["fcf"]

        terminal_value = (
            final_fcf
            * (1 + TERMINAL_GROWTH)
        ) / (
            DISCOUNT_RATE
            - TERMINAL_GROWTH
        )

        discounted_terminal = (
            terminal_value
            / (
                (1 + DISCOUNT_RATE)
                ** YEARS
            )
        )

        # -------------------------------------------------
        # Enterprise value
        # -------------------------------------------------

        enterprise_value = (
            forecast_pv
            + discounted_terminal
        )

        # -------------------------------------------------
        # Equity value
        # -------------------------------------------------

        cash = (
            self.financials.cash
            or 0.0
        )

        debt = (
            self.financials.total_debt
            or 0.0
        )

        intrinsic_value = (
            enterprise_value
            + cash
            - debt
        )

        # -------------------------------------------------
        # Per-share value
        # -------------------------------------------------

        shares = (
            self.snapshot.shares_outstanding
            or 0.0
        )

        if shares > 0:

            intrinsic_per_share = (
                intrinsic_value
                / shares
            )

        else:

            intrinsic_per_share = 0.0

        # -------------------------------------------------
        # Terminal contribution
        # -------------------------------------------------

        if enterprise_value > 0:

            terminal_percentage = (
                discounted_terminal
                / enterprise_value
            ) * 100

        else:

            terminal_percentage = 0.0

        return {
            "scenario": name,
            "status": "Available",
            "start_growth": start_growth,
            "forecasts": forecasts,
            "discounted_cashflows": discounted,
            "forecast_pv": forecast_pv,
            "terminal_value": terminal_value,
            "discounted_terminal_value": (
                discounted_terminal
            ),
            "enterprise_value": enterprise_value,
            "intrinsic_value": intrinsic_value,
            "intrinsic_value_per_share": (
                intrinsic_per_share
            ),
            "terminal_value_percentage": (
                terminal_percentage
            ),
        }

    # -----------------------------------------------------
    # Calculate
    # -----------------------------------------------------

    def calculate(self):

        base_fcf = self.get_base_fcf()

        # -------------------------------------------------
        # No FCF
        # -------------------------------------------------

        if base_fcf is None:

            return DCFResult(

                forecast_cashflows=[],

                discounted_cashflows=[],

                forecast_pv=0.0,

                terminal_value=0.0,

                discounted_terminal_value=0.0,

                enterprise_value=0.0,

                intrinsic_value=0.0,

                intrinsic_value_per_share=0.0,

                current_price=(
                    self.snapshot.current_price
                    or 0.0
                ),

                margin_of_safety=0.0,

                verdict="Unavailable",

                assumptions={
                    "base_fcf": None,
                    "growth_method": (
                        "Revenue growth mapped to "
                        "scenario starting growth "
                        "with gradual fade"
                    ),
                    "discount_rate": DISCOUNT_RATE,
                    "terminal_growth": (
                        TERMINAL_GROWTH
                    ),
                    "years": YEARS,
                    "cash": self.financials.cash,
                    "debt": self.financials.total_debt,
                    "shares_outstanding": (
                        self.snapshot.shares_outstanding
                    ),
                    "scenarios": {},
                    "sensitivity": {},
                },

                status="Unavailable",

                reason=(
                    "Free cash flow data is unavailable."
                ),
            )

        # -------------------------------------------------
        # Scenario starting growth rates
        # -------------------------------------------------

        conservative_growth = (
            self._scenario_start_growth(
                CONSERVATIVE_ADJUSTMENT
            )
        )

        base_growth = (
            self._scenario_start_growth(
                BASE_ADJUSTMENT
            )
        )

        optimistic_growth = (
            self._scenario_start_growth(
                OPTIMISTIC_ADJUSTMENT
            )
        )
        # -------------------------------------------------
        # Calculate scenarios
        # -------------------------------------------------

        conservative = (
            self._calculate_scenario(
                "Conservative",
                conservative_growth,
            )
        )

        base = (
            self._calculate_scenario(
                "Base",
                base_growth,
            )
        )

        optimistic = (
            self._calculate_scenario(
                "Optimistic",
                optimistic_growth,
            )
        )

        # -------------------------------------------------
        # Base Case Sensitivity Analysis
        # -------------------------------------------------

        sensitivity = (
            self._calculate_sensitivity(
                base["forecasts"]
            )
        )

        # -------------------------------------------------
        # Base case becomes primary DCF result
        # -------------------------------------------------

        intrinsic_value = (
            base["intrinsic_value"]
        )

        intrinsic_per_share = (
            base["intrinsic_value_per_share"]
        )

        current_price = (
            self.snapshot.current_price
            or 0.0
        )

        if intrinsic_per_share > 0:

            margin = (
                (
                    intrinsic_per_share
                    - current_price
                )
                / intrinsic_per_share
            ) * 100

        else:

            margin = 0.0

        # -------------------------------------------------
        # Base verdict
        # -------------------------------------------------

        if margin >= 30:

            verdict = "Strong Buy"

        elif margin >= 15:

            verdict = "Buy"

        elif margin >= -10:

            verdict = "Hold"

        elif margin >= -25:

            verdict = "Reduce"

        else:

            verdict = "Sell"

        # -------------------------------------------------
        # Assumptions / audit information
        # -------------------------------------------------

        assumptions = {

            "base_fcf": base_fcf,

            "growth_method": (
                "Revenue growth mapped to "
                "scenario starting growth "
                "with gradual fade toward "
                "terminal growth"
            ),

            "base_start_growth": base_growth,

            "conservative_start_growth": (
                conservative_growth
            ),

            "optimistic_start_growth": (
                optimistic_growth
            ),

            "discount_rate": DISCOUNT_RATE,

            "terminal_growth": (
                TERMINAL_GROWTH
            ),

            "years": YEARS,

            "minimum_growth": MIN_GROWTH,

            "maximum_growth": MAX_GROWTH,

            "year_10_fade_factor": (
                FADE_FACTOR_YEAR_10
            ),

            "cash": (
                self.financials.cash
                or 0.0
            ),

            "debt": (
                self.financials.total_debt
                or 0.0
            ),

            "shares_outstanding": (
                self.snapshot.shares_outstanding
                or 0.0
            ),

            "terminal_value_percentage": (
                base[
                    "terminal_value_percentage"
                ]
            ),

            "sensitivity": sensitivity,

            "scenarios": {

                "Conservative": {
                    "start_growth": (
                        conservative[
                            "start_growth"
                        ]
                    ),
                    "intrinsic_value": (
                        conservative[
                            "intrinsic_value"
                        ]
                    ),
                    "intrinsic_value_per_share": (
                        conservative[
                            "intrinsic_value_per_share"
                        ]
                    ),
                    "forecast_pv": (
                        conservative[
                            "forecast_pv"
                        ]
                    ),
                    "discounted_terminal_value": (
                        conservative[
                            "discounted_terminal_value"
                        ]
                    ),
                    "enterprise_value": (
                        conservative[
                            "enterprise_value"
                        ]
                    ),
                    "terminal_value_percentage": (
                        conservative[
                            "terminal_value_percentage"
                        ]
                    ),
                },

                "Base": {
                    "start_growth": (
                        base[
                            "start_growth"
                        ]
                    ),
                    "intrinsic_value": (
                        base[
                            "intrinsic_value"
                        ]
                    ),
                    "intrinsic_value_per_share": (
                        base[
                            "intrinsic_value_per_share"
                        ]
                    ),
                    "forecast_pv": (
                        base[
                            "forecast_pv"
                        ]
                    ),
                    "discounted_terminal_value": (
                        base[
                            "discounted_terminal_value"
                        ]
                    ),
                    "enterprise_value": (
                        base[
                            "enterprise_value"
                        ]
                    ),
                    "terminal_value_percentage": (
                        base[
                            "terminal_value_percentage"
                        ]
                    ),
                },

                "Optimistic": {
                    "start_growth": (
                        optimistic[
                            "start_growth"
                        ]
                    ),
                    "intrinsic_value": (
                        optimistic[
                            "intrinsic_value"
                        ]
                    ),
                    "intrinsic_value_per_share": (
                        optimistic[
                            "intrinsic_value_per_share"
                        ]
                    ),
                    "forecast_pv": (
                        optimistic[
                            "forecast_pv"
                        ]
                    ),
                    "discounted_terminal_value": (
                        optimistic[
                            "discounted_terminal_value"
                        ]
                    ),
                    "enterprise_value": (
                        optimistic[
                            "enterprise_value"
                        ]
                    ),
                    "terminal_value_percentage": (
                        optimistic[
                            "terminal_value_percentage"
                        ]
                    ),
                },
            },
        }

        # -------------------------------------------------
        # Return primary DCF result
        # -------------------------------------------------

        return DCFResult(

            forecast_cashflows=(
                base["forecasts"]
            ),

            discounted_cashflows=(
                base["discounted_cashflows"]
            ),

            forecast_pv=(
                base["forecast_pv"]
            ),

            terminal_value=(
                base["terminal_value"]
            ),

            discounted_terminal_value=(
                base[
                    "discounted_terminal_value"
                ]
            ),

            enterprise_value=(
                base["enterprise_value"]
            ),

            intrinsic_value=(
                intrinsic_value
            ),

            intrinsic_value_per_share=(
                intrinsic_per_share
            ),

            current_price=current_price,

            margin_of_safety=margin,

            verdict=verdict,

            assumptions=assumptions,
        )

    # -----------------------------------------------------
    # Sensitivity Analysis
    # -----------------------------------------------------

    def _calculate_sensitivity(
        self,
        forecasts,
    ):
        """
        Calculate intrinsic value per share across
        different discount-rate and terminal-growth
        combinations.

        Uses the Base Case forecast cash flows.
        """

        from research.dcf_config import (
            SENSITIVITY_DISCOUNT_RATES,
            SENSITIVITY_TERMINAL_GROWTHS,
        )

        shares = (
            self.snapshot.shares_outstanding
            or 0.0
        )

        cash = (
            self.financials.cash
            or 0.0
        )

        debt = (
            self.financials.total_debt
            or 0.0
        )

        results = {}

        for discount_rate in (
            SENSITIVITY_DISCOUNT_RATES
        ):

            rate_key = (
                f"{discount_rate:.2%}"
            )

            results[rate_key] = {}

            for terminal_growth in (
                SENSITIVITY_TERMINAL_GROWTHS
            ):

                growth_key = (
                    f"{terminal_growth:.2%}"
                )

                # -----------------------------------------
                # Invalid combination
                # -----------------------------------------

                if terminal_growth >= discount_rate:

                    results[rate_key][
                        growth_key
                    ] = None

                    continue

                # -----------------------------------------
                # Forecast PV
                # -----------------------------------------

                forecast_pv = 0.0

                for row in forecasts:

                    pv = (
                        row["fcf"]
                        / (
                            (1 + discount_rate)
                            ** row["year"]
                        )
                    )

                    forecast_pv += pv

                # -----------------------------------------
                # Terminal value
                # -----------------------------------------

                final_fcf = forecasts[-1]["fcf"]

                terminal_value = (
                    final_fcf
                    * (1 + terminal_growth)
                ) / (
                    discount_rate
                    - terminal_growth
                )

                discounted_terminal = (
                    terminal_value
                    / (
                        (1 + discount_rate)
                        ** YEARS
                    )
                )

                # -----------------------------------------
                # Enterprise value
                # -----------------------------------------

                enterprise_value = (
                    forecast_pv
                    + discounted_terminal
                )

                # -----------------------------------------
                # Equity value
                # -----------------------------------------

                intrinsic_value = (
                    enterprise_value
                    + cash
                    - debt
                )

                # -----------------------------------------
                # Per-share value
                # -----------------------------------------

                if shares > 0:

                    intrinsic_per_share = (
                        intrinsic_value
                        / shares
                    )

                else:

                    intrinsic_per_share = 0.0

                results[rate_key][
                    growth_key
                ] = intrinsic_per_share

        return results
