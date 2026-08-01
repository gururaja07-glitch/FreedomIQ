from dataclasses import dataclass
import pandas as pd


@dataclass
class PortfolioMetrics:
    top5_weight: float
    top10_weight: float

    largest_holding: str
    largest_weight: float

    diversification_score: int


def calculate_metrics(df: pd.DataFrame) -> PortfolioMetrics:
    """
    Calculate portfolio concentration metrics.
    """

    df = df.sort_values(
        by="WeightPct",
        ascending=False,
    )

    top5 = df.head(5)
    top10 = df.head(10)

    top5_weight = float(round(top5["WeightPct"].sum(), 2))
    top10_weight = float(round(top10["WeightPct"].sum(), 2))

    largest = df.iloc[0]

    # ---------------------------------------
    # Diversification Score
    # ---------------------------------------

    if top5_weight < 40:
        diversification = 100
    elif top5_weight < 50:
        diversification = 80
    elif top5_weight < 60:
        diversification = 60
    elif top5_weight < 70:
        diversification = 40
    else:
        diversification = 20

    return PortfolioMetrics(
        top5_weight=top5_weight,
        top10_weight=top10_weight,

        largest_holding=str(largest["Stock"]),
        largest_weight=float(round(largest["WeightPct"], 2)),

        diversification_score=diversification,
    )