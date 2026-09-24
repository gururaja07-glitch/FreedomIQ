from dataclasses import dataclass


@dataclass
class DailyInvestorBriefSnapshot:
    """
    Persisted historical snapshot of a Daily Investor Brief.

    This model stores the investor brief exactly as it
    existed for a particular review date.

    It does not perform investment analysis.
    """

    brief_date: str

    portfolio_snapshot: dict

    changes: list[dict]

    persistent_actions: list[dict]

    persistent_opportunities: list[dict]

    watchpoints: list[dict]

    trends: dict

    conclusion: str