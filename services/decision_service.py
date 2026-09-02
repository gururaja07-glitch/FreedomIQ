from services.research_service import analyze_company
from services.quarterly_service import get_quarterly_result
from tools.portfolio import get_portfolio
from tools.analytics import (
    calculate_metrics,
    calculate_asset_allocation,
)
from tools.risk import calculate_portfolio_risk
from tools.decision import make_investment_decision
from tools.market import update_prices


def get_investment_decision(
    company_name: str,
    portfolio=None,
    portfolio_risk: str | None = None,
):
    """
    Generate a personal investment decision
    using company research and portfolio context.

    When portfolio context is supplied, it is reused.
    This avoids rebuilding the portfolio for every
    company during portfolio-level analysis.
    """

    # ------------------------------------------------------
    # Portfolio context
    # ------------------------------------------------------

    if portfolio is None:

        portfolio = get_portfolio()

        # Use the same refreshed price state as
        # the portfolio dashboard.
        portfolio = update_prices(portfolio)

        # Calculate portfolio metrics.
        portfolio = calculate_metrics(portfolio)

    # ------------------------------------------------------
    # Find requested holding
    # ------------------------------------------------------

    matches = portfolio[
        portfolio["Stock"].str.upper()
        == company_name.upper()
    ]

    if matches.empty:
        raise ValueError(
            f"{company_name} is not present in the portfolio."
        )

    portfolio_row = matches.iloc[0]

    # ------------------------------------------------------
    # Portfolio risk
    # ------------------------------------------------------

    if portfolio_risk is None:

        allocation = calculate_asset_allocation(
            portfolio
        )

        _, portfolio_risk = calculate_portfolio_risk(
            portfolio,
            allocation,
        )

    # ------------------------------------------------------
    # Company research
    # ------------------------------------------------------

    company_analysis = analyze_company(
        company_name
    )

    # ------------------------------------------------------
    # Latest quarterly result
    # ------------------------------------------------------

    quarterly_result = get_quarterly_result(
        company_name
    )

    # ------------------------------------------------------
    # Investment decision
    # ------------------------------------------------------

    decision = make_investment_decision(
        company_analysis,
        portfolio_row,
        portfolio_risk,
        quarterly_result,
    )

    return decision