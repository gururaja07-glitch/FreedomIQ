import streamlit as st

from tools.formatter import format_money, format_percentage


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
        format_money(summary["Current Value"]),
        format_percentage(summary["Return %"])
    )

    cols[2].metric(
        "💵 Profit",
        format_money(summary["Profit"])
    )

    cols[3].metric(
        "📊 Return",
        format_percentage(summary["Return %"])
    )

    cols[4].metric(
        "📦 Stocks",
        summary["Number of Stocks"]
    )

    cols[5].metric(
        "🏆 Largest",
        summary["Largest Holding"],
        format_percentage(summary["Largest Weight"])
    )

    cols[6].metric(
        "❤️ Health",
        f'{health["Total"]:.0f}/100'
    )

    cols[7].metric(
        "⚠️ Risk",
        risk_level
    )


def show_portfolio_insights(insights):
    """
    Display portfolio insights.
    """

    st.subheader("📊 Portfolio Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🏆 Best Performer",
            insights["Best Performer"],
            format_percentage(insights["Best Return"])
        )

    with col2:
        st.metric(
            "📉 Worst Performer",
            insights["Worst Performer"],
            format_percentage(insights["Worst Return"])
        )

    with col3:
        st.metric(
            "⚖ Largest Holding",
            insights["Largest Holding"],
            format_percentage(insights["Largest Weight"])
        )


def show_top_performers(top_performers):
    """
    Display top performing stocks.
    """

    st.subheader("🏆 Top Performers")

    for i, row in top_performers.iterrows():
        st.metric(
            f"{i + 1}. {row['Stock']}",
            format_percentage(row["Return %"])
        )


def show_top_losers(top_losers):
    """
    Display worst performing stocks.
    """

    st.subheader("📉 Top Losers")

    for i, row in top_losers.iterrows():
        st.metric(
            f"{i + 1}. {row['Stock']}",
            format_percentage(row["Return %"])
        )