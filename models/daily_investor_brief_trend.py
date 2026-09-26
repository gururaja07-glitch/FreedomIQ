from dataclasses import dataclass


@dataclass
class PersistentInvestorBriefItem:
    """
    Represents an item that appears repeatedly across
    multiple Daily Investor Brief snapshots.
    """

    category: str
    title: str
    review_count: int
    consecutive_count: int
    first_seen: str
    last_seen: str
    priority: str


@dataclass
class DailyInvestorBriefTrend:
    """
    Represents historical trend intelligence across
    multiple Daily Investor Brief snapshots.
    """

    review_count: int
    start_date: str
    end_date: str
    health_trend: str
    risk_trend: str
    largest_holding_weight_trend: str
    persistent_actions: list[PersistentInvestorBriefItem]
    persistent_opportunities: list[PersistentInvestorBriefItem]
    persistent_watchpoints: list[PersistentInvestorBriefItem]
    summary: str