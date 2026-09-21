from collections import defaultdict

from models.daily_review_snapshot import (
    DailyReviewSnapshot,
)

from models.daily_review_trend import (
    DailyReviewTrend,
    PersistentReviewItem,
)

from services.daily_review_snapshot_service import (
    get_daily_review_history,
)


# ==========================================================
# Helpers
# ==========================================================

def _trend_direction(
    values: list[float],
) -> str:
    """
    Determine the historical direction of a numeric series.

    Reviews are expected in chronological order.
    """

    if len(values) < 2:
        return "Insufficient data"

    increasing = all(
        current > previous
        for previous, current in zip(
            values,
            values[1:],
        )
    )

    decreasing = all(
        current < previous
        for previous, current in zip(
            values,
            values[1:],
        )
    )

    if increasing:
        return "Improving"

    if decreasing:
        return "Declining"

    return "Stable"


def _risk_rank(
    risk: str,
) -> int | None:
    """
    Convert portfolio risk level to an ordinal value.

    Used only to determine historical direction.
    """

    normalized = risk.upper()

    if "LOW" in normalized:
        return 1

    if "MEDIUM" in normalized:
        return 2

    if "HIGH" in normalized:
        return 3

    return None


def _risk_trend(
    snapshots: list[DailyReviewSnapshot],
) -> str:
    """
    Determine the historical direction of portfolio risk.
    """

    values = []

    for snapshot in snapshots:

        risk = snapshot.portfolio_status.get(
            "Overall Risk"
        )

        if risk is None:
            continue

        rank = _risk_rank(str(risk))

        if rank is not None:
            values.append(rank)

    if len(values) < 2:
        return "Insufficient data"

    increasing = all(
        current > previous
        for previous, current in zip(
            values,
            values[1:],
        )
    )

    decreasing = all(
        current < previous
        for previous, current in zip(
            values,
            values[1:],
        )
    )

    if increasing:
        return "Increasing"

    if decreasing:
        return "Decreasing"

    return "Stable"


def _get_numeric_series(
    snapshots: list[DailyReviewSnapshot],
    field: str,
) -> list[float]:
    """
    Extract a numeric portfolio-status series.
    """

    values = []

    for snapshot in snapshots:

        value = snapshot.portfolio_status.get(
            field
        )

        if value is None:
            continue

        try:
            values.append(float(value))
        except (
            TypeError,
            ValueError,
        ):
            continue

    return values


# ==========================================================
# Persistent Review Items
# ==========================================================

def _calculate_consecutive_count(
    appearances: list[int],
    total_reviews: int,
) -> int:
    """
    Calculate consecutive appearances ending at
    the latest review.

    Appearance indexes are chronological.
    """

    if not appearances:
        return 0

    latest_index = total_reviews - 1

    if appearances[-1] != latest_index:
        return 0

    count = 1

    for index in range(
        len(appearances) - 1,
        0,
        -1,
    ):

        if (
            appearances[index]
            == appearances[index - 1] + 1
        ):
            count += 1
        else:
            break

    return count


def _build_persistent_items(
    snapshots: list[DailyReviewSnapshot],
    category: str,
    minimum_reviews: int = 2,
) -> list[PersistentReviewItem]:
    """
    Identify review items appearing repeatedly
    across the historical window.
    """

    occurrences = defaultdict(list)

    total_reviews = len(snapshots)

    for index, snapshot in enumerate(
        snapshots
    ):

        if category == "Action":
            items = snapshot.actions

        elif category == "Opportunity":
            items = snapshot.opportunities

        elif category == "Watchpoint":
            items = snapshot.watchpoints

        else:
            continue

        seen_titles = set()

        for item in items:

            title = item.get("title")

            if not title or title in seen_titles:
                continue

            seen_titles.add(title)

            occurrences[title].append(
                (
                    index,
                    snapshot.review_date,
                    item.get(
                        "priority",
                        "MEDIUM",
                    ),
                )
            )

    persistent_items = []

    for title, appearances in occurrences.items():

        if len(appearances) < minimum_reviews:
            continue

        indexes = [
            appearance[0]
            for appearance in appearances
        ]

        first_seen = appearances[0][1]
        last_seen = appearances[-1][1]

        consecutive_count = (
            _calculate_consecutive_count(
                indexes,
                total_reviews,
            )
        )

        priority = appearances[-1][2]

        persistent_items.append(
            PersistentReviewItem(
                category=category,
                title=title,
                review_count=len(appearances),
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


# ==========================================================
# Summary
# ==========================================================

def _build_summary(
    trend: DailyReviewTrend,
) -> str:
    """
    Build a deterministic historical trend summary.
    """

    parts = [
        (
            f"Portfolio health: "
            f"{trend.health_trend}."
        ),
        (
            f"Portfolio risk: "
            f"{trend.risk_trend}."
        ),
        (
            f"Largest holding weight: "
            f"{trend.largest_holding_weight_trend}."
        ),
    ]

    persistent_count = (
        len(trend.persistent_actions)
        + len(trend.persistent_opportunities)
        + len(trend.persistent_watchpoints)
    )

    if persistent_count:
        parts.append(
            f"{persistent_count} persistent "
            "review item(s) identified."
        )
    else:
        parts.append(
            "No persistent review items identified."
        )

    return " ".join(parts)


# ==========================================================
# Main Trend Analysis
# ==========================================================

def analyze_daily_review_trends(
    snapshots: list[DailyReviewSnapshot],
) -> DailyReviewTrend | None:
    """
    Analyze historical daily reviews.

    Snapshots may be supplied in newest-to-oldest order
    or chronological order; they are normalized internally.

    Returns None when no reviews are available.
    """

    if not snapshots:
        return None

    snapshots = sorted(
        snapshots,
        key=lambda snapshot: snapshot.review_date,
    )

    health_values = _get_numeric_series(
        snapshots,
        "Health",
    )

    largest_weight_values = _get_numeric_series(
        snapshots,
        "Largest Weight",
    )

    health_trend = _trend_direction(
        health_values
    )

    largest_holding_weight_trend = (
        _trend_direction(
            largest_weight_values
        )
    )

    risk_trend = _risk_trend(
        snapshots
    )

    persistent_actions = (
        _build_persistent_items(
            snapshots,
            "Action",
        )
    )

    persistent_opportunities = (
        _build_persistent_items(
            snapshots,
            "Opportunity",
        )
    )

    persistent_watchpoints = (
        _build_persistent_items(
            snapshots,
            "Watchpoint",
        )
    )

    trend = DailyReviewTrend(
        review_count=len(snapshots),

        start_date=snapshots[0].review_date,

        end_date=snapshots[-1].review_date,

        health_trend=health_trend,

        risk_trend=risk_trend,

        largest_holding_weight_trend=(
            largest_holding_weight_trend
        ),

        persistent_actions=persistent_actions,

        persistent_opportunities=(
            persistent_opportunities
        ),

        persistent_watchpoints=(
            persistent_watchpoints
        ),

        summary="",
    )

    trend.summary = _build_summary(
        trend
    )

    return trend


# ==========================================================
# Historical Reviews
# ==========================================================

def get_daily_review_trends(
    limit: int = 7,
) -> DailyReviewTrend | None:
    """
    Analyze the most recent persisted daily reviews.
    """

    if limit <= 0:
        raise ValueError(
            "Trend history limit must be greater than zero."
        )

    snapshots = get_daily_review_history(
        limit
    )

    return analyze_daily_review_trends(
        snapshots
    )