from dataclasses import dataclass, field
from typing import List


@dataclass
class CompanySnapshot:
    company: str
    ticker: str
    sector: str
    industry: str
    market_cap: str


@dataclass
class FinancialSummary:
    revenue_growth: str
    profit_growth: str
    roe: str
    roce: str
    debt_equity: str
    operating_margin: str


@dataclass
class ValuationSummary:
    pe: str
    pb: str
    ev_ebitda: str
    peg: str
    valuation: str


@dataclass
class CompanyAnalysis:
    snapshot: CompanySnapshot
    financials: FinancialSummary
    valuation: ValuationSummary

    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    growth_drivers: List[str] = field(default_factory=list)

    recommendation: str = ""
    confidence: str = ""