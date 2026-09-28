from models.investor_decision_context import InvestorDecisionContext

from services.daily_investor_brief_service import get_daily_investor_brief
from services.daily_investor_brief_change_service import (
    get_daily_investor_brief_changes,
)
from services.daily_investor_brief_trend_service import (
    get_daily_investor_brief_trends,
)


def _priority_rank(priority: str) -> int:
    return {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }.get(str(priority).upper(), 0)


def _build_recent_changes(changes) -> list[dict]:
    if not changes:
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
        for change in changes
    ]


def _build_persistent_items(items) -> list[dict]:
    if not items:
        return []

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


def _build_trends(trend) -> dict:
    if trend is None:
        return {}

    return {
        "review_count": trend.review_count,
        "start_date": trend.start_date,
        "end_date": trend.end_date,
        "health_trend": trend.health_trend,
        "risk_trend": trend.risk_trend,
        "largest_holding_weight_trend": trend.largest_holding_weight_trend,
    }


def _add_key_context(
    key_context: list[dict],
    source: str,
    item,
) -> None:
    priority = str(item.priority).upper()

    if priority not in {"CRITICAL", "HIGH"}:
        return

    key_context.append(
        {
            "source": source,
            "title": item.title,
            "priority": item.priority,
            "description": getattr(item, "description", ""),
        }
    )


def _build_key_context(
    recent_changes,
    persistent_actions,
    persistent_opportunities,
    persistent_watchpoints,
    trend,
) -> list[dict]:
    key_context: list[dict] = []

    for change in recent_changes or []:
        _add_key_context(key_context, "recent_change", change)

    for item in persistent_actions or []:
        _add_key_context(key_context, "persistent_action", item)

    for item in persistent_opportunities or []:
        _add_key_context(key_context, "persistent_opportunity", item)

    for item in persistent_watchpoints or []:
        _add_key_context(key_context, "persistent_watchpoint", item)

    if trend is not None:
        trend_items = [
            (
                "health_trend",
                trend.health_trend,
            ),
            (
                "risk_trend",
                trend.risk_trend,
            ),
            (
                "largest_holding_weight_trend",
                trend.largest_holding_weight_trend,
            ),
        ]

        for name, value in trend_items:
            if value not in {"Improving", "Declining"}:
                continue

            key_context.append(
                {
                    "source": "trend",
                    "title": name,
                    "priority": "HIGH",
                    "description": f"{name.replace('_', ' ').title()}: {value}",
                }
            )

    key_context.sort(
        key=lambda item: (
            -_priority_rank(item["priority"]),
            item["source"],
            item["title"],
        )
    )

    return key_context


def build_investor_decision_context() -> InvestorDecisionContext:
    brief = get_daily_investor_brief()
    changes = get_daily_investor_brief_changes()
    trend = get_daily_investor_brief_trends(7)

    if trend is not None:
        trend_obj = trend
    else:
        trend_obj = None

    recent_changes = changes.changes if changes else []

    persistent_actions = (
        trend_obj.persistent_actions if trend_obj else []
    )

    persistent_opportunities = (
        trend_obj.persistent_opportunities if trend_obj else []
    )

    persistent_watchpoints = (
        trend_obj.persistent_watchpoints if trend_obj else []
    )

    return InvestorDecisionContext(
        context_date=brief.brief_date,
        portfolio_status=brief.portfolio_snapshot,
        recent_changes=_build_recent_changes(recent_changes),
        persistent_actions=_build_persistent_items(persistent_actions),
        persistent_opportunities=_build_persistent_items(
            persistent_opportunities
        ),
        persistent_watchpoints=_build_persistent_items(
            persistent_watchpoints
        ),
        trends=_build_trends(trend_obj),
        key_context=_build_key_context(
            recent_changes,
            persistent_actions,
            persistent_opportunities,
            persistent_watchpoints,
            trend_obj,
        ),
    )


def get_investor_decision_context() -> InvestorDecisionContext:
    return build_investor_decision_context()
