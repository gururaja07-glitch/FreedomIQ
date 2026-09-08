from dataclasses import dataclass


@dataclass
class PortfolioChange:
    """
    Represents one meaningful change detected
    between two portfolio snapshots.
    """

    category: str

    company: str | None

    previous_value: str
    current_value: str

    priority: str

    description: str


@dataclass
class PortfolioChangeResult:
    """
    Complete result of comparing two
    portfolio snapshots.
    """

    previous_date: str | None

    current_date: str

    changes: list[PortfolioChange]

    summary: str