"""
FreedomIQ

Module : Portfolio Advisor

Purpose :
Provides portfolio recommendations.

Author : Gururaj N K
Version : 0.1
"""

from tools.rules import (
    MAX_STOCK_WEIGHT,
    MAX_SECTOR_WEIGHT,
    TARGET_CASH_WEIGHT,
    TARGET_GOLD_WEIGHT,
)


def get_stock_recommendations(df):
    """
    Stock weight recommendations.
    """

    recommendations = []

    for _, row in df.iterrows():

        if row["Weight %"] > MAX_STOCK_WEIGHT:

            recommendations.append({
                "Category": "Stock",
                "Priority": "High",
                "Recommendation":
                    f"Reduce {row['Stock']} "
                    f"({row['Weight %']:.1f}%)."
            })

    return recommendations


def get_sector_recommendations(df):
    """
    Sector recommendations.
    """

    recommendations = []

    sector_weight = (
        df.groupby("Sector")["Weight %"]
        .sum()
    )

    for sector, weight in sector_weight.items():

        if weight > MAX_SECTOR_WEIGHT:

            recommendations.append({
                "Category": "Sector",
                "Priority": "Medium",
                "Recommendation":
                    f"Reduce exposure to {sector} "
                    f"({weight:.1f}%)."
            })

    return recommendations


def get_cash_recommendation(allocation):
    """
    Cash recommendation.
    """

    recommendations = []

    total = sum(allocation.values())

    cash_weight = allocation["Cash"] / total * 100

    if cash_weight > TARGET_CASH_WEIGHT + 5:

        recommendations.append({
            "Category": "Cash",
            "Priority": "Low",
            "Recommendation":
                f"Deploy excess cash "
                f"({cash_weight:.1f}%)."
        })

    return recommendations


def get_gold_recommendation(allocation):
    """
    Gold recommendation.
    """

    recommendations = []

    total = sum(allocation.values())

    gold_weight = allocation["Gold"] / total * 100

    if gold_weight < TARGET_GOLD_WEIGHT:

        recommendations.append({
            "Category": "Gold",
            "Priority": "Medium",
            "Recommendation":
                f"Increase Gold allocation "
                f"({gold_weight:.1f}%)."
        })

    return recommendations


def generate_portfolio_advice(df, allocation):
    """
    Generate advisor recommendations.
    """

    recommendations = []

    recommendations.extend(
        get_stock_recommendations(df)
    )

    recommendations.extend(
        get_sector_recommendations(df)
    )

    recommendations.extend(
        get_cash_recommendation(allocation)
    )

    recommendations.extend(
        get_gold_recommendation(allocation)
    )

    return recommendations