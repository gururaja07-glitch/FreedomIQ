import matplotlib.pyplot as plt


def portfolio_pie_chart(df):
    """Portfolio allocation by current value."""

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        df["Current Value"],
        labels=df["Stock"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Portfolio Allocation")

    return fig


def sector_pie_chart(df):
    """Sector allocation by current value."""

    sector = (
        df.groupby("Sector")["Current Value"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        sector.values,
        labels=sector.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Sector Allocation")

    return fig


def top_holdings_chart(df):
    """Top 10 holdings by current value."""

    top = (
        df.sort_values(
            "Current Value",
            ascending=False
        )
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        top["Stock"],
        top["Current Value"]
    )

    ax.set_title("Top 10 Holdings")

    ax.set_ylabel("Current Value (₹)")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    return fig


def asset_allocation_chart(equity, gold, silver, cash):
    """Overall asset allocation."""

    values = [equity, gold, silver, cash]

    labels = [
        "Equity",
        "Gold",
        "Silver",
        "Cash"
    ]

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Asset Allocation")

    return fig