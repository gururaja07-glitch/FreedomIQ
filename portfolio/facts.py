"""
FreedomIQ

Module : Facts Engine

Purpose :
Collects objective portfolio facts.

Responsibilities :
- Gather portfolio facts
- Organize portfolio facts
- Return PortfolioFacts

Does NOT:
- Interpret facts
- Generate evidence
- Make investment decisions
- Produce recommendations
"""

from portfolio.models import PortfolioFacts


def collect_portfolio_facts(
    dashboard,
    allocation,
    sector_summary,
) -> PortfolioFacts:
    """
    Collect all portfolio facts.

    No decisions.
    No recommendations.
    No opinions.
    """