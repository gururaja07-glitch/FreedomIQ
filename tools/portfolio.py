import pandas as pd

def get_portfolio():

    df = pd.read_excel("data/holdings.xls")

    df = df.rename(columns={
        "Instrument": "Stock",
        "Qty.": "Quantity",
        "Avg. cost": "BuyPrice",
        "LTP": "CurrentPrice"
    })

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df