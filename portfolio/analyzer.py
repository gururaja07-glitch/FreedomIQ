from dataclasses import dataclass
import pandas as pd


@dataclass
class PortfolioSummary:
    total_invested: float
    total_value: float
    total_profit: float
    total_return: float

    largest_holding: str
    largest_holding_weight: float

    number_of_holdings: int


def analyze_portfolio(df: pd.DataFrame) -> PortfolioSummary:
    """
    Analyze a portfolio DataFrame returned by get_portfolio().
    """

    total_invested = df["InvestedValue"].sum()
    total_value = df["CurrentValue"].sum()

    total_profit = total_value - total_invested

    if total_invested > 0:
        total_return = (
            total_profit / total_invested * 100
        )
    else:
        total_return = 0.0

    largest = df.loc[df["WeightPct"].idxmax()]

    return PortfolioSummary(
    total_invested=float(round(total_invested, 2)),
    total_value=float(round(total_value, 2)),
    total_profit=float(round(total_profit, 2)),
    total_return=float(round(total_return, 2)),

    largest_holding=str(largest["Stock"]),
    largest_holding_weight=float(round(largest["WeightPct"], 2)),

    number_of_holdings=int(len(df)),
)