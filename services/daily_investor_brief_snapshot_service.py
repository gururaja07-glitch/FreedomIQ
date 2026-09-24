from pathlib import Path
import json

from models.daily_investor_brief import (
    DailyInvestorBrief,
)

from models.daily_investor_brief_snapshot import (
    DailyInvestorBriefSnapshot,
)

from services.daily_investor_brief_service import (
    get_daily_investor_brief,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INVESTOR_BRIEF_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "investor_brief_history"
)


def _ensure_directory() -> None:
    """
    Ensure the investor brief history directory exists.
    """

    INVESTOR_BRIEF_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )


def create_daily_investor_brief_snapshot(
    brief: DailyInvestorBrief,
) -> DailyInvestorBriefSnapshot:
    """
    Convert a DailyInvestorBrief into a persisted
    historical snapshot.
    """

    return DailyInvestorBriefSnapshot(
        brief_date=brief.brief_date,
        portfolio_snapshot=brief.portfolio_snapshot,
        changes=brief.changes,
        persistent_actions=brief.persistent_actions,
        persistent_opportunities=(
            brief.persistent_opportunities
        ),
        watchpoints=brief.watchpoints,
        trends=brief.trends,
        conclusion=brief.conclusion,
    )


def save_daily_investor_brief_snapshot(
    snapshot: DailyInvestorBriefSnapshot,
) -> DailyInvestorBriefSnapshot:
    """
    Save a daily investor brief snapshot.

    The snapshot filename is based on the brief date.
    Saving the same date again overwrites the existing
    snapshot.
    """

    _ensure_directory()

    file_path = (
        INVESTOR_BRIEF_DIRECTORY
        / f"{snapshot.brief_date}.json"
    )

    data = {
        "brief_date": snapshot.brief_date,
        "portfolio_snapshot": snapshot.portfolio_snapshot,
        "changes": snapshot.changes,
        "persistent_actions": (
            snapshot.persistent_actions
        ),
        "persistent_opportunities": (
            snapshot.persistent_opportunities
        ),
        "watchpoints": snapshot.watchpoints,
        "trends": snapshot.trends,
        "conclusion": snapshot.conclusion,
    }

    with file_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
            default=str,
        )

    return snapshot


def save_current_daily_investor_brief() -> (
    DailyInvestorBriefSnapshot
):
    """
    Generate the current daily investor brief,
    convert it into a historical snapshot, and save it.
    """

    brief = get_daily_investor_brief()

    snapshot = create_daily_investor_brief_snapshot(
        brief
    )

    return save_daily_investor_brief_snapshot(
        snapshot
    )


def load_daily_investor_brief_snapshot(
    brief_date: str,
) -> DailyInvestorBriefSnapshot | None:
    """
    Load a persisted investor brief snapshot by date.
    """

    file_path = (
        INVESTOR_BRIEF_DIRECTORY
        / f"{brief_date}.json"
    )

    if not file_path.exists():
        return None

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return DailyInvestorBriefSnapshot(
        brief_date=data["brief_date"],
        portfolio_snapshot=data[
            "portfolio_snapshot"
        ],
        changes=data["changes"],
        persistent_actions=data[
            "persistent_actions"
        ],
        persistent_opportunities=data[
            "persistent_opportunities"
        ],
        watchpoints=data["watchpoints"],
        trends=data["trends"],
        conclusion=data["conclusion"],
    )


def load_latest_daily_investor_brief_snapshot() -> (
    DailyInvestorBriefSnapshot | None
):
    """
    Load the most recent persisted investor brief.
    """

    _ensure_directory()

    files = sorted(
        INVESTOR_BRIEF_DIRECTORY.glob("*.json"),
        reverse=True,
    )

    if not files:
        return None

    return load_daily_investor_brief_snapshot(
        files[0].stem
    )


def load_previous_daily_investor_brief_snapshot() -> (
    DailyInvestorBriefSnapshot | None
):
    """
    Load the second most recent persisted investor brief.
    """

    _ensure_directory()

    files = sorted(
        INVESTOR_BRIEF_DIRECTORY.glob("*.json"),
        reverse=True,
    )

    if len(files) < 2:
        return None

    return load_daily_investor_brief_snapshot(
        files[1].stem
    )


def get_daily_investor_brief_history(
    limit: int = 7,
) -> list[DailyInvestorBriefSnapshot]:
    """
    Return the most recent investor brief snapshots.

    Results are ordered newest to oldest.
    """

    if limit <= 0:
        raise ValueError(
            "Investor brief history limit must be greater than zero."
        )

    _ensure_directory()

    files = sorted(
        INVESTOR_BRIEF_DIRECTORY.glob("*.json"),
        reverse=True,
    )

    snapshots = []

    for file_path in files[:limit]:

        snapshot = (
            load_daily_investor_brief_snapshot(
                file_path.stem
            )
        )

        if snapshot is not None:
            snapshots.append(snapshot)

    return snapshots