TICKERS = {
    "reliance": "RELIANCE.NS",
    "reliance industries": "RELIANCE.NS",

    "infosys": "INFY.NS",

    "tcs": "TCS.NS",

    "lt": "LT.NS",
    "l&t": "LT.NS",
    "larsen and toubro": "LT.NS",

    "l&t finance": "LTF.NS",
    "lt finance": "LTF.NS",

    "icici bank": "ICICIBANK.NS",

    "hdfc bank": "HDFCBANK.NS",

    "itc": "ITC.NS",

    "jio financial": "JIOFIN.NS",

    "ashok leyland": "ASHOKLEY.NS",

    "sun pharma": "SUNPHARMA.NS",

    "godrej consumer": "GODREJCP.NS",

    "unominda": "UNOMINDA.NS",

    "nalco": "NATIONALUM.NS",

    "vbl": "VBL.NS",
}


def get_ticker(company_name: str) -> str:
    """
    Convert a company name into an NSE ticker.
    """

    key = company_name.strip().lower()

    return TICKERS.get(key, company_name.upper())