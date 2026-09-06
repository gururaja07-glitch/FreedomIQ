import json
from datetime import date
from pathlib import Path

from models.portfolio_snapshot import PortfolioSnapshot

from services.portfolio_service import get_dashboard_data

from services.portfolio_committee_service import (
    get_portfolio_investment_committee,
)

from tools.serialization import to_python

# ==========================================================
# Snapshot Storage
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SNAPSHOT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "portfolio_history"
)
def _ensure_snapshot_directory():
    """
    Create the portfolio snapshot directory if it
    does not already exist.
    """

    SNAPSHOT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )
def create_portfolio_snapshot() -> PortfolioSnapshot:
    """
    Create a historical snapshot of the current
    FreedomIQ portfolio intelligence.

    Reuses existing dashboard and committee analysis.
    """

    # ------------------------------------------------------
    # 1. Generate existing portfolio intelligence
    # ------------------------------------------------------

    dashboard = get_dashboard_data()

    committee = (
        get_portfolio_investment_committee()
    )

    # ------------------------------------------------------
    # 2. Build historical snapshot
    # ------------------------------------------------------

    snapshot = PortfolioSnapshot(
        snapshot_date=date.today().isoformat(),

        portfolio_summary=to_python(
            dashboard.summary
        ),

        portfolio_health=to_python(
            dashboard.health
        ),

        portfolio_risk=to_python(
            dashboard.risk
        ),

        committee_summary=committee.summary,

        committee_confidence=committee.confidence,

        quarterly_summary=committee.quarterly_summary,

        quarterly_assessment_counts=to_python(
            committee.quarterly_assessment_counts
        ),

        company_decisions=to_python(
            committee.company_decisions
        ),
    )

    return snapshot
def save_portfolio_snapshot(
    snapshot: PortfolioSnapshot,
) -> Path:
    """
    Save a portfolio snapshot as a JSON file.

    One snapshot is stored per calendar day.
    """

    _ensure_snapshot_directory()

    snapshot_path = (
        SNAPSHOT_DIRECTORY
        / f"{snapshot.snapshot_date}.json"
    )

    snapshot_data = to_python(snapshot)

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