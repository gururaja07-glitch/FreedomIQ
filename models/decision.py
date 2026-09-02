from dataclasses import dataclass


@dataclass
class InvestmentDecision:
    company: str

    # Final decision
    decision: str

    # Fundamental / valuation view
    fundamental_rating: str
    valuation_view: str

    # Evidence
    fcf_quality: str
    dcf_verdict: str
    financial_data_quality: str
    evidence_summary: str

    # Portfolio context
    portfolio_weight: float
    portfolio_risk: str

    # Confidence
    confidence: str

    # Latest quarterly evidence
    quarterly_assessment: str
    quarterly_positive_changes: list[str]
    quarterly_negative_changes: list[str]

    # Detailed explanation
    reasons: list[str]
    risks: list[str]
