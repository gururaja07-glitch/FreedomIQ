from dataclasses import dataclass

from portfolio.analyzer import PortfolioSummary
from portfolio.metrics import PortfolioMetrics


@dataclass
class PortfolioScore:

    diversification: int
    concentration: int
    profitability: int

    overall: int

    rating: str
    stars: str


def calculate_portfolio_score(
    summary: PortfolioSummary,
    metrics: PortfolioMetrics,
) -> PortfolioScore:
    """
    Calculate an overall portfolio score.
    """

    # ----------------------------------------
    # Diversification
    # ----------------------------------------

    diversification = metrics.diversification_score

    # ----------------------------------------
    # Concentration
    # ----------------------------------------

    weight = metrics.largest_weight

    if weight < 10:
        concentration = 100
    elif weight < 15:
        concentration = 90
    elif weight < 20:
        concentration = 75
    elif weight < 25:
        concentration = 60
    elif weight < 30:
        concentration = 40
    else:
        concentration = 20

    # ----------------------------------------
    # Profitability
    # ----------------------------------------

    ret = summary.total_return

    if ret > 50:
        profitability = 100
    elif ret > 30:
        profitability = 90
    elif ret > 20:
        profitability = 75
    elif ret > 10:
        profitability = 60
    else:
        profitability = 40

    overall = round(
        (
            diversification +
            concentration +
            profitability
        ) / 3
    )

    # ----------------------------------------
    # Rating
    # ----------------------------------------

    if overall >= 85:
        rating = "Excellent"
        stars = "★★★★★"

    elif overall >= 70:
        rating = "Good"
        stars = "★★★★☆"

    elif overall >= 55:
        rating = "Average"
        stars = "★★★☆☆"

    elif overall >= 40:
        rating = "Weak"
        stars = "★★☆☆☆"

    else:
        rating = "Poor"
        stars = "★☆☆☆☆"

    return PortfolioScore(
        diversification=diversification,
        concentration=concentration,
        profitability=profitability,
        overall=overall,
        rating=rating,
        stars=stars,
    )