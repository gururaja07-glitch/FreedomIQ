from dataclasses import dataclass

from services.investor_action_brief_service import (
    _build_attention_items,
    _build_summary,
)


@dataclass
class TestContext:
    key_context: list[dict]
    portfolio_status: dict


def test_attention_items_keep_only_critical_and_high():
    context = TestContext(
        key_context=[
            {
                "source": "persistent_action",
                "title": "LT REDUCE",
                "priority": "CRITICAL",
                "description": "Persistent reduction signal.",
            },
            {
                "source": "persistent_opportunity",
                "title": "RELIANCE ADD",
                "priority": "HIGH",
                "description": "Persistent opportunity.",
            },
            {
                "source": "recent_change",
                "title": "ITC valuation",
                "priority": "MEDIUM",
                "description": "Valuation changed.",
            },
        ],
        portfolio_status={},
    )

    items = _build_attention_items(context)

    assert len(items) == 2

    assert items[0]["title"] == "LT REDUCE"
    assert items[0]["priority"] == "CRITICAL"

    assert items[1]["title"] == "RELIANCE ADD"
    assert items[1]["priority"] == "HIGH"


def test_attention_items_empty_when_no_high_priority_context():
    context = TestContext(
        key_context=[
            {
                "source": "recent_change",
                "title": "ITC valuation",
                "priority": "MEDIUM",
                "description": "Valuation changed.",
            },
            {
                "source": "watchpoint",
                "title": "Sector concentration",
                "priority": "LOW",
                "description": "Monitor concentration.",
            },
        ],
        portfolio_status={},
    )

    items = _build_attention_items(context)

    assert items == []


def test_summary_uses_existing_portfolio_status():
    context = TestContext(
        key_context=[],
        portfolio_status={
            "Health Score": 90,
            "Overall Risk": "🟢 Low",
            "Largest Holding": "LTF",
            "Largest Weight": 22.67,
        },
    )

    summary = _build_summary(context, [])

    assert "Portfolio health is 90" in summary
    assert "overall risk 🟢 Low" in summary
    assert "Largest holding is LTF at 22.67%" in summary
    assert "No critical or high-priority items require attention." in summary


def test_summary_reports_attention_count():
    context = TestContext(
        key_context=[],
        portfolio_status={
            "Health Score": 90,
            "Overall Risk": "🟢 Low",
            "Largest Holding": "LTF",
            "Largest Weight": 22.67,
        },
    )

    attention_items = [
        {
            "source": "persistent_action",
            "title": "LT REDUCE",
            "priority": "CRITICAL",
            "description": "",
        },
        {
            "source": "persistent_opportunity",
            "title": "RELIANCE ADD",
            "priority": "HIGH",
            "description": "",
        },
    ]

    summary = _build_summary(context, attention_items)

    assert "2 high-priority item(s) deserve attention." in summary
