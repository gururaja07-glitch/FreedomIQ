from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HOLDINGS_FILE = PROJECT_ROOT / "data" / "holdings.xls"

REQUIRED_COLUMNS = {
    "Instrument": "Stock",
    "Qty.": "Quantity",
    "Avg. cost": "BuyPrice",
    "LTP": "CurrentPrice",
}


def get_portfolio():
    if not HOLDINGS_FILE.exists():
        raise FileNotFoundError(f"Holdings file not found: {HOLDINGS_FILE}")

    df = pd.read_excel(HOLDINGS_FILE)

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.rename(columns=REQUIRED_COLUMNS)

    df["InvestedValue"] = df["Quantity"] * df["BuyPrice"]
    df["CurrentValue"] = df["Quantity"] * df["CurrentPrice"]
    df["ProfitLoss"] = df["CurrentValue"] - df["InvestedValue"]
    df["ReturnPct"] = (
        df["ProfitLoss"] / df["InvestedValue"] * 100
    ).round(2)

    total = df["CurrentValue"].sum()
    df["WeightPct"] = df["CurrentValue"] / total * 100

    return df