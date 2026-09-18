from models.daily_review_change import (
    DailyReviewChange,
    DailyReviewChangeResult,
)

from models.daily_review_snapshot import (
    DailyReviewSnapshot,
)

from services.daily_review_snapshot_service import (
    load_latest_daily_review_snapshot,
    load_previous_daily_review_snapshot,
)


# ==========================================================
# Helpers
# ==========================================================

def _priority_rank(priority: str) -> int:
    """
    Return a numeric rank for change priority.
    """

    return {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }.get(
        priority.upper(),
        0,
    )


def _get_highest_priority(
    first: str,
    second: str,
) -> str:
    """
    Return the higher of two priorities.
    """

    if _priority_rank(first) >= _priority_rank(second):
        return first

    return second


def _index_items(
    items: list[dict],
) -> dict[str, dict]:
    """
    Index review items by title.

    Daily review titles are treated as the stable
    identifier for comparison.
    """

    return {
        item["title"]: item
        for item in items
        if item.get("title")
    }


# ==========================================================
# Review Item Comparison
# ==========================================================

def _compare_review_items(
    previous_items: list[dict],
    current_items: list[dict],
    category: str,
) -> list[DailyReviewChange]:
    """
    Compare two groups of daily review items.

    Detects:
    - newly appearing items
    - removed items
    - priority changes

    Unchanged items are ignored.
    """

    changes = []

    previous = _index_items(
        previous_items
    )

    current = _index_items(
        current_items
    )

    previous_titles = set(previous)
    current_titles = set(current)

    # ------------------------------------------------------
    # New items
    # ------------------------------------------------------

    for title in sorted(
        current_titles - previous_titles
    ):

        item = current[title]

        priority = item.get(
            "priority",
            "MEDIUM",
        )

        changes.append(
            DailyReviewChange(
                category=category,
                title=title,
                previous_value="Not present",
                current_value=item.get(
                    "description",
                    "Present",
                ),
                priority=priority,
                description=(
                    f"New {category.lower()} identified: "
                    f"{title}."
                ),
            )
        )

    # ------------------------------------------------------
    # Removed items
    # ------------------------------------------------------

    for title in sorted(
        previous_titles - current_titles
    ):

        item = previous[title]

        priority = item.get(
            "priority",
            "MEDIUM",
        )

        changes.append(
            DailyReviewChange(
                category=category,
                title=title,
                previous_value=item.get(
                    "description",
                    "Present",
                ),
                current_value="Not present",
                priority=priority,
                description=(
                    f"{category} no longer appears: "
                    f"{title}."
                ),
            )
        )

    # ------------------------------------------------------
    # Priority changes
    # ------------------------------------------------------

    for title in sorted(
        previous_titles & current_titles
    ):

        previous_priority = previous[title].get(
            "priority"
        )

        current_priority = current[title].get(
            "priority"
        )

        if (
            previous_priority is None
            or current_priority is None
        ):
            continue

        if previous_priority == current_priority:
            continue

        priority = _get_highest_priority(
            previous_priority,
            current_priority,
        )

        changes.append(
            DailyReviewChange(
                category=category,
                title=title,
                previous_value=previous_priority,
                current_value=current_priority,
                priority=priority,
                description=(
                    f"{category} priority changed "
                    f"from {previous_priority} to "
                    f"{current_priority} for {title}."
                ),
            )
        )

    return changes


# ==========================================================
# Portfolio Status Comparison
# ==========================================================

def _compare_portfolio_status(
    previous: DailyReviewSnapshot,
    current: DailyReviewSnapshot,
) -> list[DailyReviewChange]:
    """
    Compare important portfolio status fields.

    Only meaningful status changes are reported.
    """

    changes = []

    previous_status = previous.portfolio_status
    current_status = current.portfolio_status

    fields = (
        (
            "Portfolio Health",
            "Health",
            "MEDIUM",
        ),
        (
            "Overall Risk",
            "Overall Risk",
            "MEDIUM",
        ),
        (
            "Largest Holding",
            "Largest Holding",
            "MEDIUM",
        ),
        (
            "Largest Holding Weight",
            "Largest Weight",
            "MEDIUM",
        ),
    )

    for category, field, priority in fields:

        previous_value = previous_status.get(
            field
        )

        current_value = current_status.get(
            field
        )

        if (
            previous_value is None
            or current_value is None
        ):
            continue

        if previous_value == current_value:
            continue

        changes.append(
            DailyReviewChange(
                category=category,
                title=category,
                previous_value=str(
                    previous_value
                ),
                current_value=str(
                    current_value
                ),
                priority=priority,
                description=(
                    f"{category} changed from "
                    f"{previous_value} to "
                    f"{current_value}."
                ),
            )
        )

    return changes


# ==========================================================
# Compare Two Reviews
# ==========================================================

def compare_daily_reviews(
    previous: DailyReviewSnapshot,
    current: DailyReviewSnapshot,
) -> DailyReviewChangeResult:
    """
    Compare two persisted daily portfolio reviews.
    """

    changes = []

    changes.extend(
        _compare_portfolio_status(
            previous,
            current,
        )
    )

    changes.extend(
        _compare_review_items(
            previous.actions,
            current.actions,
            "Action",
        )
    )

    changes.extend(
        _compare_review_items(
            previous.opportunities,
            current.opportunities,
            "Opportunity",
        )
    )

    changes.extend(
        _compare_review_items(
            previous.watchpoints,
            current.watchpoints,
            "Watchpoint",
        )
    )

    changes.sort(
        key=lambda change: (
            -_priority_rank(
                change.priority
            ),
            change.category,
            change.title,
        )
    )

    change_count = len(changes)

    if change_count == 0:
        summary = (
            "No meaningful daily review changes detected."
        )

    elif change_count == 1:
        summary = (
            "1 meaningful daily review change detected."
        )

    else:
        summary = (
            f"{change_count} meaningful daily review "
            "changes detected."
        )

    return DailyReviewChangeResult(
        previous_date=previous.review_date,
        current_date=current.review_date,
        changes=changes,
        summary=summary,
    )


# ==========================================================
# Compare Latest and Previous
# ==========================================================

def get_daily_review_changes() -> DailyReviewChangeResult | None:
    """
    Compare the latest persisted daily review with
    the immediately preceding persisted review.

    Returns None when fewer than two reviews exist.
    """

    previous = load_previous_daily_review_snapshot()
    current = load_latest_daily_review_snapshot()

    if (
        previous is None
        or current is None
    ):
        return None

    return compare_daily_reviews(
        previous,
        current,
    )