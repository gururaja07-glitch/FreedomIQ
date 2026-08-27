from models.portfolio_action import PortfolioAction
from models.portfolio_committee import PortfolioCommitteeResult


def _company_action_priority(decision) -> str:
    """
    Determine the priority of a company action using
    existing InvestmentDecision evidence.

    No new investment scoring is performed here.
    """

    action = decision.decision
    weight = float(decision.portfolio_weight)
    confidence = decision.confidence

    # High-risk portfolio situations take precedence.
    if action == "SELL":
        if weight >= 10:
            return "CRITICAL"
        return "HIGH"

    if action == "REDUCE":
        if weight >= 15:
            return "CRITICAL"
        if weight >= 5:
            return "HIGH"
        return "MEDIUM"

    # Strong opportunities deserve attention, but
    # concentration must be respected.
    if action == "ADD":
        if weight >= 15:
            return "HIGH"

        if confidence == "High":
            return "MEDIUM"

        return "LOW"

    # HOLD positions are normally lower priority,
    # unless portfolio concentration is significant.
    if action == "HOLD":
        if weight >= 20:
            return "HIGH"

        if weight >= 15:
            return "MEDIUM"

        return "LOW"

    return "LOW"


def _build_company_action(decision) -> PortfolioAction:
    """
    Convert an existing InvestmentDecision into
    a prioritized PortfolioAction.
    """

    action = decision.decision
    priority = _company_action_priority(decision)

    if action == "ADD":
        if decision.portfolio_weight >= 15:
            action_text = "HOLD / NO ADD"
        else:
            action_text = "ADD"

    elif action == "HOLD":
        if decision.portfolio_weight >= 20:
            action_text = "HOLD / NO ADD"
        else:
            action_text = "HOLD"

    else:
        action_text = action

    reason = (
        f"Fundamentals: {decision.fundamental_rating}; "
        f"valuation: {decision.valuation_view}; "
        f"portfolio weight: {decision.portfolio_weight:.1f}%."
    )

    evidence = (
        f"FCF quality: {decision.fcf_quality}; "
        f"DCF: {decision.dcf_verdict}; "
        f"financial data quality: "
        f"{decision.financial_data_quality}; "
        f"confidence: {decision.confidence}."
    )

    return PortfolioAction(
        priority=priority,
        company=decision.company,
        action=action_text,
        reason=reason,
        evidence=evidence,
    )


def _portfolio_action_priority(priority: str) -> str:
    """
    Normalize existing portfolio-action priorities
    to the committee priority hierarchy.
    """

    if priority == "High":
        return "HIGH"

    if priority == "Medium":
        return "MEDIUM"

    return "LOW"


def _build_portfolio_action(action) -> PortfolioAction:
    """
    Convert an existing PortfolioDecision into
    a prioritized PortfolioAction.
    """

    return PortfolioAction(
        priority=_portfolio_action_priority(
            action.priority
        ),
        company="PORTFOLIO",
        action=action.action,
        reason=action.issue,
        evidence=action.reason,
    )


def generate_portfolio_action_plan(
    company_decisions,
    portfolio_actions,
) -> list[PortfolioAction]:
    """
    Generate a ranked portfolio action plan from
    the existing Investment Committee result.

    This service does not recalculate financial,
    valuation, DCF, or portfolio metrics.
    """

    actions = []

    # ------------------------------------------------------
    # Company actions
    # ------------------------------------------------------

    for decision in company_decisions:
        actions.append(
            _build_company_action(decision)
        )

    # ------------------------------------------------------
    # Portfolio-level actions
    # ------------------------------------------------------

    for portfolio_action in portfolio_actions:
        actions.append(
            _build_portfolio_action(
                portfolio_action
            )
        )

    # ------------------------------------------------------
    # Priority ordering
    # ------------------------------------------------------

    priority_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    actions.sort(
        key=lambda item: (
            priority_order.get(
                item.priority,
                99,
            ),
            item.company,
        )
    )

    return actions