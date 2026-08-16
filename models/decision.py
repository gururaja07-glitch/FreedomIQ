from dataclasses import dataclass


@dataclass
class InvestmentDecision:
    company: str
    decision: str
    fundamental_rating: str
    valuation_view: str
    portfolio_weight: float
    portfolio_risk: str
    confidence: str
    reasons: list[str]
    risks: list[str]