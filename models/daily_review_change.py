from dataclasses import dataclass


@dataclass
class DailyReviewChange:
    """
    Represents one meaningful change between
    two persisted daily portfolio reviews.
    """

    category: str

    title: str

    previous_value: str

    current_value: str

    priority: str

    description: str


@dataclass
class DailyReviewChangeResult:
    """
    Complete result of comparing two
    daily portfolio reviews.
    """

    previous_date: str | None

    current_date: str

    changes: list[DailyReviewChange]

    summary: str