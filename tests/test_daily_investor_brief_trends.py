from models.daily_investor_brief_snapshot import (
    DailyInvestorBriefSnapshot,
)
from services.daily_investor_brief_trend_service import (
    analyze_daily_investor_brief_trends,
)


def make_snapshot(
    date,
    health,
    risk,
    weight,
    actions,
    opportunities,
    watchpoints,
):
    return DailyInvestorBriefSnapshot(
        brief_date=date,
        portfolio_snapshot={
            "Health Score": health,
            "Overall Risk": risk,
            "Largest Weight": weight,
        },
        changes=[],
        persistent_actions=actions,
        persistent_opportunities=opportunities,
        watchpoints=watchpoints,
        trends={
            "health": "Stable",
            "risk": "Stable",
            "largest_holding_weight": "Stable",
            "review_count": 1,
            "start_date": date,
            "end_date": date,
        },
        conclusion="Test snapshot.",
    )


snapshots = [
    make_snapshot(
        "2026-09-21",
        82,
        "🟢 Low",
        20,
        [
            {
                "title": "LT REDUCE",
                "priority": "HIGH",
            }
        ],
        [],
        [
            {
                "title": "Top-3 concentration",
                "priority": "MEDIUM",
            }
        ],
    ),
    make_snapshot(
        "2026-09-22",
        85,
        "🟡 Medium",
        21,
        [
            {
                "title": "LT REDUCE",
                "priority": "HIGH",
            }
        ],
        [
            {
                "title": "RELIANCE ADD",
                "priority": "MEDIUM",
            }
        ],
        [
            {
                "title": "Top-3 concentration",
                "priority": "MEDIUM",
            }
        ],
    ),
    make_snapshot(
        "2026-09-23",
        87,
        "🟡 Medium",
        23,
        [
            {
                "title": "LT REDUCE",
                "priority": "CRITICAL",
            }
        ],
        [
            {
                "title": "RELIANCE ADD",
                "priority": "MEDIUM",
            }
        ],
        [
            {
                "title": "Top-3 concentration",
                "priority": "HIGH",
            }
        ],
    ),
    make_snapshot(
        "2026-09-24",
        90,
        "🔴 High",
        24,
        [
            {
                "title": "LT REDUCE",
                "priority": "CRITICAL",
            }
        ],
        [
            {
                "title": "RELIANCE ADD",
                "priority": "HIGH",
            }
        ],
        [
            {
                "title": "Top-3 concentration",
                "priority": "HIGH",
            }
        ],
    ),
]


result = analyze_daily_investor_brief_trends(
    snapshots
)

print("Reviews:", result.review_count)
print("Period:", result.start_date, "to", result.end_date)
print("Health trend:", result.health_trend)
print("Risk trend:", result.risk_trend)
print(
    "Largest weight trend:",
    result.largest_holding_weight_trend,
)

print("\nPersistent Actions:")
for item in result.persistent_actions:
    print(
        item.title,
        "| reviews:",
        item.review_count,
        "| consecutive:",
        item.consecutive_count,
        "| priority:",
        item.priority,
    )

print("\nPersistent Opportunities:")
for item in result.persistent_opportunities:
    print(
        item.title,
        "| reviews:",
        item.review_count,
        "| consecutive:",
        item.consecutive_count,
        "| priority:",
        item.priority,
    )

print("\nPersistent Watchpoints:")
for item in result.persistent_watchpoints:
    print(
        item.title,
        "| reviews:",
        item.review_count,
        "| consecutive:",
        item.consecutive_count,
        "| priority:",
        item.priority,
    )

print("\nSummary:")
print(result.summary)