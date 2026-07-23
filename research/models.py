from dataclasses import dataclass


# ==========================================================
# Company Snapshot
# ==========================================================

@dataclass
class CompanySnapshot:
    company: str
    ticker: str
    sector: str
    industry: str
    market_cap: str


# ==========================================================
# Financial Summary
# ==========================================================

@dataclass
class FinancialSummary:
    revenue_growth: str
    profit_growth: str
    roe: str
    roce: str
    debt_equity: str
    operating_margin: str


# ==========================================================
# Valuation Summary
# ==========================================================

@dataclass
class ValuationSummary:
    pe: str
    pb: str
    ev_ebitda: str
    peg: str
    valuation: str


# ==========================================================
# Investment Score
# ==========================================================

@dataclass
class InvestmentScore:
    valuation: int
    growth: int
    profitability: int
    financial_strength: int
    business_quality: int

    total: int
    stars: str
    rating: str

    reasons: list[str]


# ==========================================================
# Complete Company Analysis
# ==========================================================

@dataclass
class CompanyAnalysis:
    snapshot: CompanySnapshot
    financials: FinancialSummary
    valuation: ValuationSummary

    score: InvestmentScore

    strengths: list[str]
    weaknesses: list[str]
    risks: list[str]
    growth_drivers: list[str]

    confidence: str


# ==========================================================
# Research Report
# ==========================================================

@dataclass
class ResearchReport:
    """Structured research report."""

    snapshot: CompanySnapshot
    financials: FinancialSummary
    valuation: ValuationSummary

    score: InvestmentScore

    strengths: list[str]
    weaknesses: list[str]
    risks: list[str]
    growth_drivers: list[str]

    confidence: str