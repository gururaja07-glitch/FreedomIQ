"""
FreedomIQ

Module : Advisor UI

Purpose :
Displays Portfolio Advisor recommendations.

Author : Gururaj N K
Version : 0.1
"""

import streamlit as st


def show_advisor(recommendations):
    """
    Display portfolio recommendations.
    """

    st.subheader("📋 Portfolio Advisor")

    if not recommendations:

        st.success(
            "✅ Portfolio is well balanced. No action required."
        )
        return

    for item in recommendations:

        priority = item["Priority"]

        if priority == "High":
            icon = "🔴"

        elif priority == "Medium":
            icon = "🟡"

        else:
            icon = "🟢"

        st.info(
            f"{icon} **{item['Category']}** : "
            f"{item['Recommendation']}"
        )