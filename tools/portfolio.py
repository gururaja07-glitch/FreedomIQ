from pathlib import Path
import pandas as pd

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Absolute path to holdings file
HOLDINGS_FILE = PROJECT_ROOT / "data" / "holdings.xls"

REQUIRED_COLUMNS = {
    "Instrument": "Stock",
    "Qty.": "Quantity",
    "Avg. cost": "BuyPrice",
    "LTP": "CurrentPrice",
}


def get_portfolio() -> pd.DataFrame:
    """
    Load and validate the portfolio holdings.

    Returns
    -------
    pandas.DataFrame
        Standardized portfolio dataframe.
    """

    if not HOLDINGS_FILE.exists():
        raise FileNotFoundError(
            f"Holdings file not found:\n{HOLDINGS_FILE}"
        )

    df = pd.read_excel(HOLDINGS_FILE)

    # Remove empty columns created by Excel exports
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Validate required columns
    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )

    # Standardize column names
    df = df.rename(columns=REQUIRED_COLUMNS)

    # Keep only required columns
    df = df[list(REQUIRED_COLUMNS.values())].copy()

    # Clean data
    df["Stock"] = df["Stock"].astype(str).str.strip()

    numeric_columns = [
        "Quantity",
        "BuyPrice",
        "CurrentPrice",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove invalid rows
    df = df.dropna(
        subset=[
            "Stock",
            "Quantity",
            "BuyPrice",
            "CurrentPrice",
        ]
    )

    # Derived metrics
    df["InvestedValue"] = df["Quantity"] * df["BuyPrice"]
    df["CurrentValue"] = df["Quantity"] * df["CurrentPrice"]
    df["ProfitLoss"] = df["CurrentValue"] - df["InvestedValue"]
    df["ReturnPct"] = (
        df["ProfitLoss"] / df["InvestedValue"] * 100
    ).round(2)

    total_value = df["CurrentValue"].sum()

    if total_value > 0:
        df["WeightPct"] = (
            df["CurrentValue"] / total_value * 100
        ).round(2)
    else:
        df["WeightPct"] = 0.0

    df = df.sort_values(
        by="CurrentValue",
        ascending=False,
    ).reset_index(drop=True)

    return df