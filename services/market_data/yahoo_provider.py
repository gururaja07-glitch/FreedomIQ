import yfinance as yf

from services.market_data.base import MarketDataProvider


class YahooMarketDataProvider(MarketDataProvider):
    """Yahoo Finance implementation of the market-data provider."""

    def get_latest_close(self, ticker: str) -> float | None:
        symbol = str(ticker).strip().upper()

        if not symbol:
            return None

        if "." not in symbol:
            symbol = f"{symbol}.NS"

        try:
            data = yf.Ticker(symbol).history(period="1d")

            if data.empty:
                return None

            return round(float(data["Close"].iloc[-1]), 2)

        except Exception:
            return None