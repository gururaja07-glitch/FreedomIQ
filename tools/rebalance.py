"""
FreedomIQ

Module : Rebalancing Engine

Purpose :
Calculates portfolio rebalancing suggestions.

Author : Gururaj N K
Version : 0.1
"""

from tools.rules import MAX_STOCK_WEIGHT


def calculate_rebalancing(df):
    """
    Calculate stock rebalancing suggestions.
    """

    recommendations = []

    portfolio_value = df["Current Value"].sum()

    for _, row in df.iterrows():

        current_weight = row["Weight %"]

        if current_weight <= MAX_STOCK_WEIGHT:
            continue

        target_value = (
            MAX_STOCK_WEIGHT / 100
        ) * portfolio_value

        amount_to_sell = (
            row["Current Value"] - target_value
        )

        recommendations.append({
            "Stock": row["Stock"],
            "Current Weight": round(current_weight, 2),
            "Target Weight": MAX_STOCK_WEIGHT,
            "Sell Amount": round(amount_to_sell, 2)
        })

    return recommendations