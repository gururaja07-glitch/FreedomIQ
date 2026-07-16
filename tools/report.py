from tools.analytics import calculate_portfolio_summary


def print_summary(df):
    """
    Print portfolio summary.
    """

    summary = calculate_portfolio_summary(df)

    best = df.sort_values(
        "Return %",
        ascending=False
    ).iloc[0]

    worst = df.sort_values(
        "Return %",
        ascending=True
    ).iloc[0]

    print("=" * 55)
    print("              FREEDOMIQ PORTFOLIO")
    print("=" * 55)

    print(f"Total Investment : ₹ {summary['Investment']:,.2f}")
    print(f"Current Value    : ₹ {summary['Current Value']:,.2f}")
    print(f"Overall Profit   : ₹ {summary['Profit']:,.2f}")
    print(f"Overall Return   : {summary['Return %']:.2f}%")

    print()

    print(f"Number of Stocks : {summary['Number of Stocks']}")
    print(f"Largest Holding  : {summary['Largest Holding']}")
    print(f"Holding Weight   : {summary['Largest Weight']:.2f}%")

    print()

    print(
        f"Best Performer   : "
        f"{best['Company']} ({best['Return %']:.2f}%)"
    )

    print(
        f"Worst Performer  : "
        f"{worst['Company']} ({worst['Return %']:.2f}%)"
    )

    print("=" * 55)