# BUSINESS RULE
# Cash is considered part of the portfolio.
# Selling a stock increases cash but does not reduce total portfolio value.
from tools.rules import MAX_STOCK_WEIGHT

def rebalance_portfolio(df):

    total_portfolio = df["Current Value"].sum()

    overweight = df[df["Weight %"] > MAX_STOCK_WEIGHT]

    print("=" * 40)
    print("REBALANCING ADVISOR")
    print("=" * 40)

    for index, row in overweight.iterrows():

        target_value = total_portfolio * MAX_STOCK_WEIGHT / 100

        sell_amount = row["Current Value"] - target_value

        print("-" * 40)
        print(f'Stock           : {row["Stock"]}')
        print(f'Current Weight  : {row["Weight %"]:.2f}%')
        print(f'Target Weight   : {MAX_STOCK_WEIGHT:.2f}%')
        print(f'Sell Amount     : ₹{sell_amount:,.2f}')

    print("=" * 40)
   