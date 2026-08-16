from dataclasses import dataclass


@dataclass
class PortfolioDecision:
    """
    Represents a portfolio-level investment decision.
    """

    issue: str
    reason: str
    action: str
    priority: str