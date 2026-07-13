from tools.sector import SECTOR_MAP


def add_sector(df):

    df["Sector"] = df["Stock"].map(SECTOR_MAP)

    return df


def calculate_sector_summary(df):

    sector_summary = df.groupby(
        "Sector"
    )["Current Value"].sum()

    return sector_summary


def print_sector_summary(sector_summary):

    print()
    print("=" * 40)
    print("SECTOR ALLOCATION")
    print("=" * 40)

    for sector, value in sector_summary.items():
        print(f"{sector:<20} ₹ {value:,.2f}")

    print("=" * 40)