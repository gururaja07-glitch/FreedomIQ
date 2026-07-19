from dataclasses import dataclass
from typing import Any


@dataclass
class DashboardData:
    """Container for all dashboard data."""

    portfolio: Any
    summary: Any
    allocation: Any
    insights: Any
    health: Any
    risk: Any
    advisor: Any
    rebalancing: Any
    top_performers: Any
    top_losers: Any