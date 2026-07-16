"""
FreedomIQ

Module : Health UI

Purpose :
Displays Portfolio Health in Streamlit.

Author : Gururaj N K
Version : 0.1
"""

import streamlit as st


def show_health(health):

    st.subheader("❤️ Portfolio Health")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.metric(
            "Overall Health",
            f'{health["Total"]:.0f}/100'
        )

    with col2:

        if health["Total"] >= 90:
            rating = "🟢 Excellent"
        elif health["Total"] >= 75:
            rating = "🟡 Good"
        elif health["Total"] >= 60:
            rating = "🟠 Average"
        else:
            rating = "🔴 Poor"

        st.metric(
            "Rating",
            rating
        )

    health_data = {
        "Category": [
            "Diversification",
            "Concentration",
            "Sector",
            "Cash",
            "Gold"
        ],
        "Score": [
            health["Diversification"],
            health["Concentration"],
            health["Sector"],
            health["Cash"],
            health["Gold"]
        ]
    }

    st.dataframe(
        health_data,
        hide_index=True,
        use_container_width=True
    )