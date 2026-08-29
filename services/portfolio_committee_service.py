from models.portfolio_committee import PortfolioCommitteeResult

from services.decision_service import (
    get_investment_decision,
)

from services.portfolio_decision_service import (
    get_portfolio_decisions,
)

from services.portfolio_action_service import (
    generate_portfolio_action_plan,
)

from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import (
    calculate_metrics,
    calculate_asset_allocation,
)
from tools.risk import calculate_portfolio_risk


def get_portfolio_investment_committee() -> PortfolioCommitteeResult:
    """
    Generate a portfolio-level investment committee result.

    Combines:
    - Individual company investment decisions
    - Existing portfolio-level decisions
    - Prioritized portfolio actions

    Portfolio context is calculated once and reused
    across all company decisions.
    """

    # ------------------------------------------------------
    # 1. Load and prepare portfolio ONCE
    # ------------------------------------------------------

    portfolio = get_portfolio()

    portfolio = update_prices(
        portfolio
    )

    portfolio = calculate_metrics(
        portfolio
    )

    # ------------------------------------------------------
    # 2. Calculate portfolio risk ONCE
    # ------------------------------------------------------

    allocation = calculate_asset_allocation(
        portfolio
    )

    _, overall_risk = calculate_portfolio_risk(
        portfolio,
        allocation,
    )

    # ------------------------------------------------------
    # 3. Generate individual company decisions
    # ------------------------------------------------------

    company_decisions = []

    for _, row in portfolio.iterrows():

        sector = str(
            row.get("Sector", "")
        ).strip().lower()

        industry = str(
            row.get("Industry", "")
        ).strip().lower()

        # Company analysis applies only to
        # actual companies.
        if sector in {"gold", "cash"}:
            continue

        if industry in {"", "unknown"}:
            continue

        company = row["Stock"]

        decision = get_investment_decision(
            company,
            portfolio=portfolio,
            portfolio_risk=overall_risk,
        )

        company_decisions.append(
            decision
        )

    # ------------------------------------------------------
    # 4. Existing portfolio-level decisions
    # ------------------------------------------------------

    portfolio_actions = (
        get_portfolio_decisions()
    )

    # ------------------------------------------------------
    # 5. Portfolio synthesis
    # ------------------------------------------------------

    add_count = sum(
        decision.decision == "ADD"
        for decision in company_decisions
    )

    reduce_count = sum(
        decision.decision in ["REDUCE", "SELL"]
        for decision in company_decisions
    )

    hold_count = sum(
        decision.decision == "HOLD"
        for decision in company_decisions
    )

    watch_count = sum(
        decision.decision == "WATCH"
        for decision in company_decisions
    )

    summary = (
        f"Portfolio committee reviewed "
        f"{len(company_decisions)} holdings: "
        f"{add_count} ADD, "
        f"{hold_count} HOLD, "
        f"{reduce_count} REDUCE/SELL, "
        f"{watch_count} WATCH. "
        f"{len(portfolio_actions)} portfolio-level "
        f"actions require attention."
    )

    # ------------------------------------------------------
    # 6. Committee confidence
    # ------------------------------------------------------

    if not company_decisions:

        confidence = "Low"

    else:

        high_confidence = sum(
            decision.confidence == "High"
            for decision in company_decisions
        )

        high_confidence_ratio = (
            high_confidence
            / len(company_decisions)
        )

        if high_confidence_ratio >= 0.75:
            confidence = "High"

        elif high_confidence_ratio >= 0.50:
            confidence = "Medium"

        else:
            confidence = "Low"

    # ------------------------------------------------------
    # 7. Prioritized action plan
    # ------------------------------------------------------

    prioritized_actions = (
        generate_portfolio_action_plan(
            company_decisions=company_decisions,
            portfolio_actions=portfolio_actions,
        )
    )

    # ------------------------------------------------------
    # 8. Return structured committee result
    # ------------------------------------------------------

    return PortfolioCommitteeResult(
        company_decisions=company_decisions,
        portfolio_actions=portfolio_actions,
        prioritized_actions=prioritized_actions,
        summary=summary,
        confidence=confidence,
    )