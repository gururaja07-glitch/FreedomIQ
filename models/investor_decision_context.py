from dataclasses import dataclass


@dataclass
class InvestorDecisionContext:
    """
    Consolidated decision context built from
    existing Daily Investor Brief intelligence.
    """

    context_date: str
    portfolio_status: dict
    recent_changes: list[dict]
    persistent_actions: list[dict]
    persistent_opportunities: list[dict]
    persistent_watchpoints: list[dict]
    trends: dict
    key_context: list[dict]
