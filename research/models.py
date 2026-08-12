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

    cash: float | None = None

    total_debt: float | None = None

    fcf_history: list | None = None


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


@dataclass
class ConfidenceSummary:
    stars: str
    level: str
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

    dcf: DCFResult | None = None

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

    confidence: ConfidenceSummary

    dcf: DCFResult | None = None


# ==========================================================
# DCF Result
# ==========================================================

@dataclass
class DCFResult:

    # Forecast
    forecast_cashflows: list

    # Discounted yearly cash flows
    discounted_cashflows: list

    # Present value of forecast period
    forecast_pv: float

    # Terminal value
    terminal_value: float

    discounted_terminal_value: float

    # Enterprise valuation
    enterprise_value: float

    # Equity valuation
    intrinsic_value: float

    intrinsic_value_per_share: float

    current_price: float

    margin_of_safety: float

    verdict: str

    assumptions: dict | None = None

    status: str = "Available"

    reason: str = ""

# ==========================================================
# DCF Valuation (Final Report)
# ==========================================================

