from services.research_service import analyze_company
from tools.portfolio import get_portfolio
from tools.analytics import calculate_metrics, calculate_asset_allocation
from tools.risk import calculate_portfolio_risk
from tools.decision import make_investment_decision
from tools.market import update_prices


def get_investment_decision(company_name: str):
    """
    Generate a personal investment decision
    using company research and portfolio context.
    """

    df = get_portfolio()

    # Use the same refreshed price state as the portfolio dashboard
    df = update_prices(df)

    # Calculate portfolio metrics
    df = calculate_metrics(df)
    # Find the requested holding
    matches = df[df["Stock"].str.upper() == company_name.upper()]

    if matches.empty:
        raise ValueError(
            f"{company_name} is not present in the portfolio."
        )

    portfolio_row = matches.iloc[0]

    # Calculate portfolio risk
    allocation = calculate_asset_allocation(df)

    _, overall_risk = calculate_portfolio_risk(
        df,
        allocation,
    )

    # Research the company
    company_analysis = analyze_company(
        company_name
    )

    # Make personal investment decision
    decision = make_investment_decision(
        company_analysis,
        portfolio_row,
        overall_risk,
    )

    return decision