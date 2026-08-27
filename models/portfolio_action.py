from dataclasses import dataclass


@dataclass
class PortfolioAction:
    """
    Represents one prioritized portfolio action.

    This model does not calculate investment decisions.
    It represents the action priority derived from
    existing committee decisions.
    """

    priority: str
    company: str
    action: str
    reason: str
    evidence: str