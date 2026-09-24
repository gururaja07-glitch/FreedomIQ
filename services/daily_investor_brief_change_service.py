from models.daily_investor_brief_change import (
    DailyInvestorBriefChange,
    DailyInvestorBriefChangeResult,
)
from models.daily_investor_brief_snapshot import DailyInvestorBriefSnapshot
from services.daily_investor_brief_snapshot_service import (
    load_latest_daily_investor_brief_snapshot,
    load_previous_daily_investor_brief_snapshot,
)


PRIORITY_RANK = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}


def _priority_rank(priority: str) -> int:
    return PRIORITY_RANK.get(priority.upper(), 0)


def _get_highest_priority(*priorities: str) -> str:
    valid_priorities = [
        priority.upper()
        for priority in priorities
        if priority
    ]

    if not valid_priorities:
        return "LOW"

    return max(
        valid_priorities,
        key=_priority_rank,
    )


def _index_items(items: list[dict]) -> dict[str, dict]:
    return {
        item["title"]: item
        for item in items
        if item.get("title")
    }


def _compare_items(
    category: str,
    previous_items: list[dict],
    current_items: list[dict],
) -> list[DailyInvestorBriefChange]:
    changes = []

    previous = _index_items(previous_items)
    current = _index_items(current_items)

    all_titles = sorted(
        set(previous) | set(current)
    )

    for title in all_titles:
        previous_item = previous.get(title)
        current_item = current.get(title)

        if previous_item is None:
            changes.append(
                DailyInvestorBriefChange(
                    category=category,
                    title=title,
                    previous_value="Not present",
                    current_value=current_item.get(
                        "priority",
                        "Present",
                    ),
                    priority=current_item.get(
                        "priority",
                        "MEDIUM",
                    ),
                    description=f"New {category.lower()} item appeared.",
                )
            )
            continue

        if current_item is None:
            changes.append(
                DailyInvestorBriefChange(
                    category=category,
                    title=title,
                    previous_value=previous_item.get(
                        "priority",
                        "Present",
                    ),
                    current_value="Not present",
                    priority=previous_item.get(
                        "priority",
                        "MEDIUM",
                    ),
                    description=f"{category} item is no longer present.",
                )
            )
            continue

        previous_priority = previous_item.get(
            "priority",
            "MEDIUM",
        )
        current_priority = current_item.get(
            "priority",
            "MEDIUM",
        )

        if previous_priority != current_priority:
            priority = _get_highest_priority(
                previous_priority,
                current_priority,
            )

            changes.append(
                DailyInvestorBriefChange(
                    category=category,
                    title=title,
                    previous_value=previous_priority,
                    current_value=current_priority,
                    priority=priority,
                    description=(
                        f"{category} priority changed from "
                        f"{previous_priority} to "
                        f"{current_priority}."
                    ),
                )
            )

    return changes


def _compare_portfolio_snapshot(
    previous: dict,
    current: dict,
) -> list[DailyInvestorBriefChange]:
    changes = []

    fields = [
        ("Health Score", "Portfolio Health"),
        ("Overall Risk", "Overall Risk"),
        ("Largest Holding", "Largest Holding"),
        ("Largest Weight", "Largest Holding Weight"),
        ("Portfolio Return", "Portfolio Return"),
        ("Current Value", "Current Value"),
        ("Profit", "Portfolio Profit"),
    ]

    for field, title in fields:
        previous_value = previous.get(field)
        current_value = current.get(field)

        if previous_value == current_value:
            continue

        priority = "MEDIUM"

        if field == "Health Score":
            priority = "HIGH"

        elif field == "Overall Risk":
            priority = "HIGH"

        elif field == "Largest Weight":
            try:
                difference = abs(
                    float(current_value)
                    - float(previous_value)
                )

                if difference >= 5:
                    priority = "HIGH"
                elif difference >= 1:
                    priority = "MEDIUM"
                else:
                    continue
            except (TypeError, ValueError):
                priority = "MEDIUM"

        changes.append(
            DailyInvestorBriefChange(
                category="Portfolio",
                title=title,
                previous_value=str(previous_value),
                current_value=str(current_value),
                priority=priority,
                description=(
                    f"{title} changed from "
                    f"{previous_value} to "
                    f"{current_value}."
                ),
            )
        )

    return changes


def _compare_trends(
    previous: dict,
    current: dict,
) -> list[DailyInvestorBriefChange]:
    changes = []

    fields = [
        ("health", "Health Trend"),
        ("risk", "Risk Trend"),
        (
            "largest_holding_weight",
            "Largest Holding Weight Trend",
        ),
    ]

    for field, title in fields:
        previous_value = previous.get(field)
        current_value = current.get(field)

        if previous_value == current_value:
            continue

        changes.append(
            DailyInvestorBriefChange(
                category="Trend",
                title=title,
                previous_value=str(previous_value),
                current_value=str(current_value),
                priority="MEDIUM",
                description=(
                    f"{title} changed from "
                    f"{previous_value} to "
                    f"{current_value}."
                ),
            )
        )

    return changes


def compare_daily_investor_briefs(
    previous: DailyInvestorBriefSnapshot,
    current: DailyInvestorBriefSnapshot,
) -> DailyInvestorBriefChangeResult:
    changes = []

    changes.extend(
        _compare_portfolio_snapshot(
            previous.portfolio_snapshot,
            current.portfolio_snapshot,
        )
    )

    changes.extend(
        _compare_items(
            "Action",
            previous.changes,
            current.changes,
        )
    )

    changes.extend(
        _compare_items(
            "Persistent Action",
            previous.persistent_actions,
            current.persistent_actions,
        )
    )

    changes.extend(
        _compare_items(
            "Persistent Opportunity",
            previous.persistent_opportunities,
            current.persistent_opportunities,
        )
    )

    changes.extend(
        _compare_items(
            "Watchpoint",
            previous.watchpoints,
            current.watchpoints,
        )
    )

    changes.extend(
        _compare_trends(
            previous.trends,
            current.trends,
        )
    )

    changes.sort(
        key=lambda change: (
            -_priority_rank(change.priority),
            change.category,
            change.title,
        )
    )

    if not changes:
        summary = "No meaningful changes detected."

    else:
        summary = (
            f"{len(changes)} meaningful change(s) "
            "detected between the two investor briefs."
        )

    return DailyInvestorBriefChangeResult(
        previous_date=previous.brief_date,
        current_date=current.brief_date,
        changes=changes,
        summary=summary,
    )


def get_daily_investor_brief_changes() -> (
    DailyInvestorBriefChangeResult | None
):
    current = load_latest_daily_investor_brief_snapshot()
    previous = load_previous_daily_investor_brief_snapshot()

    if current is None or previous is None:
        return None

    return compare_daily_investor_briefs(
        previous,
        current,
    )