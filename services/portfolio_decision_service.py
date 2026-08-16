from services.portfolio_service import get_dashboard_data
from models.portfolio_decision import PortfolioDecision


def get_portfolio_decisions():

    dashboard = get_dashboard_data()

    decisions = []

    if dashboard.summary["Largest Weight"] > 20:

        decisions.append(
            PortfolioDecision(
                issue="Portfolio concentration is high.",
                reason=(
                    f"{dashboard.summary['Largest Holding']} "
                    f"represents "
                    f"{dashboard.summary['Largest Weight']:.2f}% "
                    "of the portfolio."
                ),
                action=(
                    "Avoid adding further capital to this holding."
                ),
                priority="Medium",
            )
        )

    return decisions