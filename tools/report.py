def print_summary(df):

    investment = df["Investment"].sum()
    current = df["Current Value"].sum()
    profit = df["Profit"].sum()
    returns = (profit / investment * 100)

    top = df.sort_values(
        "Current Value",
        ascending=False
    ).iloc[0]

    best = df.sort_values(
        "Return %",
        ascending=False
    ).iloc[0]

    worst = df.sort_values(
        "Return %",
        ascending=True
    ).iloc[0]

    print("=" * 50)
    print("          PORTFOLIO SUMMARY")
    print("=" * 50)

    print(f"Investment     : ₹ {investment:,.2f}")
    print(f"Current Value  : ₹ {current:,.2f}")
    print(f"Profit         : ₹ {profit:,.2f}")
    print(f"Return         : {returns:.2f}%")

    print()

    print(f"Top Holding    : {top['Stock']} ({top['Weight %']}%)")
    print(f"Best Performer : {best['Stock']} ({best['Return %']}%)")
    print(f"Worst Performer: {worst['Stock']} ({worst['Return %']}%)")

    print("=" * 50)