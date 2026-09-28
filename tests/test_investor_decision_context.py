from dataclasses import dataclass

from services.investor_decision_context_service import (
    _build_key_context,
)


@dataclass
class TestItem:
    title: str
    priority: str
    description: str = ""


def test_key_context_prioritizes_existing_intelligence():
    recent_changes = [
        TestItem(
            title="LT valuation changed",
            priority="HIGH",
            description="Valuation moved from Fairly Valued to Expensive.",
        )
    ]

    persistent_actions = [
        TestItem(
            title="LT REDUCE",
            priority="CRITICAL",
        )
    ]

    persistent_opportunities = [
        TestItem(
            title="RELIANCE ADD",
            priority="HIGH",
        )
    ]

    persistent_watchpoints = [
        TestItem(
            title="Top-3 concentration",
            priority="HIGH",
        )
    ]

    context = _build_key_context(
        recent_changes,
        persistent_actions,
        persistent_opportunities,
        persistent_watchpoints,
        None,
    )

    assert len(context) == 4

    assert context[0]["priority"] == "CRITICAL"
    assert context[0]["title"] == "LT REDUCE"

    titles = [item["title"] for item in context]

    assert "LT valuation changed" in titles
    assert "RELIANCE ADD" in titles
    assert "Top-3 concentration" in titles


def test_medium_and_low_priority_items_are_not_key_context():
    recent_changes = [
        TestItem(title="Medium change", priority="MEDIUM"),
        TestItem(title="Low change", priority="LOW"),
    ]

    context = _build_key_context(
        recent_changes,
        [],
        [],
        [],
        None,
    )

    assert context == []


def test_trend_changes_are_added_to_key_context():
    @dataclass
    class TestTrend:
        health_trend: str = "Declining"
        risk_trend: str = "Stable"
        largest_holding_weight_trend: str = "Improving"

    context = _build_key_context(
        [],
        [],
        [],
        [],
        TestTrend(),
    )

    titles = [item["title"] for item in context]

    assert "health_trend" in titles
    assert "largest_holding_weight_trend" in titles
    assert "risk_trend" not in titles

    for item in context:
        assert item["priority"] == "HIGH"
