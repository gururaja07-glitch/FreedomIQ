from dataclasses import dataclass

from models.decision import InvestmentDecision
from models.portfolio_decision import PortfolioDecision
from models.portfolio_action import PortfolioAction


@dataclass
class PortfolioCommitteeResult:
    """
    Structured portfolio-level investment committee result.

    Combines:
    - Individual company investment decisions
    - Existing portfolio-level decisions
    - Overall portfolio synthesis
    """

    company_decisions: list[InvestmentDecision]
    portfolio_actions: list[PortfolioDecision]
    prioritized_actions: list[PortfolioAction]
    summary: str
    confidence: str
    quarterly_assessment_counts: dict[str, int]
    quarterly_summary: str