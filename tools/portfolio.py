from pathlib import Path
import pandas as pd

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Absolute path to holdings file
HOLDINGS_FILE = PROJECT_ROOT / "data" / "holdings.xls"


def get_portfolio():

    df = pd.read_excel(HOLDINGS_FILE)

    df = df.rename(columns={
        "Instrument": "Stock",
        "Qty.": "Quantity",
        "Avg. cost": "BuyPrice",
        "LTP": "CurrentPrice"
    })

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df