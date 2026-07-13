from tools.portfolio_utils import (
    calculate_largest_holding,
    calculate_total_portfolio,
    calculate_cash_weight,
    calculate_gold_weight
)

def calculate_portfolio_summary(df, cash, gold):

    # Financial Summary
    investment = df["Investment"].sum()
    current_value = df["Current Value"].sum()
    profit = df["Profit"].sum()
    return_percentage = (profit / investment) * 100

    # Portfolio Statistics
    number_of_stocks = len(df)
    number_of_sectors = df["Sector"].nunique()

    # Largest Holding
    largest_holding = calculate_largest_holding(df)

    largest_stock = largest_holding["Stock"]
    largest_weight = largest_holding["Weight %"]

    # Total Portfolio
    total_portfolio = calculate_total_portfolio(
    current_value,
    cash,
    gold
)

    gold_weight = calculate_gold_weight(
    gold,
    total_portfolio
)

    cash_weight = calculate_cash_weight(
    cash,
    total_portfolio
)

    # Summary Dictionary
    summary = {
    "Investment": investment,
    "Current Value": current_value,
    "Profit": profit,
    "Return %": return_percentage,
    "Number of Stocks": number_of_stocks,
    "Number of Sectors": number_of_sectors,
    "Largest Holding": largest_stock,
    "Largest Weight": largest_weight,
    "Cash Weight": cash_weight,
    "Gold Weight": gold_weight
}
    return summary


def print_portfolio_summary(summary):

    print()
    print("=" * 50)
    print("PORTFOLIO SUMMARY")
    print("=" * 50)

    print(f'{"Investment":<25} ₹ {summary["Investment"]:,.2f}')
    print(f'{"Current Value":<25} ₹ {summary["Current Value"]:,.2f}')
    print(f'{"Profit":<25} ₹ {summary["Profit"]:,.2f}')
    print(f'{"Return %":<25} {summary["Return %"]:.2f}%')
    print(f'{"Number of Stocks":<25} {summary["Number of Stocks"]}')
    print(f'{"Number of Sectors":<25} {summary["Number of Sectors"]}')
    print(f'{"Largest Holding":<25} {summary["Largest Holding"]}')
    print(f'{"Largest Weight":<25} {summary["Largest Weight"]:.2f}%')

    print("=" * 50)