from dataclasses import dataclass

from portfolio.loader import get_portfolio
from portfolio.analyzer import analyze_portfolio
from portfolio.metrics import calculate_metrics
from portfolio.scoring import calculate_portfolio_score
from portfolio.advisor import generate_advice
from portfolio.decision_engine import generate_decisions


@dataclass
class PortfolioDashboard:
    summary: object
    metrics: object
    score: object
    advice: list[str]
    decisions: list


def get_portfolio_dashboard() -> PortfolioDashboard:
    """
    Build the complete portfolio dashboard.
    """

    # Load portfolio
    portfolio = get_portfolio()

    # Analyze portfolio
    summary = analyze_portfolio(portfolio)

    # Calculate metrics
    metrics = calculate_metrics(portfolio)

    # Calculate score
    score = calculate_portfolio_score(
        summary,
        metrics,
    )

    # Create a temporary dashboard object
    dashboard = PortfolioDashboard(
        summary=summary,
        metrics=metrics,
        score=score,
        advice=[],
        decisions=[],
    )

    # Generate AI advice
    advice = generate_advice(dashboard)

    decisions = generate_decisions(dashboard)

    # Return final dashboard
    return PortfolioDashboard(
        summary=summary,
        metrics=metrics,
        score=score,
        advice=advice,
        decisions=decisions,
    )
