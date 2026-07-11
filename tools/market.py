import yfinance as yf

def update_prices(df):

    prices = []

    for _, row in df.iterrows():

        stock = row["Stock"]
        old_price = row["CurrentPrice"]

        try:
            symbol = str(stock).strip().upper() + ".NS"

            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")

            if not data.empty:
                prices.append(round(data["Close"].iloc[-1], 2))
            else:
                prices.append(old_price)

        except Exception:
            prices.append(old_price)

    df["CurrentPrice"] = prices

    return df