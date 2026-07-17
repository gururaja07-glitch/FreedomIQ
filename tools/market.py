import yfinance as yf


def update_prices(df):

    prices = []

    for _, row in df.iterrows():

        stock = row["Stock"]
        sector = str(row["Sector"]).strip().lower()
        old_price = row["CurrentPrice"]

        # Skip assets that don't have Yahoo Finance quotes
        if sector in ["gold", "silver", "cash"]:
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