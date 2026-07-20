import yfinance as yf

from research.models import (
    CompanyAnalysis,
    CompanySnapshot,
    FinancialSummary,
    ValuationSummary,
)
from research.ticker_lookup import get_ticker


def analyze_company(company_name: str) -> CompanyAnalysis:
    """
    Returns a structured company analysis using yfinance.
    """

    ticker_symbol = get_ticker(company_name)
    print(f"Input: {company_name}")
    print(f"Resolved Ticker: {ticker_symbol}")

    ticker = yf.Ticker(ticker_symbol)

    try:
        info = ticker.info
        print(f"Fields Returned: {len(info)}")
    except Exception as e:
        print(f"Error: {e}")
        info = {}

    snapshot = CompanySnapshot(
        company=info.get("longName", company_name),
        ticker=info.get("symbol", ticker_symbol),
        sector=info.get("sector", "Unknown"),
        industry=info.get("industry", "Unknown"),
        market_cap=str(info.get("marketCap", "Unknown")),
    )

    financials = FinancialSummary(
        revenue_growth="N/A",
        profit_growth="N/A",
        roe=str(info.get("returnOnEquity", "N/A")),
        roce="N/A",
        debt_equity=str(info.get("debtToEquity", "N/A")),
        operating_margin=str(info.get("operatingMargins", "N/A")),
    )

    valuation = ValuationSummary(
        pe=str(info.get("trailingPE", "N/A")),
        pb=str(info.get("priceToBook", "N/A")),
        ev_ebitda="N/A",
        peg=str(info.get("pegRatio", "N/A")),
        valuation="Pending",
    )

    analysis = CompanyAnalysis(
        snapshot=snapshot,
        financials=financials,
        valuation=valuation,
        strengths=[],
        weaknesses=[],
        risks=[],
        growth_drivers=[],
        recommendation="Analysis in Progress",
        confidence="Medium",
    )

    return analysis