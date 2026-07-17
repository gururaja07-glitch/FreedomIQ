def calculate_metrics(df):
    """
    Calculate investment metrics for each holding.
    """

    df["Investment"] = (
        df["Quantity"] * df["BuyPrice"]
    )

    df["Current Value"] = (
        df["Quantity"] * df["CurrentPrice"]
    )

    df["Profit"] = (
        df["Current Value"] -
        df["Investment"]
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


def calculate_portfolio_summary(df):
    """
    Returns overall portfolio statistics.
    """

    investment = df["Investment"].sum()
    current_value = df["Current Value"].sum()
    profit = current_value - investment

    if investment == 0:
        return_percent = 0
    else:
        return_percent = round(
            profit / investment * 100,
            2
        )

    largest = df.loc[
        df["Current Value"].idxmax()
    ]

    summary = {
        "Investment": round(investment, 2),
        "Current Value": round(current_value, 2),
        "Profit": round(profit, 2),
        "Return %": return_percent,
        "Number of Stocks": len(df),
        "Largest Holding": largest["Stock"],
        "Largest Weight": round(
            largest["Weight %"], 2
        ),
    }

    return summary


def calculate_asset_allocation(df):
    """
    Calculate overall asset allocation.
    """

    sector = df["Sector"].astype(str).str.strip().str.lower()

    equity = df[
        ~sector.isin(["gold", "silver", "cash"])
    ]["Current Value"].sum()

    gold = df[
        sector == "gold"
    ]["Current Value"].sum()

    silver = df[
        sector == "silver"
    ]["Current Value"].sum()

    cash = df[
        sector == "cash"
    ]["Current Value"].sum()

    return {
        "Equity": equity,
        "Gold": gold,
        "Silver": silver,
        "Cash": cash,
    }


def calculate_portfolio_insights(df):
    """
    Returns important portfolio insights.
    """

    best = df.loc[df["Return %"].idxmax()]
    worst = df.loc[df["Return %"].idxmin()]
    largest = df.loc[df["Weight %"].idxmax()]

    insights = {
        "Best Performer": best["Stock"],
        "Best Return": round(best["Return %"], 2),

        "Worst Performer": worst["Stock"],
        "Worst Return": round(worst["Return %"], 2),

        "Largest Holding": largest["Stock"],
        "Largest Weight": round(largest["Weight %"], 2),
    }

    return insights


def get_top_performers(df, top_n=3):
    """
    Returns the top performing stocks.
    """

    return (
        df.sort_values(
            by="Return %",
            ascending=False
        )
        .head(top_n)[["Stock", "Return %"]]
        .reset_index(drop=True)
    )


def get_top_losers(df, top_n=3):
    """
    Returns the worst performing stocks.
    """

    return (
        df.sort_values(
            by="Return %",
            ascending=True
        )
        .head(top_n)[["Stock", "Return %"]]
        .reset_index(drop=True)
    )