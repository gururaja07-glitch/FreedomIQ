from dataclasses import dataclass


@dataclass
class PortfolioSnapshot:
    """
    Historical record of FreedomIQ portfolio intelligence
    at a specific point in time.

    Stores existing analysis outputs and does not perform
    any investment analysis itself.
    """

    snapshot_date: str

    portfolio_summary: dict
    portfolio_health: dict
    portfolio_risk: dict

    committee_summary: str
    committee_confidence: str

    quarterly_summary: str
    quarterly_assessment_counts: dict

    company_decisions: list[dict]