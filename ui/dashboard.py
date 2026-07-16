import streamlit as st

from tools.formatter import format_money


def show_metrics(summary, health, risk_level):
    """
    Display top dashboard metrics.
    """

    cols = st.columns(8)

    cols[0].metric(
        "💰 Investment",
        format_money(summary["Investment"])
    )

    cols[1].metric(
        "📈 Portfolio",
        format_money(summary["Current Value"])
    )

    cols[2].metric(
        "💵 Profit",
        format_money(summary["Profit"])
    )

    cols[3].metric(
        "📊 Return",
        f'{summary["Return %"]:.2f}%'
    )

    cols[4].metric(
        "📦 Stocks",
        summary["Number of Stocks"]
    )

    cols[5].metric(
        "🏆 Largest",
        summary["Largest Holding"]
    )

    cols[6].metric(
        "❤️ Health",
        f'{health["Total"]:.0f}/100'
    )

    cols[7].metric(
        "⚠️ Risk",
        risk_level
    )