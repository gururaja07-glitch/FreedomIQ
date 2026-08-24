from dataclasses import dataclass

from models.decision import InvestmentDecision
from models.portfolio_decision import PortfolioDecision


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
    summary: str
    confidence: str