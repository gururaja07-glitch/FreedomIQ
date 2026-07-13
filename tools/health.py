"""
FreedomIQ

Module : Health

Purpose :
Calculates Portfolio Health Score

Author : Gururaj N K
Version : 0.1
"""

from tools.rules import MIN_STOCKS


def calculate_diversification_score(df):

    number_of_stocks = len(df)

    if number_of_stocks >= MIN_STOCKS:
        return 20

    return (number_of_stocks / MIN_STOCKS) * 20

from tools.rules import MAX_STOCK_WEIGHT


def calculate_concentration_score(df):

    largest_weight = df["Weight %"].max()

    if largest_weight <= MAX_STOCK_WEIGHT:
        return 20

    penalty = largest_weight - MAX_STOCK_WEIGHT

    return max(0, 20 - penalty)



from tools.rules import MIN_SECTORS

def calculate_sector_score(df):

    sectors = df["Sector"].nunique()

    if sectors >= MIN_SECTORS:
        return 20

    return (sectors / MIN_SECTORS) * 20

from tools.rules import TARGET_CASH_WEIGHT


def calculate_cash_score(cash_weight):

    if cash_weight >= TARGET_CASH_WEIGHT:
        return 20

    return (cash_weight / TARGET_CASH_WEIGHT) * 20

    

from tools.rules import TARGET_GOLD_WEIGHT


def calculate_gold_score(gold_weight):

    if gold_weight >= TARGET_GOLD_WEIGHT:
        return 20

    return (gold_weight / TARGET_GOLD_WEIGHT) * 20

    

def calculate_health_score(df, cash_weight, gold_weight):

    diversification = calculate_diversification_score(df)

    concentration = calculate_concentration_score(df)

    sector = calculate_sector_score(df)

    cash = calculate_cash_score(cash_weight)

    gold = calculate_gold_score(gold_weight)

    total = (
        diversification
        + concentration
        + sector
        + cash
        + gold
    )

    health = {
        "Diversification": diversification,
        "Concentration": concentration,
        "Sector": sector,
        "Cash": cash,
        "Gold": gold,
        "Total": total
    }

    return health

def print_health_score(health):

    print()
    print("=" * 50)
    print("PORTFOLIO HEALTH")
    print("=" * 50)

    print(f'{"Diversification":<20} {health["Diversification"]:.2f}/20')
    print(f'{"Concentration":<20} {health["Concentration"]:.2f}/20')
    print(f'{"Sector":<20} {health["Sector"]:.2f}/20')
    print(f'{"Cash":<20} {health["Cash"]:.2f}/20')
    print(f'{"Gold":<20} {health["Gold"]:.2f}/20')

    print("-" * 50)

    print(f'{"TOTAL":<20} {health["Total"]:.2f}/100')

    print("=" * 50)