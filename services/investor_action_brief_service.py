from models.investor_action_brief import InvestorActionBrief

from services.investor_decision_context_service import (
    get_investor_decision_context,
)


def _priority_rank(priority: str) -> int:
    return {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }.get(str(priority).upper(), 0)


def _build_attention_items(context) -> list[dict]:
    items = []

    for item in context.key_context:
        priority = str(item.get("priority", "")).upper()

        if priority not in {"CRITICAL", "HIGH"}:
            continue

        items.append(
            {
                "source": item.get("source", ""),
                "title": item.get("title", ""),
                "priority": item.get("priority", ""),
                "description": item.get("description", ""),
            }
        )

    items.sort(
        key=lambda item: (
            -_priority_rank(item["priority"]),
            item["source"],
            item["title"],
        )
    )

    return items


def _build_summary(
    context,
    attention_items: list[dict],
) -> str:
    status = context.portfolio_status

    health = status.get("Health Score")
    risk = status.get("Overall Risk")
    largest_holding = status.get("Largest Holding")
    largest_weight = status.get("Largest Weight")

    if attention_items:
        attention_text = (
            f"{len(attention_items)} high-priority item(s) "
            "deserve attention."
        )
    else:
        attention_text = "No critical or high-priority items require attention."

    return (
        f"Portfolio health is {health} with overall risk {risk}. "
        f"Largest holding is {largest_holding} at "
        f"{largest_weight}%. "
        f"{attention_text}"
    )


def build_investor_action_brief() -> InvestorActionBrief:
    context = get_investor_decision_context()

    attention_items = _build_attention_items(context)

    return InvestorActionBrief(
        brief_date=context.context_date,
        portfolio_status=context.portfolio_status,
        attention_items=attention_items,
        recent_changes=context.recent_changes,
        persistent_actions=context.persistent_actions,
        persistent_opportunities=context.persistent_opportunities,
        persistent_watchpoints=context.persistent_watchpoints,
        trends=context.trends,
        summary=_build_summary(
            context,
            attention_items,
        ),
    )


def get_investor_action_brief() -> InvestorActionBrief:
    return build_investor_action_brief()