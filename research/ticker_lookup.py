"""
FreedomIQ

Ticker Lookup

Converts company names and portfolio symbols into
Yahoo Finance NSE tickers.
"""

TICKERS = {

    # --------------------------------------------------
    # Company Names
    # --------------------------------------------------

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

    "godrej consumer products": "GODREJCP.NS",

    "unominda": "UNOMINDA.NS",

    "nalco": "NATIONALUM.NS",

    "vbl": "VBL.NS",

    "varun beverages": "VBL.NS",

    "shriram finance": "SHRIRAMFIN.NS",

    "cera": "CERA.NS",

    "adani enterprises": "ADANIENT.NS",

    "adani ports": "ADANIPORTS.NS",

    # --------------------------------------------------
    # Portfolio Symbols
    # --------------------------------------------------

    "reliance": "RELIANCE.NS",
    "infy": "INFY.NS",
    "tcs": "TCS.NS",
    "lt": "LT.NS",
    "ltf": "LTF.NS",
    "icicibank": "ICICIBANK.NS",
    "itc": "ITC.NS",
    "jiofin": "JIOFIN.NS",
    "ashokley": "ASHOKLEY.NS",
    "sunpharma": "SUNPHARMA.NS",
    "godrejcp": "GODREJCP.NS",
    "unominda": "UNOMINDA.NS",
    "nationalum": "NATIONALUM.NS",
    "nalco": "NATIONALUM.NS",
    "vbl": "VBL.NS",
    "shriramfin": "SHRIRAMFIN.NS",
    "cera": "CERA.NS",
    "adanient": "ADANIENT.NS",
    "adaniports": "ADANIPORTS.NS",

    # ETFs

    "mid150bees": "MID150BEES.NS",
    "niftyietf": "NIFTYIETF.NS",

    # Commodities

    "silvercase": "SILVERCASE.NS",

    # Sovereign Gold Bond

    "sgbde31iii-gb": "SGBDE31III-GB.NS",
}


def get_ticker(company_name: str) -> str:
    """
    Convert a company name or portfolio symbol
    into a Yahoo Finance ticker.
    """

    key = company_name.strip().lower()

    # Cash is not a market-traded security.
    if key == "cash":
        return None

    # Already a Yahoo Finance NSE ticker.
    if key.endswith(".ns"):
        return key.upper()

    # Known company name or alias.
    if key in TICKERS:
        return TICKERS[key]

    # Default to NSE.
    return key.upper() + ".NS"