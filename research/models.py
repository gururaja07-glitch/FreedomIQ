from dataclasses import dataclass


# ==========================================================
# Company Snapshot
# ==========================================================

@dataclass
class Snapshot:
    company: str
    ticker: str
    sector: str
    industry: str
    market_cap: str

    current_price: float | None = None
    shares_outstanding: float | None = None


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

    free_cash_flow: float | None = None


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
    snapshot: Snapshot
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
    snapshot: Snapshot
    financials: FinancialSummary
    valuation: ValuationSummary

    score: InvestmentScore

    summary: str
    investment_thesis: str

    strengths: list[str]
    weaknesses: list[str]
    risks: list[str]
    growth_drivers: list[str]

    confidence: str


# ==========================================================
# DCF Valuation
# ==========================================================

@dataclass
class DCFValuation:
    intrinsic_value: str
    current_price: str
    margin_of_safety: str
    verdict: str