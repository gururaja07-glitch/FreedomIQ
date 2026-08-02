from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portfolio.dashboard import PortfolioDashboard


@dataclass
class Decision:
    issue: str
    reason: str
    action: str
    priority: str


def generate_decisions(
    dashboard: "PortfolioDashboard",
) -> list[Decision]:
    """
    Generate portfolio decisions.
    """

    decisions = []

    summary = dashboard.summary
    metrics = dashboard.metrics

    # ------------------------------------
    # Concentration
    # ------------------------------------

    if metrics.largest_weight > 20:

        decisions.append(

            Decision(

                issue="Portfolio concentration is high.",

                reason=(
                    f"{metrics.largest_holding} represents "
                    f"{metrics.largest_weight:.2f}% "
                    "of the portfolio."
                ),

                action=(
                    "Avoid adding further capital to this "
                    "holding. Direct future investments "
                    "towards underweight sectors until "
                    "allocation falls below 20%."
                ),

                priority="Medium",
            )
        )

    # ------------------------------------
    # Diversification
    # ------------------------------------

    if summary.number_of_holdings < 15:

        decisions.append(

            Decision(

                issue="Portfolio diversification is limited.",

                reason=(
                    f"Portfolio contains only "
                    f"{summary.number_of_holdings} holdings."
                ),

                action=(
                    "Increase the number of quality holdings "
                    "over time."
                ),

                priority="High",
            )
        )

    # ------------------------------------
    # Performance
    # ------------------------------------

    if summary.total_return > 30:

        decisions.append(

            Decision(

                issue="Portfolio performance is strong.",

                reason=(
                    f"Overall return is "
                    f"{summary.total_return:.2f}%."
                ),

                action=(
                    "Avoid unnecessary trading. "
                    "Continue long-term investing."
                ),

                priority="Low",
            )
        )

    return decisions
