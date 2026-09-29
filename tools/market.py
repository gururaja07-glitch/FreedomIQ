from services.market_data.yahoo_provider import YahooMarketDataProvider


NON_QUOTED_SECTORS = {"gold", "silver", "cash"}

market_data_provider = YahooMarketDataProvider()


def update_price(
    stock: str,
    current_price: float,
    *,
    sector: str | None = None,
    ticker: str | None = None,
) -> float:
    """Return the latest closing price, or the last known price on failure.

    ``ticker`` is preferred because portfolio enrichment already resolves
    company names such as ``ICICI Bank`` to their Yahoo Finance symbols.
    """
    if str(sector or "").strip().lower() in NON_QUOTED_SECTORS:
        return current_price

    symbol = str(ticker or stock).strip().upper()

    if not symbol:
        return current_price

    if "." not in symbol:
        symbol = f"{symbol}.NS"

    latest_price = market_data_provider.get_latest_close(symbol)

    if latest_price is None:
        print(f"Price not found for {stock}. Using previous price.")
        return current_price

    return latest_price


def update_prices(df):
    """Update the ``CurrentPrice`` column for every quoted holding."""
    prices = []

    for _, row in df.iterrows():
        prices.append(
            update_price(
                row["Stock"],
                row["CurrentPrice"],
                sector=row.get("Sector"),
                ticker=row.get("Ticker"),
            )
        )

    df["CurrentPrice"] = prices
    return df
