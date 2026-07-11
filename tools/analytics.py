def calculate_metrics(df):

    df["Investment"] = df["Quantity"] * df["BuyPrice"]

    df["Current Value"] = (
        df["Quantity"] * df["CurrentPrice"]
    )

    df["Profit"] = (
        df["Current Value"] - df["Investment"]
    )

    df["Return %"] = (
        df["Profit"] /
        df["Investment"] * 100
    ).round(2)

    df["Weight %"] = (
        df["Current Value"] /
        df["Current Value"].sum() * 100
    ).round(2)

    return df