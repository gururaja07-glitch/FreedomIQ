from dataclasses import dataclass


@dataclass
class DailyReviewItem:
    """
    One item surfaced by the daily portfolio review.
    """

    title: str
    priority: str
    description: str


@dataclass
class DailyPortfolioReview:
    """
    Structured daily portfolio review.

    This model contains only information assembled
    from existing FreedomIQ intelligence engines.
    """

    review_date: str
    portfolio_status: dict
    changes: list[DailyReviewItem]
    actions: list[DailyReviewItem]
    opportunities: list[DailyReviewItem]
    watchpoints: list[DailyReviewItem]
    conclusion: str