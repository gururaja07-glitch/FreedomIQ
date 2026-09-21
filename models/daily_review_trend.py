from dataclasses import dataclass


@dataclass
class PersistentReviewItem:
    """
    Represents a review item that appears repeatedly
    across the historical daily review window.
    """

    category: str

    title: str

    review_count: int

    consecutive_count: int

    first_seen: str

    last_seen: str

    priority: str


@dataclass
class DailyReviewTrend:
    """
    Historical trend analysis across persisted
    FreedomIQ daily portfolio reviews.

    This model contains historical observations only.
    It does not perform prediction or investment analysis.
    """

    review_count: int

    start_date: str

    end_date: str

    health_trend: str

    risk_trend: str

    largest_holding_weight_trend: str

    persistent_actions: list[PersistentReviewItem]

    persistent_opportunities: list[PersistentReviewItem]

    persistent_watchpoints: list[PersistentReviewItem]

    summary: str