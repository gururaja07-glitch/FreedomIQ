"""
FreedomIQ

Portfolio Service

This module orchestrates all portfolio-related workflows.

It acts as the bridge between the UI and the core modules.
"""

from models.dashboard import DashboardData

from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import (
    calculate_metrics,
    calculate_portfolio_summary,
    calculate_asset_allocation,
    calculate_portfolio_insights,
    get_top_performers,
    get_top_losers,
)
from tools.health import calculate_portfolio_health
from tools.risk import calculate_portfolio_risk
from tools.advisor import generate_portfolio_advice
from tools.rebalance import calculate_rebalancing


def get_dashboard_data() -> DashboardData:
    """
    Load and prepare all dashboard data.
    """

    df = get_portfolio()
    df = update_prices(df)
    df = calculate_metrics(df)

    summary = calculate_portfolio_summary(df)
    allocation = calculate_asset_allocation(df)
    insights = calculate_portfolio_insights(df)

    top_performers = get_top_performers(df)
    top_losers = get_top_losers(df)

    health = calculate_portfolio_health(df, allocation)
    risk, overall_risk = calculate_portfolio_risk(df, allocation)

    advisor = generate_portfolio_advice(df, allocation)
    rebalancing = calculate_rebalancing(df)

    return DashboardData(
        portfolio=df,
        summary=summary,
        allocation=allocation,
        insights=insights,
        health=health,
        risk={
            "details": risk,
            "overall": overall_risk,
        },
        advisor=advisor,
        rebalancing=rebalancing,
        top_performers=top_performers,
        top_losers=top_losers,
    )