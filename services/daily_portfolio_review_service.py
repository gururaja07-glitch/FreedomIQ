from datetime import date

from models.daily_portfolio_review import (
    DailyReviewItem,
    DailyPortfolioReview,
)

from services.portfolio_service import (
    get_dashboard_data,
)

from services.portfolio_committee_service import (
    get_portfolio_investment_committee,
)

from services.portfolio_change_service import (
    compare_portfolio_state,
)


def _priority_rank(priority: str) -> int:
    """
    Convert priority to a sortable rank.
    """

    return {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }.get(priority, 99)


def _build_portfolio_status(dashboard) -> dict:
    """
    Build the daily portfolio status from existing
    dashboard information.
    """

    summary = dashboard.summary
    health = dashboard.health
    risk = dashboard.risk

    return {
        "Health Score": health.get("Total"),
        "Overall Risk": risk.get("overall"),
        "Portfolio Return": summary.get("Return %"),
        "Investment Value": summary.get("Investment"),
        "Current Value": summary.get("Current Value"),
        "Profit": summary.get("Profit"),
        "Number of Stocks": summary.get("Number of Stocks"),
        "Largest Holding": summary.get("Largest Holding"),
        "Largest Weight": summary.get("Largest Weight"),
    }


def _build_change_items(change_result) -> list[DailyReviewItem]:
    """
    Convert existing portfolio changes into concise
    investor-facing daily review items.

    Multiple changes for the same company are grouped
    together. The underlying change detection remains
    unchanged.
    """

    if change_result is None:
        return []

    grouped = {}

    for change in change_result.changes:

        key = change.company or "Portfolio"

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(change)

    items = []

    for company, changes in grouped.items():

        # Use the highest priority among the grouped changes.
        priority = min(
            changes,
            key=lambda item: _priority_rank(item.priority),
        ).priority

        # --------------------------------------------------
        # Company-specific changes
        # --------------------------------------------------

        if company != "Portfolio":

            decision_change = next(
                (
                    item
                    for item in changes
                    if item.category == "Investment Decision"
                ),
                None,
            )

            valuation_change = next(
                (
                    item
                    for item in changes
                    if item.category == "Valuation"
                ),
                None,
            )

            fundamental_change = next(
                (
                    item
                    for item in changes
                    if item.category == "Fundamental Rating"
                ),
                None,
            )

            quarterly_change = next(
                (
                    item
                    for item in changes
                    if item.category == "Quarterly Momentum"
                ),
                None,
            )

            confidence_change = next(
                (
                    item
                    for item in changes
                    if item.category == "Confidence"
                ),
                None,
            )

            weight_change = next(
                (
                    item
                    for item in changes
                    if item.category == "Portfolio Weight"
                ),
                None,
            )

            details = []

            if decision_change:
                details.append(
                    "Decision: "
                    f"{decision_change.previous_value} -> "
                    f"{decision_change.current_value}"
                )

            if fundamental_change:
                details.append(
                    "Fundamentals: "
                    f"{fundamental_change.previous_value} -> "
                    f"{fundamental_change.current_value}"
                )

            if valuation_change:
                details.append(
                    "Valuation: "
                    f"{valuation_change.previous_value} -> "
                    f"{valuation_change.current_value}"
                )

            if confidence_change:
                details.append(
                    "Confidence: "
                    f"{confidence_change.previous_value} -> "
                    f"{confidence_change.current_value}"
                )

            if quarterly_change:
                details.append(
                    "Quarterly momentum: "
                    f"{quarterly_change.previous_value} -> "
                    f"{quarterly_change.current_value}"
                )

            if weight_change:
                details.append(
                    weight_change.description
                )

            # Fallback for any future change category.
            if not details:
                details = [
                    change.description
                    for change in changes
                ]

            items.append(
                DailyReviewItem(
                    title=(
                        f"{priority} — "
                        f"{company}: Portfolio update"
                    ),
                    priority=priority,
                    description="; ".join(details),
                )
            )

        # --------------------------------------------------
        # Portfolio-level changes
        # --------------------------------------------------

        else:

            for change in changes:

                items.append(
                    DailyReviewItem(
                        title=(
                            f"{change.priority} — "
                            f"Portfolio: "
                            f"{change.category}"
                        ),
                        priority=change.priority,
                        description=change.description,
                    )
                )

    items.sort(
        key=lambda item: (
            _priority_rank(item.priority),
            item.title,
        )
    )

    return items

    items.sort(
        key=lambda item: (
            _priority_rank(item.priority),
            item.title,
        )
    )

    return items


def _build_action_items(committee) -> list[DailyReviewItem]:
    """
    Extract action-required items from the existing
    prioritized committee action plan.

    Opportunities are handled separately.
    """

    items = []

    for action in committee.prioritized_actions:

        # ADD actions are handled separately as opportunities.
        if action.action == "ADD":
            continue

        # Only CRITICAL, HIGH and MEDIUM items require
        # explicit action in the daily review.
        if action.priority not in {
            "CRITICAL",
            "HIGH",
            "MEDIUM",
        }:
            continue

        items.append(
            DailyReviewItem(
                title=(
                f"{action.priority} — "
                f"{action.company}: "
                f"{action.action}"
                ),
                priority=action.priority,
                description=(
                f"{action.reason} "
                f"{action.evidence}"
                ),
            )
        )

    items.sort(
        key=lambda item: (
            _priority_rank(item.priority),
            item.title,
        )
    )

    return items


def _build_opportunity_items(
    committee,
) -> list[DailyReviewItem]:
    """
    Extract existing ADD recommendations from the
    committee action plan.

    No new investment recommendation is generated.
    """

    items = []

    for action in committee.prioritized_actions:

        if action.action != "ADD":
            continue

        items.append(
            DailyReviewItem(
                title=(
                    f"{action.priority} — "
                    f"{action.company}: ADD"
                ),
                priority=action.priority,
                description=(
                    f"{action.reason} "
                    f"{action.evidence}"
                ),
            )
        )

    items.sort(
        key=lambda item: (
            _priority_rank(item.priority),
            item.title,
        )
    )

    return items


def _build_watchpoints(
    dashboard,
    committee,
) -> list[DailyReviewItem]:
    """
    Build watchpoints from existing portfolio risk,
    concentration and quarterly information.
    """

    watchpoints = []

    risk_details = dashboard.risk.get(
        "details",
        {},
    )

    # ------------------------------------------------------
    # Risk details
    # ------------------------------------------------------

    for category, value in risk_details.items():

        if not value:
            continue

        if not isinstance(value, (list, tuple)):
            continue

        if len(value) < 2:
            continue

        level = value[0]
        reason = value[1]

        if level in {"Medium", "High"}:

            priority = (
                "HIGH"
                if level == "High"
                else "MEDIUM"
            )

            watchpoints.append(
                DailyReviewItem(
                    title=(
                        f"{priority} — "
                        f"{category} risk"
                    ),
                    priority=priority,
                    description=str(reason),
                )
            )

    # ------------------------------------------------------
    # Quarterly momentum
    # ------------------------------------------------------

    counts = committee.quarterly_assessment_counts

    negative = counts.get(
        "Negative",
        0,
    )

    if negative > 0:

        watchpoints.append(
            DailyReviewItem(
                title=(
                    "HIGH — Negative quarterly momentum"
                ),
                priority="HIGH",
                description=committee.quarterly_summary,
            )
        )

    # ------------------------------------------------------
    # Committee confidence
    # ------------------------------------------------------

    if committee.confidence == "Low":

        watchpoints.append(
            DailyReviewItem(
                title="MEDIUM — Committee confidence is Low",
                priority="MEDIUM",
                description=(
                    "The current investment committee "
                    "contains a relatively low proportion "
                    "of high-confidence company decisions."
                ),
            )
        )

    watchpoints.sort(
        key=lambda item: (
            _priority_rank(item.priority),
            item.title,
        )
    )

    return watchpoints


def _build_conclusion(
    dashboard,
    committee,
    changes,
    actions,
    opportunities,
    watchpoints,
) -> str:
    """
    Generate a deterministic daily conclusion.

    This function does not use an LLM or create new
    investment intelligence.
    """

    health = dashboard.health.get(
        "Total",
        0,
    )

    risk = dashboard.risk.get(
        "overall",
        "Unknown",
    )

    if health < 60:
        health_message = (
            "Portfolio health is weak and requires attention."
        )

    elif health < 80:
        health_message = (
            "Portfolio health can be improved gradually."
        )

    else:
        health_message = (
            "Portfolio health remains relatively strong."
        )

    if actions:
        action_message = (
            f"{len(actions)} action item(s) require attention."
        )
    else:
        action_message = (
            "No immediate corrective action is currently "
            "identified."
        )

    if opportunities:
        opportunity_message = (
            f"{len(opportunities)} existing investment "
            "opportunit"
            f"{'y' if len(opportunities) == 1 else 'ies'} "
            "are available for consideration."
        )
    else:
        opportunity_message = (
            "No ADD opportunities are currently identified."
        )

    if watchpoints:
        watch_message = (
            f"{len(watchpoints)} portfolio watchpoint(s) "
            "should remain under observation."
        )
    else:
        watch_message = (
            "No material portfolio watchpoints are currently "
            "identified."
        )

    return (
        f"{health_message} "
        f"Overall risk is {risk}. "
        f"{action_message} "
        f"{opportunity_message} "
        f"{watch_message}"
    )


def get_daily_portfolio_review() -> DailyPortfolioReview:
    """
    Generate the complete deterministic daily
    FreedomIQ portfolio review.

    This is an orchestration layer only.

    It reuses:
    - Dashboard intelligence
    - Investment Committee decisions
    - Portfolio change detection

    It does not create new financial or investment
    intelligence.
    """

    # ------------------------------------------------------
    # 1. Existing dashboard intelligence
    # ------------------------------------------------------

    dashboard = get_dashboard_data()

    # ------------------------------------------------------
    # 2. Existing investment committee
    # ------------------------------------------------------

    committee = (
        get_portfolio_investment_committee()
    )

    # ------------------------------------------------------
    # 3. Existing change detection
    # ------------------------------------------------------

    change_result = (
        compare_portfolio_state()
    )

    # ------------------------------------------------------
    # 4. Build daily sections
    # ------------------------------------------------------

    portfolio_status = (
        _build_portfolio_status(
            dashboard
        )
    )

    changes = _build_change_items(
        change_result
    )

    actions = _build_action_items(
        committee
    )

    opportunities = _build_opportunity_items(
        committee
    )

    watchpoints = _build_watchpoints(
        dashboard,
        committee,
    )

    # ------------------------------------------------------
    # 5. Daily conclusion
    # ------------------------------------------------------

    conclusion = _build_conclusion(
        dashboard=dashboard,
        committee=committee,
        changes=changes,
        actions=actions,
        opportunities=opportunities,
        watchpoints=watchpoints,
    )

    return DailyPortfolioReview(
        review_date=date.today().isoformat(),
        portfolio_status=portfolio_status,
        changes=changes,
        actions=actions,
        opportunities=opportunities,
        watchpoints=watchpoints,
        conclusion=conclusion,
    )
