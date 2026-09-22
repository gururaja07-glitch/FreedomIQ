from dataclasses import dataclass


@dataclass
class DailyInvestorBrief:
    """
    Consolidated daily investor brief.

    This model contains existing portfolio intelligence
    assembled into a single investor-facing view.
    It does not perform new investment analysis.
    """

    brief_date: str

    portfolio_snapshot: dict

    changes: list[dict]

    persistent_actions: list[dict]

    persistent_opportunities: list[dict]

    watchpoints: list[dict]

    trends: dict

    conclusion: str