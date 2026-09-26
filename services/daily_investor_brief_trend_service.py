from models.daily_investor_brief_snapshot import DailyInvestorBriefSnapshot
from models.daily_investor_brief_trend import (
    DailyInvestorBriefTrend,
    PersistentInvestorBriefItem,
)
from services.daily_investor_brief_snapshot_service import (
    get_daily_investor_brief_history,
)


def _trend_direction(values: list[float]) -> str:
    if len(values) < 2:
        return "Insufficient data"

    if all(
        current > previous
        for previous, current in zip(values, values[1:])
    ):
        return "Improving"

    if all(
        current < previous
        for previous, current in zip(values, values[1:])
    ):
        return "Declining"

    return "Stable"


def _risk_rank(risk: str) -> int:
    normalized = risk.upper()

    if "LOW" in normalized:
        return 1

    if "MEDIUM" in normalized:
        return 2

    if "HIGH" in normalized:
        return 3

    return 0


def _risk_trend(values: list[str]) -> str:
    if len(values) < 2:
        return "Insufficient data"

    ranks = [_risk_rank(value) for value in values]

    if 0 in ranks:
        return "Insufficient data"

    if all(
        current < previous
        for previous, current in zip(ranks, ranks[1:])
    ):
        return "Improving"

    if all(
        current > previous
        for previous, current in zip(ranks, ranks[1:])
    ):
        return "Declining"

    return "Stable"


def _get_numeric_series(
    snapshots: list[DailyInvestorBriefSnapshot],
    field: str,
) -> list[float]:
    values = []

    for snapshot in snapshots:
        value = snapshot.portfolio_snapshot.get(field)

        try:
            values.append(float(value))
        except (TypeError, ValueError):
            continue

    return values


def _calculate_consecutive_count(
    snapshots: list[DailyInvestorBriefSnapshot],
    category: str,
    title: str,
) -> int:
    count = 0

    for snapshot in snapshots:
        items = getattr(
            snapshot,
            category,
            [],
        )

        titles = {
            item.get("title")
            for item in items
            if item.get("title")
        }

        if title in titles:
            count += 1
        else:
            break

    return count


def _build_persistent_items(
    snapshots: list[DailyInvestorBriefSnapshot],
    category: str,
    minimum_occurrences: int = 2,
) -> list[PersistentInvestorBriefItem]:
    occurrences: dict[str, list[tuple[str, str]]] = {}

    for snapshot in reversed(snapshots):
        items = getattr(
            snapshot,
            category,
            [],
        )

        seen_titles = set()

        for item in items:
            title = item.get("title")

            if not title or title in seen_titles:
                continue

            seen_titles.add(title)

            occurrences.setdefault(
                title,
                [],
            ).append(
                (
                    snapshot.brief_date,
                    item.get("priority", "MEDIUM"),
                )
            )

    persistent_items = []

    for title, records in occurrences.items():
        if len(records) < minimum_occurrences:
            continue

        first_seen = records[0][0]
        last_seen = records[-1][0]

        priorities = [
            priority
            for _, priority in records
            if priority
        ]

        priority_rank = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "CRITICAL": 4,
        }

        priority = max(
            priorities,
            key=lambda value: priority_rank.get(
                value.upper(),
                0,
            ),
        )

        consecutive_count = _calculate_consecutive_count(
            list(reversed(snapshots)),
            category,
            title,
        )

        persistent_items.append(
            PersistentInvestorBriefItem(
                category=category,
                title=title,
                review_count=len(records),
                consecutive_count=consecutive_count,
                first_seen=first_seen,
                last_seen=last_seen,
                priority=priority,
            )
        )

    persistent_items.sort(
        key=lambda item: (
            -item.consecutive_count,
            -item.review_count,
            item.title,
        )
    )

    return persistent_items


def _build_summary(
    review_count: int,
    health_trend: str,
    risk_trend: str,
    weight_trend: str,
    actions: list[PersistentInvestorBriefItem],
    opportunities: list[PersistentInvestorBriefItem],
    watchpoints: list[PersistentInvestorBriefItem],
) -> str:
    if review_count < 2:
        return (
            "Insufficient historical data to identify "
            "persistent investor brief trends."
        )

    return (
        f"Across {review_count} investor brief review(s), "
        f"health is {health_trend}, risk is {risk_trend}, "
        f"and largest holding weight is {weight_trend}. "
        f"{len(actions)} persistent action(s), "
        f"{len(opportunities)} persistent opportunit"
        f"{'y' if len(opportunities) == 1 else 'ies'}, "
        f"and {len(watchpoints)} persistent watchpoint(s) "
        f"were identified."
    )


def analyze_daily_investor_brief_trends(
    snapshots: list[DailyInvestorBriefSnapshot],
) -> DailyInvestorBriefTrend:
    if not snapshots:
        return DailyInvestorBriefTrend(
            review_count=0,
            start_date="",
            end_date="",
            health_trend="Insufficient data",
            risk_trend="Insufficient data",
            largest_holding_weight_trend="Insufficient data",
            persistent_actions=[],
            persistent_opportunities=[],
            persistent_watchpoints=[],
            summary="No investor brief history available.",
        )

    ordered_snapshots = sorted(
        snapshots,
        key=lambda snapshot: snapshot.brief_date,
    )

    health_values = _get_numeric_series(
        ordered_snapshots,
        "Health Score",
    )

    weight_values = _get_numeric_series(
        ordered_snapshots,
        "Largest Weight",
    )

    risk_values = [
        snapshot.portfolio_snapshot.get(
            "Overall Risk",
            "",
        )
        for snapshot in ordered_snapshots
    ]

    persistent_actions = _build_persistent_items(
        ordered_snapshots,
        "persistent_actions",
    )

    persistent_opportunities = _build_persistent_items(
        ordered_snapshots,
        "persistent_opportunities",
    )

    persistent_watchpoints = _build_persistent_items(
        ordered_snapshots,
        "watchpoints",
    )

    health_trend = _trend_direction(
        health_values
    )

    risk_trend = _risk_trend(
        risk_values
    )

    weight_trend = _trend_direction(
        weight_values
    )

    summary = _build_summary(
        len(ordered_snapshots),
        health_trend,
        risk_trend,
        weight_trend,
        persistent_actions,
        persistent_opportunities,
        persistent_watchpoints,
    )

    return DailyInvestorBriefTrend(
        review_count=len(ordered_snapshots),
        start_date=ordered_snapshots[0].brief_date,
        end_date=ordered_snapshots[-1].brief_date,
        health_trend=health_trend,
        risk_trend=risk_trend,
        largest_holding_weight_trend=weight_trend,
        persistent_actions=persistent_actions,
        persistent_opportunities=persistent_opportunities,
        persistent_watchpoints=persistent_watchpoints,
        summary=summary,
    )


def get_daily_investor_brief_trends(
    limit: int = 7,
) -> DailyInvestorBriefTrend:
    if limit <= 0:
        raise ValueError(
            "Investor brief trend history limit must be greater than zero."
        )

    snapshots = get_daily_investor_brief_history(
        limit
    )

    return analyze_daily_investor_brief_trends(
        snapshots
    )