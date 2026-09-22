from services.daily_portfolio_review_service import (
    get_daily_portfolio_review,
)

from services.daily_review_change_service import (
    get_daily_review_changes,
)

from services.daily_review_trend_service import (
    get_daily_review_trends,
)

from models.daily_investor_brief import (
    DailyInvestorBrief,
)


def _build_portfolio_snapshot(
    portfolio_status: dict,
) -> dict:
    """
    Extract the key portfolio metrics already produced
    by the daily portfolio review.

    No new portfolio calculations are performed here.
    """

    fields = [
        "Health Score",
        "Overall Risk",
        "Portfolio Return",
        "Investment Value",
        "Current Value",
        "Profit",
        "Number of Stocks",
        "Largest Holding",
        "Largest Weight",
    ]

    return {
        field: portfolio_status.get(field)
        for field in fields
        if field in portfolio_status
    }


def _build_changes(
    change_result,
) -> list[dict]:
    """
    Convert existing daily review changes into
    investor-brief data.
    """

    if change_result is None:
        return []

    return [
        {
            "category": change.category,
            "title": change.title,
            "previous_value": change.previous_value,
            "current_value": change.current_value,
            "priority": change.priority,
            "description": change.description,
        }
        for change in change_result.changes
    ]


def _build_persistent_items(
    items,
) -> list[dict]:
    """
    Convert persistent trend items into dictionaries.
    """

    return [
        {
            "category": item.category,
            "title": item.title,
            "review_count": item.review_count,
            "consecutive_count": item.consecutive_count,
            "first_seen": item.first_seen,
            "last_seen": item.last_seen,
            "priority": item.priority,
        }
        for item in items
    ]


def _build_watchpoints(
    review,
    trend,
) -> list[dict]:
    """
    Combine current watchpoints with persistent watchpoints.

    Existing intelligence is reused without introducing
    new watchpoint rules.
    """

    watchpoints = []

    seen_titles = set()

    for item in review.watchpoints:
        title = item.title

        if title in seen_titles:
            continue

        seen_titles.add(title)

        watchpoints.append(
            {
                "title": title,
                "priority": item.priority,
                "description": item.description,
                "persistent": False,
            }
        )

    for item in trend.persistent_watchpoints:
        title = item.title

        if title in seen_titles:
            continue

        seen_titles.add(title)

        watchpoints.append(
            {
                "title": title,
                "priority": item.priority,
                "description": (
                    f"Persistent across "
                    f"{item.review_count} review(s); "
                    f"consecutive: "
                    f"{item.consecutive_count}."
                ),
                "persistent": True,
            }
        )

    return watchpoints


def _build_trends(
    trend,
) -> dict:
    """
    Convert historical trend intelligence into
    brief-friendly data.
    """

    return {
        "health": trend.health_trend,
        "risk": trend.risk_trend,
        "largest_holding_weight": (
            trend.largest_holding_weight_trend
        ),
        "review_count": trend.review_count,
        "start_date": trend.start_date,
        "end_date": trend.end_date,
    }


def _build_conclusion(
    review,
    trend,
) -> str:
    """
    Reuse the deterministic daily review conclusion.

    The investor brief does not introduce new narrative
    or investment judgement.
    """

    return review.conclusion


def build_daily_investor_brief() -> DailyInvestorBrief:
    """
    Assemble existing portfolio intelligence into one
    daily investor brief.
    """

    review = get_daily_portfolio_review()

    change_result = get_daily_review_changes()

    trend = get_daily_review_trends()

    if trend is None:
        raise ValueError(
            "Daily review trend data is unavailable."
        )

    portfolio_snapshot = _build_portfolio_snapshot(
        review.portfolio_status
    )

    changes = _build_changes(
        change_result
    )

    persistent_actions = _build_persistent_items(
        trend.persistent_actions
    )

    persistent_opportunities = (
        _build_persistent_items(
            trend.persistent_opportunities
        )
    )

    watchpoints = _build_watchpoints(
        review,
        trend,
    )

    trends = _build_trends(
        trend
    )

    conclusion = _build_conclusion(
        review,
        trend,
    )

    return DailyInvestorBrief(
        brief_date=review.review_date,
        portfolio_snapshot=portfolio_snapshot,
        changes=changes,
        persistent_actions=persistent_actions,
        persistent_opportunities=(
            persistent_opportunities
        ),
        watchpoints=watchpoints,
        trends=trends,
        conclusion=conclusion,
    )


def get_daily_investor_brief() -> DailyInvestorBrief:
    """
    Public service entry point for the daily investor brief.
    """

    return build_daily_investor_brief()