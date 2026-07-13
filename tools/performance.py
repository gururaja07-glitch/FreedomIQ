def calculate_top_performers(df):

    top_performers = df.sort_values(
        "Return %",
        ascending=False
    ).iloc[:3]

    return top_perfomers


def print_top_performers(top_performers):

    print("=" * 40)
    print("TOP 3 PERFORMERS")
    print("=" * 40)

    for _, row in top_performers.iterrows():
        print(f'{row["Stock"]:<20} {row["Return %"]:.2f}%')

    print("=" * 40)


def calculate_top_losers(df):

    top_losers = df.sort_values(
        "Return %",
        ascending=True
    ).iloc[:3]

    return top_losers


def print_top_losers(top_losers):

    print("=" * 40)
    print("TOP 3 LOSERS")
    print("=" * 40)

    for _, row in top_losers.iterrows():
        print(f'{row["Stock"]:<20} {row["Return %"]:.2f}%')

    print("=" * 40)