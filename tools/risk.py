"""
FreedomIQ

Module : Risk Engine

Purpose :
Calculates Portfolio Risk.

Author : Gururaj N K
Version : 0.1
"""

from tools.rules import (
    MAX_STOCK_WEIGHT,
    MAX_SECTOR_WEIGHT,
    MAX_TOP3_WEIGHT,
    TARGET_CASH_WEIGHT,
)

def calculate_concentration_risk(df):
    """
    Risk based on largest stock weight.
    """

    largest = df["Weight %"].max()

    if largest <= MAX_STOCK_WEIGHT:
        return (
            "Low",
            f"Largest holding is {largest:.1f}%."
        )

    if largest <= MAX_STOCK_WEIGHT + 10:
        return (
            "Medium",
            f"Largest holding is {largest:.1f}%."
        )

    return (
        "High",
        f"Largest holding is {largest:.1f}%."
    )
def calculate_top3_concentration(df):
    """
    Risk based on combined weight of the top 3 holdings.
    """

    top3_weight = (
        df["Weight %"]
        .sort_values(ascending=False)
        .head(3)
        .sum()
    )

    if top3_weight <= MAX_TOP3_WEIGHT:
        return (
            "Low",
            f"Top 3 holdings account for {top3_weight:.1f}%."
        )

    if top3_weight <= MAX_TOP3_WEIGHT + 10:
        return (
            "Medium",
            f"Top 3 holdings account for {top3_weight:.1f}%."
        )

    return (
        "High",
        f"Top 3 holdings account for {top3_weight:.1f}%."
    )

def calculate_sector_risk(df):
    """
    Risk based on largest sector exposure.
    """

    sector_weight = (
        df.groupby("Sector")["Weight %"]
        .sum()
        .max()
    )

    if sector_weight <= MAX_SECTOR_WEIGHT:
        return (
            "Low",
            f"Largest sector exposure is {sector_weight:.1f}%."
        )

    if sector_weight <= MAX_SECTOR_WEIGHT + 10:
        return (
            "Medium",
            f"Largest sector exposure is {sector_weight:.1f}%."
        )

    return (
        "High",
        f"Largest sector exposure is {sector_weight:.1f}%."
    )


def calculate_cash_risk(allocation):
    """
    Risk based on available cash.
    """

    total = sum(allocation.values())

    if total == 0:
        return (
            "High",
            "Cash allocation unavailable."
        )

    cash_weight = allocation["Cash"] / total * 100

    if cash_weight >= TARGET_CASH_WEIGHT:
        return (
            "Low",
            f"Cash allocation is {cash_weight:.1f}%."
        )

    if cash_weight >= TARGET_CASH_WEIGHT / 2:
        return (
            "Medium",
            f"Cash allocation is {cash_weight:.1f}%."
        )

    return (
        "High",
        f"Cash allocation is {cash_weight:.1f}%."
    )


def calculate_portfolio_risk(df, allocation):
    """
    Calculate portfolio risk summary.
    """
    concentration = calculate_concentration_risk(df)
    top3 = calculate_top3_concentration(df)
    sector = calculate_sector_risk(df)
    cash = calculate_cash_risk(allocation)

    levels = [
        concentration[0],
        top3[0],
        sector[0],
        cash[0],
    ]

    if "High" in levels:
        overall = "🔴 High"
    elif "Medium" in levels:
        overall = "🟡 Medium"
    else:
        overall = "🟢 Low"

    return (
        {
            "Concentration": concentration,
            "Top 3 Concentration": top3,
            "Sector": sector,
            "Cash": cash,
        },
        overall,
    )
