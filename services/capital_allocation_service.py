from models.capital_allocation import (
    CapitalAllocationRecommendation,
    CapitalAllocationPlan,
)

from services.portfolio_committee_service import (
    get_portfolio_investment_committee,
)

def _get_allocation_priority(
    decision,
) -> int:
    """
    Rank eligible ADD opportunities using existing
    InvestmentDecision evidence.

    Lower number means higher allocation priority.
    """

    if (
        decision.confidence == "High"
        and decision.fundamental_rating == "Strong Buy"
        and decision.valuation_view == "Undervalued"
    ):
        return 1

    if decision.confidence == "High":
        return 2

    if decision.confidence == "Medium":
        return 3

    return 4

def get_capital_allocation_plan(
    available_capital: float,
) -> CapitalAllocationPlan:
    """
    Generate a recommendation for deploying
    new capital using the existing Portfolio
    Investment Committee decisions.

    This service does not perform new company
    research or investment analysis.
    """

    # ------------------------------------------------------
    # 1. Validate capital
    # ------------------------------------------------------

    if available_capital <= 0:
        raise ValueError(
            "Available capital must be greater than zero."
        )

    # ------------------------------------------------------
    # 2. Get existing committee result
    # ------------------------------------------------------

    committee = (
        get_portfolio_investment_committee()
    )

    # ------------------------------------------------------
    # 3. Identify eligible ADD candidates
    # ------------------------------------------------------

    candidates = []

    for decision in committee.company_decisions:

        if decision.decision != "ADD":
            continue

        # Do not increase already large positions.
        if decision.portfolio_weight >= 20:
            continue

        candidates.append(
            decision
        )

    def _get_allocation_share(
        priority: int,
    ) -> float:
        """
        Return the relative allocation share
        for each priority tier.
        """

        shares = {
            1: 5,
            2: 3,
            3: 2,
            4: 1,
        }

        return shares.get(priority, 1)
    # ------------------------------------------------------
    # 4. Rank allocation candidates
    # ------------------------------------------------------

    candidates.sort(
        key=_get_allocation_priority
    )
    # ------------------------------------------------------
    # 5. Handle no eligible candidates
    # ------------------------------------------------------

    if not candidates:

        return CapitalAllocationPlan(
            available_capital=available_capital,
            recommendations=[],
            unallocated_capital=available_capital,
            summary=(
                "No eligible ADD opportunities are "
                "currently available for new capital."
            ),
        )


    # ------------------------------------------------------
    # 6. Calculate allocation shares
    # ------------------------------------------------------

    total_shares = sum(
        _get_allocation_share(
            _get_allocation_priority(decision)
        )
        for decision in candidates
    )

    recommendations = []
    allocated_capital = 0.0

    # ------------------------------------------------------
    # 7. Build allocation recommendations
    # ------------------------------------------------------

    for index, decision in enumerate(candidates):

        priority = _get_allocation_priority(
            decision
        )

        share = _get_allocation_share(
            priority
        )

        allocation_percent = (
            share / total_shares
        ) * 100

        # Give the final candidate any rounding remainder
        # so total allocation always equals available capital.
        if index == len(candidates) - 1:

            amount = (
                available_capital - allocated_capital
            )

        else:

            amount = round(
                available_capital
                * allocation_percent
                / 100,
                2,
            )

        allocated_capital += amount

        reason = (
            f"{decision.decision} recommendation; "
            f"confidence: {decision.confidence}; "
            f"fundamentals: "
            f"{decision.fundamental_rating}; "
            f"valuation: {decision.valuation_view}; "
            f"quarterly momentum: "
            f"{decision.quarterly_assessment}."
        )

        recommendations.append(
            CapitalAllocationRecommendation(
                company=decision.company,
                amount=amount,
                allocation_percent=round(
                    amount / available_capital * 100,
                    2,
                ),
                decision=decision.decision,
                confidence=decision.confidence,
                reason=reason,
            )
        )

    # ------------------------------------------------------
    # 8. Build plan
    # ------------------------------------------------------

    unallocated_capital = round(
        available_capital - allocated_capital,
        2,
    )

    summary = (
        f"Recommended deployment of "
        f"{available_capital:,.2f} across "
        f"{len(recommendations)} eligible "
        "investment opportunities."
    )

    return CapitalAllocationPlan(
        available_capital=available_capital,
        recommendations=recommendations,
        unallocated_capital=unallocated_capital,
        summary=summary,
    )