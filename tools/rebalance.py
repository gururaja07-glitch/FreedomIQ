"""
FreedomIQ

Module : Rebalancing

Purpose :
Suggests portfolio rebalancing actions.

Author : Gururaj N K
Version : 0.1
"""

from tools.portfolio_utils import (
    calculate_largest_holding,
    calculate_sector_weights
)

from tools.rules import (
    MAX_STOCK_WEIGHT,
    MAX_SECTOR_WEIGHT
)

def rebalance_stock(df):

    largest_holding = calculate_largest_holding(df)

    stock = largest_holding["Stock"]
    weight = largest_holding["Weight %"]

    if weight <= MAX_STOCK_WEIGHT:
        return None

    excess = weight - MAX_STOCK_WEIGHT

    return {
        "Type": "Stock",
        "Name": stock,
        "Current Weight": weight,
        "Target Weight": MAX_STOCK_WEIGHT,
        "Excess": excess
    }

def rebalance_sector(df):

    sector_weights = calculate_sector_weights(df)

    largest_sector = sector_weights.idxmax()
    largest_weight = sector_weights.max()

    if largest_weight <= MAX_SECTOR_WEIGHT:
        return None

    excess = largest_weight - MAX_SECTOR_WEIGHT

    return {
        "Type": "Sector",
        "Name": largest_sector,
        "Current Weight": largest_weight,
        "Target Weight": MAX_SECTOR_WEIGHT,
        "Excess": excess
    }

def calculate_rebalancing(df):

    actions = []

    stock_action = rebalance_stock(df)

    if stock_action:
        actions.append(stock_action)

    sector_action = rebalance_sector(df)

    if sector_action:
        actions.append(sector_action)

    return actions

def print_rebalancing(actions):

    print()
    print("=" * 50)
    print("REBALANCING SUGGESTIONS")
    print("=" * 50)

    if not actions:

        print("Portfolio is well balanced.")

    else:

        for action in actions:

            print(f'Type            : {action["Type"]}')
            print(f'Name            : {action["Name"]}')
            print(f'Current Weight  : {action["Current Weight"]:.2f}%')
            print(f'Target Weight   : {action["Target Weight"]:.2f}%')
            print(f'Excess          : {action["Excess"]:.2f}%')
            print("-" * 50)