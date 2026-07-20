import yfinance as yf

ticker = yf.Ticker("RELIANCE.NS")

try:
    info = ticker.info

    print("Number of fields:", len(info))
    print("=" * 50)

    for key in ["longName", "symbol", "sector", "industry", "marketCap", "trailingPE"]:
        print(f"{key}: {info.get(key)}")

except Exception as e:
    print("ERROR:", e)