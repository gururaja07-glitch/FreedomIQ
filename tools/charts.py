import matplotlib.pyplot as plt

def allocation_chart(df):

    # Keep only rows with valid Current Value
    chart_df = df.dropna(subset=["Current Value"])

    # Remove zero or negative values
    chart_df = chart_df[chart_df["Current Value"] > 0]

    plt.figure(figsize=(8, 8))

    plt.pie(
        chart_df["Current Value"],
        labels=chart_df["Stock"],
        autopct="%1.1f%%"
    )

    plt.title("Portfolio Allocation")

    plt.savefig("charts/allocation.png")

    plt.close()

    print("✅ Chart saved to charts/allocation.png")


def top_holdings_chart(df):

    top = df.sort_values(
        "Current Value",
        ascending=False
    ).head(10)

    plt.figure(figsize=(10, 6))

    plt.bar(
        top["Stock"],
        top["Current Value"]
    )

    plt.xticks(rotation=45)

    plt.title("Top 10 Holdings")

    plt.tight_layout()

    plt.savefig("charts/top_holdings.png")

    plt.close()

    print("✅ Top holdings chart saved")