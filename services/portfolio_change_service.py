from models.portfolio_change import (
    PortfolioChange,
    PortfolioChangeResult,
)

from models.portfolio_snapshot import (
    PortfolioSnapshot,
)
from services.portfolio_snapshot_service import (
    create_portfolio_snapshot,
    load_latest_snapshot,
)

def _index_company_decisions(
    snapshot: PortfolioSnapshot,
) -> dict:
    """
    Create a company lookup dictionary from
    snapshot company decisions.
    """

    return {
        decision["company"]: decision
        for decision in snapshot.company_decisions
    }


def _get_decision_change_priority(
    previous_decision: str,
    current_decision: str,
) -> str:
    """
    Determine the materiality of an investment
    decision change.
    """

    critical_changes = {
        ("ADD", "SELL"),
        ("HOLD", "SELL"),
    }

    high_changes = {
        ("ADD", "REDUCE"),
        ("HOLD", "REDUCE"),
        ("ADD", "HOLD"),
    }

    if (
        previous_decision,
        current_decision,
    ) in critical_changes:

        return "CRITICAL"

    if (
        previous_decision,
        current_decision,
    ) in high_changes:

        return "HIGH"

    return "MEDIUM"


def _detect_decision_changes(
    previous: PortfolioSnapshot,
    current: PortfolioSnapshot,
) -> list[PortfolioChange]:
    """
    Detect changes in company investment decisions.
    """

    changes = []

    previous_decisions = (
        _index_company_decisions(previous)
    )

    current_decisions = (
        _index_company_decisions(current)
    )

    common_companies = (
        previous_decisions.keys()
        & current_decisions.keys()
    )

    for company in sorted(common_companies):

        previous_decision = (
            previous_decisions[company]["decision"]
        )

        current_decision = (
            current_decisions[company]["decision"]
        )

        if previous_decision == current_decision:
            continue

        priority = (
            _get_decision_change_priority(
                previous_decision,
                current_decision,
            )
        )

        changes.append(
            PortfolioChange(
                category="Investment Decision",
                company=company,
                previous_value=previous_decision,
                current_value=current_decision,
                priority=priority,
                description=(
                    f"Investment decision changed from "
                    f"{previous_decision} to "
                    f"{current_decision}."
                ),
            )
        )

    return changes
def _get_confidence_change_priority(
    previous_confidence: str,
    current_confidence: str,
) -> str:
    """
    Determine the materiality of a confidence change.
    """

    if (
        previous_confidence == "High"
        and current_confidence == "Low"
    ):
        return "HIGH"

    if (
        previous_confidence == "Low"
        and current_confidence == "High"
    ):
        return "HIGH"

    return "MEDIUM"


def _detect_confidence_changes(
    previous: PortfolioSnapshot,
    current: PortfolioSnapshot,
) -> list[PortfolioChange]:
    """
    Detect changes in investment decision confidence.
    """

    changes = []

    previous_decisions = (
        _index_company_decisions(previous)
    )

    current_decisions = (
        _index_company_decisions(current)
    )

    common_companies = (
        previous_decisions.keys()
        & current_decisions.keys()
    )

    for company in sorted(common_companies):

        previous_confidence = (
            previous_decisions[company].get(
                "confidence"
            )
        )

        current_confidence = (
            current_decisions[company].get(
                "confidence"
            )
        )

        # Skip if confidence data is unavailable.
        if (
            previous_confidence is None
            or current_confidence is None
        ):
            continue

        if previous_confidence == current_confidence:
            continue

        priority = (
            _get_confidence_change_priority(
                previous_confidence,
                current_confidence,
            )
        )

        changes.append(
            PortfolioChange(
                category="Confidence",
                company=company,
                previous_value=previous_confidence,
                current_value=current_confidence,
                priority=priority,
                description=(
                    f"Investment confidence changed from "
                    f"{previous_confidence} to "
                    f"{current_confidence}."
                ),
            )
        )

    return changes
def _detect_company_field_changes(
    previous: PortfolioSnapshot,
    current: PortfolioSnapshot,
    field: str,
    category: str,
    priority: str = "MEDIUM",
) -> list[PortfolioChange]:
    """
    Detect changes in a specified company decision field.
    """

    changes = []

    previous_decisions = (
        _index_company_decisions(previous)
    )

    current_decisions = (
        _index_company_decisions(current)
    )

    common_companies = (
        previous_decisions.keys()
        & current_decisions.keys()
    )

    for company in sorted(common_companies):

        previous_value = (
            previous_decisions[company].get(field)
        )

        current_value = (
            current_decisions[company].get(field)
        )

        if (
            previous_value is None
            or current_value is None
        ):
            continue

        if previous_value == current_value:
            continue

        changes.append(
            PortfolioChange(
                category=category,
                company=company,
                previous_value=str(previous_value),
                current_value=str(current_value),
                priority=priority,
                description=(
                    f"{category} changed from "
                    f"{previous_value} to "
                    f"{current_value}."
                ),
            )
        )

    return changes
def _detect_portfolio_weight_changes(
    previous: PortfolioSnapshot,
    current: PortfolioSnapshot,
    threshold: float = 1.0,
) -> list[PortfolioChange]:
    """
    Detect meaningful changes in company portfolio weights.

    Small changes below the configured percentage-point
    threshold are ignored.
    """

    changes = []

    previous_decisions = (
        _index_company_decisions(previous)
    )

    current_decisions = (
        _index_company_decisions(current)
    )

    common_companies = (
        previous_decisions.keys()
        & current_decisions.keys()
    )

    for company in sorted(common_companies):

        previous_weight = (
            previous_decisions[company].get(
                "portfolio_weight"
            )
        )

        current_weight = (
            current_decisions[company].get(
                "portfolio_weight"
            )
        )

        if (
            previous_weight is None
            or current_weight is None
        ):
            continue

        previous_weight = float(
            previous_weight
        )

        current_weight = float(
            current_weight
        )

        change = (
            current_weight - previous_weight
        )

        if abs(change) < threshold:
            continue

        if abs(change) >= 5:
            priority = "HIGH"

        elif abs(change) >= 2:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        direction = (
            "increased"
            if change > 0
            else "decreased"
        )

        changes.append(
            PortfolioChange(
                category="Portfolio Weight",
                company=company,
                previous_value=(
                    f"{previous_weight:.2f}%"
                ),
                current_value=(
                    f"{current_weight:.2f}%"
                ),
                priority=priority,
                description=(
                    f"Portfolio weight {direction} by "
                    f"{abs(change):.2f} percentage points."
                ),
            )
        )

    return changes

def _detect_portfolio_metric_change(
    previous_value,
    current_value,
    category: str,
    priority: str = "MEDIUM",
) -> PortfolioChange | None:
    """
    Detect a change in a portfolio-level metric.
    """

    if (
        previous_value is None
        or current_value is None
    ):
        return None

    if previous_value == current_value:
        return None

    return PortfolioChange(
        category=category,
        company=None,
        previous_value=str(previous_value),
        current_value=str(current_value),
        priority=priority,
        description=(
            f"{category} changed from "
            f"{previous_value} to "
            f"{current_value}."
        ),
    )

def _detect_portfolio_level_changes(
    previous: PortfolioSnapshot,
    current: PortfolioSnapshot,
) -> list[PortfolioChange]:
    """
    Detect meaningful portfolio-level changes.
    """

    changes = []

    # ------------------------------------------------------
    # Portfolio Health
    # ------------------------------------------------------

    previous_health = (
        previous.portfolio_health.get("Total")
    )

    current_health = (
        current.portfolio_health.get("Total")
    )

    health_change = _detect_portfolio_metric_change(
        previous_health,
        current_health,
        category="Portfolio Health",
        priority="MEDIUM",
    )

    if health_change:
        changes.append(health_change)

    # ------------------------------------------------------
    # Largest Holding
    # ------------------------------------------------------

    previous_largest_holding = (
        previous.portfolio_summary.get(
            "Largest Holding"
        )
    )

    current_largest_holding = (
        current.portfolio_summary.get(
            "Largest Holding"
        )
    )

    holding_change = (
        _detect_portfolio_metric_change(
            previous_largest_holding,
            current_largest_holding,
            category="Largest Holding",
            priority="MEDIUM",
        )
    )

    if holding_change:
        changes.append(holding_change)

    # ------------------------------------------------------
    # Largest Holding Weight
    # ------------------------------------------------------

    previous_largest_weight = (
        previous.portfolio_summary.get(
            "Largest Weight"
        )
    )

    current_largest_weight = (
        current.portfolio_summary.get(
            "Largest Weight"
        )
    )

    if (
        previous_largest_weight is not None
        and current_largest_weight is not None
    ):

        weight_difference = abs(
            float(current_largest_weight)
            - float(previous_largest_weight)
        )

        # Ignore insignificant portfolio movement.
        if weight_difference >= 1.0:

            changes.append(
                PortfolioChange(
                    category="Largest Holding Weight",
                    company=None,
                    previous_value=(
                        f"{float(previous_largest_weight):.2f}%"
                    ),
                    current_value=(
                        f"{float(current_largest_weight):.2f}%"
                    ),
                    priority=(
                        "HIGH"
                        if weight_difference >= 5
                        else "MEDIUM"
                    ),
                    description=(
                        "Largest holding weight changed by "
                        f"{weight_difference:.2f} "
                        "percentage points."
                    ),
                )
            )

    # ------------------------------------------------------
    # Top 3 Concentration
    # ------------------------------------------------------

    previous_top3 = (
        previous.portfolio_risk
        .get("details", {})
        .get("Top 3 Concentration")
    )

    current_top3 = (
        current.portfolio_risk
        .get("details", {})
        .get("Top 3 Concentration")
    )

    if previous_top3 and current_top3:

        previous_level = previous_top3[0]
        current_level = current_top3[0]

        if previous_level != current_level:

            changes.append(
                PortfolioChange(
                    category="Top 3 Concentration",
                    company=None,
                    previous_value=previous_level,
                    current_value=current_level,
                    priority="HIGH",
                    description=(
                        "Top-3 portfolio concentration "
                        f"risk changed from "
                        f"{previous_level} to "
                        f"{current_level}."
                    ),
                )
            )

    return changes
def compare_portfolio_snapshots(
    previous: PortfolioSnapshot,
    current: PortfolioSnapshot,
) -> PortfolioChangeResult:
    """
    Compare two portfolio snapshots and identify
    meaningful changes.

    Initial version detects investment decision
    changes only.
    """

    changes = []

    changes.extend(
        _detect_decision_changes(
            previous,
            current,
        )
    )

    changes.extend(
        _detect_confidence_changes(
            previous,
            current,
        )
    )

    changes.extend(
        _detect_company_field_changes(
            previous,
            current,
            field="fundamental_rating",
            category="Fundamental Rating",
        )
    )

    changes.extend(
        _detect_company_field_changes(
            previous,
            current,
            field="valuation_view",
            category="Valuation",
        )
    )

    changes.extend(
        _detect_company_field_changes(
            previous,
            current,
            field="quarterly_assessment",
            category="Quarterly Momentum",
            priority="HIGH",
        )
    )
    changes.extend(
        _detect_portfolio_weight_changes(
            previous,
            current,
        )
    )

    changes.extend(
        _detect_portfolio_level_changes(
            previous,
            current,
        )
    )
    change_count = len(changes)

    if change_count == 0:
        summary = "No meaningful portfolio changes detected."
    elif change_count == 1:
        summary = "1 meaningful portfolio change detected."
    else:
        summary = (
            f"{change_count} meaningful portfolio changes detected."
        )

    return PortfolioChangeResult(
        previous_date=previous.snapshot_date,
        current_date=current.snapshot_date,
        changes=changes,
        summary=summary,
    )
def compare_portfolio_state():
    """
    Compare the latest saved portfolio snapshot
    with the current FreedomIQ portfolio state.
    """

    previous_snapshot = load_latest_snapshot()

    if previous_snapshot is None:
        return None

    current_snapshot = create_portfolio_snapshot()

    return compare_portfolio_snapshots(
        previous_snapshot,
        current_snapshot,
    )