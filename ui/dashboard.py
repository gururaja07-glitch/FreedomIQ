import streamlit as st

from tools.formatter import format_money


def show_metrics(summary, health):

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Investment",
            format_money(summary["Investment"])
        )

    with col2:

        st.metric(
            "Current Value",
            format_money(summary["Current Value"])
        )

    with col3:

        st.metric(
            "Return",
            f'{summary["Return %"]:.2f}%'
        )

    col4, col5 = st.columns(2)

    with col4:

        st.metric(
            "Health Score",
            f'{health["Total"]:.2f}/100'
        )

    with col5:

        st.metric(
            "Risk",
            "HIGH"
        )