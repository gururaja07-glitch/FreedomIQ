"""
FreedomIQ

Module : Portfolio Models

Purpose :
Contains all portfolio data models.

Author : Gururaj N K
Version : 1.0
"""

from dataclasses import dataclass


@dataclass
class InvestmentDecision:
    """
    Represents a portfolio investment decision.
    """

    issue: str
    reason: str
    action: str
    priority: str

@dataclass
class PortfolioScore:

    diversification: int
    concentration: int
    profitability: int

    overall: int

    rating: str
    stars: str


@dataclass
class PortfolioMetrics:
    top5_weight: float
    top10_weight: float

    largest_holding: str
    largest_weight: float

    diversification_score: int

@dataclass
class PortfolioSummary:
    total_invested: float
    total_value: float
    total_profit: float
    total_return: float

    largest_holding: str
    largest_holding_weight: float

    number_of_holdings: int

@dataclass
class PortfolioDashboard:
    summary: object
    metrics: object
    score: object
    advice: list[str]
    decisions: list