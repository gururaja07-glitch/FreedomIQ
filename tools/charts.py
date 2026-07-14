import matplotlib.pyplot as plt


def portfolio_pie_chart(df):

    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        df["Current Value"],
        labels=df["Stock"],
        autopct="%1.1f%%"
    )

    ax.set_title("Portfolio Allocation")

    return fig


def top_holdings_chart(df):

    top = df.sort_values(
        "Current Value",
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(10,6))

    ax.bar(
        top["Stock"],
        top["Current Value"]
    )

    plt.xticks(rotation=45)

    ax.set_title("Top 10 Holdings")

    plt.tight_layout()

    return fig