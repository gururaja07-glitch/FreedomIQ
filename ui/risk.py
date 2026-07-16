"""
FreedomIQ

Module : Risk UI

Purpose :
Displays Portfolio Risk in Streamlit.

Author : Gururaj N K
Version : 0.1
"""

import streamlit as st


def show_risk(risk):
    """
    Display portfolio risk.
    """

    st.subheader("⚠️ Portfolio Risk")

    risk_data = []

    for category, (level, message) in risk.items():

        if level.lower() == "low":
            icon = "🟢"

        elif level.lower() == "medium":
            icon = "🟡"

        else:
            icon = "🔴"

        risk_data.append({
            "Category": category,
            "Risk": f"{icon} {level}",
            "Description": message
        })

    st.dataframe(
        risk_data,
        hide_index=True,
        use_container_width=True
    )