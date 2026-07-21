import yfinance as yf

from research.models import CompanySnapshot
from research.ticker_lookup import get_ticker


def get_company_snapshot(company_name: str):
    """
    Returns the company snapshot and raw Yahoo Finance info.
    """

    ticker_symbol = get_ticker(company_name)

    ticker = yf.Ticker(ticker_symbol)

    info = ticker.info

    snapshot = CompanySnapshot(
        company=info.get("longName", company_name),
        ticker=info.get("symbol", ticker_symbol),
        sector=info.get("sector", "Unknown"),
        industry=info.get("industry", "Unknown"),
        market_cap=str(info.get("marketCap", "Unknown")),
    )

    return snapshot, info