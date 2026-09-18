import json
from datetime import date
from pathlib import Path

from models.daily_review_snapshot import (
    DailyReviewSnapshot,
)

from services.daily_portfolio_review_service import (
    get_daily_portfolio_review,
)

from tools.serialization import to_python


# ==========================================================
# Snapshot Storage
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DAILY_REVIEW_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "daily_review_history"
)


def _ensure_daily_review_directory():
    """
    Create the daily review history directory if it
    does not already exist.
    """

    DAILY_REVIEW_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# Create
# ==========================================================

def create_daily_review_snapshot() -> DailyReviewSnapshot:
    """
    Generate a historical snapshot of the current
    FreedomIQ daily portfolio review.

    Reuses the existing Daily Portfolio Review engine.
    """

    review = get_daily_portfolio_review()

    return DailyReviewSnapshot(
        review_date=review.review_date,

        portfolio_status=to_python(
            review.portfolio_status
        ),

        changes=to_python(
            review.changes
        ),

        actions=to_python(
            review.actions
        ),

        opportunities=to_python(
            review.opportunities
        ),

        watchpoints=to_python(
            review.watchpoints
        ),

        conclusion=review.conclusion,
    )


# ==========================================================
# Save
# ==========================================================

def save_daily_review_snapshot(
    snapshot: DailyReviewSnapshot,
) -> Path:
    """
    Save a daily review snapshot as a JSON file.

    One review snapshot is stored per calendar day.

    Running the review multiple times on the same day
    replaces the existing record rather than creating
    duplicate files.
    """

    _ensure_daily_review_directory()

    snapshot_path = (
        DAILY_REVIEW_DIRECTORY
        / f"{snapshot.review_date}.json"
    )

    snapshot_data = to_python(
        snapshot
    )

    with snapshot_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            snapshot_data,
            file,
            indent=4,
        )

    return snapshot_path


# ==========================================================
# Load Specific Date
# ==========================================================

def load_daily_review_snapshot(
    review_date: str,
) -> DailyReviewSnapshot | None:
    """
    Load a daily review snapshot for a specific date.
    """

    snapshot_path = (
        DAILY_REVIEW_DIRECTORY
        / f"{review_date}.json"
    )

    if not snapshot_path.exists():
        return None

    with snapshot_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        snapshot_data = json.load(file)

    return DailyReviewSnapshot(
        **snapshot_data
    )


# ==========================================================
# Load Latest
# ==========================================================

def load_latest_daily_review_snapshot(
) -> DailyReviewSnapshot | None:
    """
    Load the most recent daily review snapshot.
    """

    _ensure_daily_review_directory()

    snapshot_files = sorted(
        DAILY_REVIEW_DIRECTORY.glob("*.json")
    )

    if not snapshot_files:
        return None

    latest_file = snapshot_files[-1]

    with latest_file.open(
        "r",
        encoding="utf-8",
    ) as file:

        snapshot_data = json.load(file)

    return DailyReviewSnapshot(
        **snapshot_data
    )


# ==========================================================
# Load Previous
# ==========================================================

def load_previous_daily_review_snapshot(
) -> DailyReviewSnapshot | None:
    """
    Load the daily review snapshot immediately before
    the most recent snapshot.
    """

    _ensure_daily_review_directory()

    snapshot_files = sorted(
        DAILY_REVIEW_DIRECTORY.glob("*.json")
    )

    if len(snapshot_files) < 2:
        return None

    previous_file = snapshot_files[-2]

    with previous_file.open(
        "r",
        encoding="utf-8",
    ) as file:

        snapshot_data = json.load(file)

    return DailyReviewSnapshot(
        **snapshot_data
    )


# ==========================================================
# History
# ==========================================================

def get_daily_review_history(
    limit: int = 7,
) -> list[DailyReviewSnapshot]:
    """
    Return recent daily review snapshots.

    Results are returned from newest to oldest.

    The limit prevents the history tool from returning
    an unnecessarily large amount of data.
    """

    if limit <= 0:
        raise ValueError(
            "History limit must be greater than zero."
        )

    _ensure_daily_review_directory()

    snapshot_files = sorted(
        DAILY_REVIEW_DIRECTORY.glob("*.json"),
        reverse=True,
    )

    snapshots = []

    for snapshot_file in snapshot_files[:limit]:

        with snapshot_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            snapshot_data = json.load(file)

        snapshots.append(
            DailyReviewSnapshot(
                **snapshot_data
            )
        )

    return snapshots