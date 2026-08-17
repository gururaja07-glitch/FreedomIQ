from services.portfolio_service import get_dashboard_data
from models.portfolio_decision import PortfolioDecision


def get_portfolio_decisions():
    """
    Generate portfolio-level investment decisions.

    Uses the existing FreedomIQ dashboard engines for:
    - Portfolio summary
    - Portfolio health
    - Portfolio risk
    - Rebalancing

    This service does not recalculate portfolio metrics.
    """

    dashboard = get_dashboard_data()

    decisions = []

    summary = dashboard.summary
    health = dashboard.health
    risk = dashboard.risk
    rebalancing = dashboard.rebalancing

    # ------------------------------------------------------
    # 1. Largest holding concentration
    # ------------------------------------------------------

    largest_weight = float(
        summary.get("Largest Weight", 0)
    )

    largest_holding = summary.get(
        "Largest Holding",
        "Unknown",
    )

    if largest_weight > 20:

        decisions.append(
            PortfolioDecision(
                issue="Portfolio concentration is high.",
                reason=(
                    f"{largest_holding} represents "
                    f"{largest_weight:.2f}% "
                    "of the portfolio."
                ),
                action=(
                    "Avoid adding further capital to this "
                    "holding until its portfolio weight "
                    "falls below 20%."
                ),
                priority="Medium",
            )
        )

    # ------------------------------------------------------
    # 2. Top 3 concentration
    # ------------------------------------------------------

    top3 = risk.get("details", {}).get(
        "Top 3 Concentration"
    )

    if top3:

        top3_level, top3_reason = top3

        if top3_level in ["Medium", "High"]:

            decisions.append(
                PortfolioDecision(
                    issue="Top-3 portfolio concentration "
                          "requires attention.",
                    reason=top3_reason,
                    action=(
                        "Direct new investments toward "
                        "underweight holdings and sectors "
                        "rather than increasing the largest "
                        "positions."
                    ),
                    priority=(
                        "High"
                        if top3_level == "High"
                        else "Medium"
                    ),
                )
            )

    # ------------------------------------------------------
    # 3. Sector concentration
    # ------------------------------------------------------

    sector = risk.get("details", {}).get(
        "Sector"
    )

    if sector:

        sector_level, sector_reason = sector

        if sector_level in ["Medium", "High"]:

            decisions.append(
                PortfolioDecision(
                    issue="Sector concentration requires "
                          "attention.",
                    reason=sector_reason,
                    action=(
                        "Avoid increasing exposure to the "
                        "largest sector and direct future "
                        "investments toward underweight sectors."
                    ),
                    priority=(
                        "High"
                        if sector_level == "High"
                        else "Medium"
                    ),
                )
            )

    # ------------------------------------------------------
    # 4. Cash allocation
    # ------------------------------------------------------

    cash = risk.get("details", {}).get(
        "Cash"
    )

    if cash:

        cash_level, cash_reason = cash

        if cash_level == "High":

            decisions.append(
                PortfolioDecision(
                    issue="Cash allocation is low.",
                    reason=cash_reason,
                    action=(
                        "Build cash allocation gradually "
                        "to maintain liquidity and future "
                        "buying capacity."
                    ),
                    priority="Medium",
                )
            )

    # ------------------------------------------------------
    # 5. Portfolio health
    # ------------------------------------------------------

    health_total = float(
        health.get("Total", 0)
    )

    if health_total < 60:

        decisions.append(
            PortfolioDecision(
                issue="Overall portfolio health is weak.",
                reason=(
                    f"Portfolio health score is "
                    f"{health_total:.0f}/100."
                ),
                action=(
                    "Review diversification, concentration "
                    "and asset allocation before making "
                    "additional investments."
                ),
                priority="High",
            )
        )

    elif health_total < 80:

        decisions.append(
            PortfolioDecision(
                issue="Portfolio health can be improved.",
                reason=(
                    f"Portfolio health score is "
                    f"{health_total:.0f}/100."
                ),
                action=(
                    "Improve allocation gradually rather "
                    "than making large portfolio changes."
                ),
                priority="Low",
            )
        )

    # ------------------------------------------------------
    # 6. Rebalancing
    # ------------------------------------------------------

    if rebalancing:

        for item in rebalancing:

            stock = item.get(
                "Stock",
                "Unknown",
            )

            current_weight = item.get(
                "Current Weight",
                0,
            )

            sell_amount = item.get(
                "Sell Amount",
                0,
            )

            decisions.append(
                PortfolioDecision(
                    issue=f"{stock} requires rebalancing.",
                    reason=(
                        f"Current allocation is "
                        f"{current_weight:.2f}%."
                    ),
                    action=(
                        f"Consider reducing the position "
                        f"by approximately "
                        f"{sell_amount:,.0f} "
                        "to restore the target allocation."
                    ),
                    priority="Medium",
                )
            )

    return decisions