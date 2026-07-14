# ==========================================
# Performance Analysis
# ==========================================

def calculate_top_performers(df):
    """
    Returns the top 3 performing stocks
    based on Return %.
    """

    top_performers = df.sort_values(
        "Return %",
        ascending=False
    ).head(3)

    return top_performers


def calculate_top_losers(df):
    """
    Returns the top 3 losing stocks
    based on Return %.
    """

    top_losers = df.sort_values(
        "Return %",
        ascending=True
    ).head(3)

    return top_losers


def print_top_performers(top_performers):

    print()
    print("=" * 40)
    print("TOP 3 PERFORMERS")
    print("=" * 40)

    for _, row in top_performers.iterrows():

        print(
            f'{row["Stock"]:<20}'
            f'{row["Return %"]:>8.2f}%'
        )

    print("=" * 40)


def print_top_losers(top_losers):

    print()
    print("=" * 40)
    print("TOP 3 LOSERS")
    print("=" * 40)

    for _, row in top_losers.iterrows():

        print(
            f'{row["Stock"]:<20}'
            f'{row["Return %"]:>8.2f}%'
        )

    print("=" * 40)