def calculate_largest_holding(df):

    largest_holding = df.sort_values(
        "Weight %",
        ascending=False
    ).iloc[0]

    return largest_holding

def calculate_sector_weights(df):

    sector_weights = (
        df.groupby("Sector")["Weight %"]
        .sum()
        .sort_values(ascending=False)
    )

    return sector_weights

def calculate_total_portfolio(
    current_value,
    cash,
    gold
):

    return current_value + cash + gold

def calculate_cash_weight(
    cash,
    total_portfolio
):

    return cash / total_portfolio * 100


def calculate_gold_weight(
    gold,
    total_portfolio
):

    return gold / total_portfolio * 100

