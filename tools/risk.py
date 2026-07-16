"""
FreedomIQ

Module : Risk

Purpose :
Identifies portfolio risks.

Author : Gururaj N K
Version : 0.1
"""
from tools.portfolio_utils import (
    calculate_largest_holding,
    calculate_sector_weights,
)
from tools.rules import (
    MAX_SECTOR_WEIGHT,
    MAX_STOCK_WEIGHT,
    TARGET_CASH_WEIGHT,
    TARGET_GOLD_WEIGHT,
)


def calculate_concentration_risk(df):

    largest_holding = calculate_largest_holding(df)

    stock = largest_holding["Stock"]

    weight = largest_holding["Weight %"]

    if weight <= MAX_STOCK_WEIGHT:

        return (
            "Low",
            f"{stock} is within the "
            f"{MAX_STOCK_WEIGHT}% limit."
        )

    excess = weight - MAX_STOCK_WEIGHT

    return (
        "High",
        f"{stock} exceeds the limit "
        f"by {excess:.2f}%."
    )


def calculate_sector_risk(df):

    sector_weights = calculate_sector_weights(df)

    sector = sector_weights.idxmax()

    weight = sector_weights.max()

    if weight <= MAX_SECTOR_WEIGHT:

        return (
            "Low",
            f"{sector} sector is within limit."
        )

    excess = weight - MAX_SECTOR_WEIGHT

    return (
        "High",
        f"{sector} sector exceeds the limit "
        f"by {excess:.2f}%."
    )


def calculate_cash_risk(cash_weight):

    if cash_weight >= TARGET_CASH_WEIGHT:

        return (
            "Low",
            f"Cash allocation is healthy ({cash_weight:.2f}%)."
        )

    shortage = TARGET_CASH_WEIGHT - cash_weight

    return (
        "High",
        f"Cash allocation is below target by {shortage:.2f}%."
    )


def calculate_gold_risk(gold_weight):

    if gold_weight >= TARGET_GOLD_WEIGHT:

        return (
            "Low",
            f"Gold allocation is healthy ({gold_weight:.2f}%)."
        )

    shortage = TARGET_GOLD_WEIGHT - gold_weight

    return (
        "High",
        f"Gold allocation is below target by {shortage:.2f}%."
    )


def calculate_risk(df, cash_weight, gold_weight):

    concentration = calculate_concentration_risk(df)

    sector = calculate_sector_risk(df)

    cash = calculate_cash_risk(cash_weight)

    gold = calculate_gold_risk(gold_weight)

    risk = {
        "Concentration": concentration,
        "Sector": sector,
        "Cash": cash,
        "Gold": gold
    }

    return risk


def print_risk(risk):

    print()
    print("=" * 50)
    print("PORTFOLIO RISK")
    print("=" * 50)

    for category, (level, message) in risk.items():

        print(f"{category:<15} : {level}")
        print(f"   {message}")
        print()

    print("=" * 50)