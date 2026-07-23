from research.models import (
    CompanySnapshot,
    FinancialSummary,
    ValuationSummary,
    InvestmentScore,
)


def generate_summary(
    snapshot: CompanySnapshot,
    financials: FinancialSummary,
    valuation: ValuationSummary,
    score: InvestmentScore,
) -> str:
    """
    Generates a concise executive summary for the research report.
    """

    company = snapshot.company
    rating = score.rating
    total = score.total

    parts = []

    parts.append(
        f"{company} is a {rating.lower()} rated company with a FreedomIQ score of {total}/100."
    )

    if score.profitability >= 15:
        parts.append("The business demonstrates strong profitability.")

    if score.growth >= 15:
        parts.append("Growth indicators remain healthy.")
    elif score.growth <= 5:
        parts.append("Growth appears to be slowing.")

    if score.valuation >= 15:
        parts.append("Current valuation appears attractive.")
    elif score.valuation <= 5:
        parts.append("Valuation does not appear particularly attractive.")

    if score.financial_strength >= 15:
        parts.append("The balance sheet looks financially strong.")

    parts.append(
        f"Overall, FreedomIQ assigns a {rating.upper()} recommendation based on the available financial data."
    )

    return " ".join(parts)