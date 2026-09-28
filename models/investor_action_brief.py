from dataclasses import dataclass


@dataclass
class InvestorActionBrief:
    """
    Daily investor-facing brief built from
    existing FreedomIQ decision context.
    """

    brief_date: str
    portfolio_status: dict
    attention_items: list[dict]
    recent_changes: list[dict]
    persistent_actions: list[dict]
    persistent_opportunities: list[dict]
    persistent_watchpoints: list[dict]
    trends: dict
    summary: str