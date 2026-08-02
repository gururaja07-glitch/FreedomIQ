from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portfolio.dashboard import PortfolioDashboard


def generate_advice(
    dashboard: "PortfolioDashboard",
) -> list[str]:
    """
    Generate portfolio recommendations.
    """

    advice = []

    summary = dashboard.summary
    metrics = dashboard.metrics
    score = dashboard.score

    # ----------------------------------------
    # Concentration
    # ----------------------------------------

    if metrics.largest_weight > 20:
        advice.append(
            f"{metrics.largest_holding} accounts for "
            f"{metrics.largest_weight:.2f}% of your portfolio. "
            "Consider reducing it towards 15-20%."
        )

    # ----------------------------------------
    # Diversification
    # ----------------------------------------

    if metrics.diversification_score < 60:
        advice.append(
            "Portfolio concentration is high. "
            "Increase diversification across more holdings."
        )

    # ----------------------------------------
    # Performance
    # ----------------------------------------

    if summary.total_return > 30:
        advice.append(
            "Portfolio has generated excellent long-term returns. "
            "Avoid unnecessary churn."
        )

    # ----------------------------------------
    # Overall Score
    # ----------------------------------------

    if score.overall >= 80:
        advice.append(
            "Overall portfolio quality is strong. "
            "Focus on gradual optimization rather than major changes."
        )

    elif score.overall >= 60:
        advice.append(
            "Portfolio is fundamentally healthy but can be improved through better allocation."
        )

    else:
        advice.append(
            "Portfolio requires significant restructuring."
        )

    return advice
