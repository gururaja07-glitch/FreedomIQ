import yfinance as yf

def update_prices(df):

    prices = []

    for _, row in df.iterrows():

        stock = row["Stock"]
        old_price = row["CurrentPrice"]

        # Skip Sovereign Gold Bonds
        if stock.upper().startswith("SGB"):
            prices.append(old_price)
            continue

        symbol = stock.strip().upper() + ".NS"

        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")

            if data.empty:
                print(f"⚠ Price not found for {stock}. Using previous price.")
                prices.append(old_price)
            else:
                latest_price = round(data["Close"].iloc[-1], 2)
                prices.append(latest_price)

        except Exception as e:
            print(f"⚠ Error updating {stock}: {e}")
            prices.append(old_price)

    df["CurrentPrice"] = prices

    return df