from tools.sector import SECTOR_MAP

def add_sector(df):

    df["Sector"] = df["Stock"].map(SECTOR_MAP)

    return df


def sector_summary(df):

    summary = df.groupby("Sector")["Current Value"].sum()

    print("\n")
    print("=" * 40)
    print("SECTOR ALLOCATION")
    print("=" * 40)

    for sector, value in summary.items():
        print(f"{sector:<20} ₹ {value:,.2f}")

    print("=" * 40)