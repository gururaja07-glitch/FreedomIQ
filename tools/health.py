"""
FreedomIQ

Module : Health Engine

Purpose :
Calculates Portfolio Health Score.

Author : Gururaj N K
Version : 0.1
"""

from tools.rules import (
    MIN_STOCKS,
    MIN_SECTORS,
    MAX_STOCK_WEIGHT,
    TARGET_CASH_WEIGHT,
    TARGET_GOLD_WEIGHT,
    MAX_GOLD,
)


def calculate_diversification_score(df):
    """
    Score based on number of holdings.
    """

    stocks = len(df)

    if stocks >= MIN_STOCKS:
        return 20

    return round((stocks / MIN_STOCKS) * 20)


def calculate_sector_score(df):
    """
    Score based on number of sectors.
    """

    sectors = df["Sector"].nunique()

    if sectors >= MIN_SECTORS:
        return 20

    return round((sectors / MIN_SECTORS) * 20)


def calculate_stock_concentration_score(df):
    """
    Score based on largest holding.
    """
def calculate_stock_concentration_score(df):
    """
    Score based on largest holding.
    """

    largest = df["Weight %"].max()

    if largest <= 10:
        return 20
    elif largest <= 15:
        return 18
    elif largest <= 20:
        return 15
    elif largest <= 25:
        return 10
    elif largest <= 30:
        return 5

    return 0

    return score


def calculate_cash_score(allocation):
    """
    Score based on cash allocation.
    """

    total = sum(allocation.values())

    if total == 0:
        return 0

    cash_weight = allocation["Cash"] / total * 100

    if cash_weight >= TARGET_CASH_WEIGHT:
        return 20

    return round(cash_weight / TARGET_CASH_WEIGHT * 20)


def calculate_gold_score(allocation):
    """
    Score based on gold allocation.
    """

    total = sum(allocation.values())

    if total == 0:
        return 0

    gold_weight = allocation["Gold"] / total * 100

    if TARGET_GOLD_WEIGHT <= gold_weight <= MAX_GOLD:
        return 20

    if gold_weight < TARGET_GOLD_WEIGHT:
        return round(gold_weight / TARGET_GOLD_WEIGHT * 20)

    excess = gold_weight - MAX_GOLD

    return max(0, 20 - round(excess))


def calculate_portfolio_health(df, allocation):
    """
    Calculate overall portfolio health.
    """

    diversification = calculate_diversification_score(df)
    sector = calculate_sector_score(df)
    concentration = calculate_stock_concentration_score(df)
    cash = calculate_cash_score(allocation)
    gold = calculate_gold_score(allocation)

    total = (
        diversification +
        sector +
        concentration +
        cash +
        gold
    )

    return {
        "Diversification": diversification,
        "Sector": sector,
        "Concentration": concentration,
        "Cash": cash,
        "Gold": gold,
        "Total": total,
    }
