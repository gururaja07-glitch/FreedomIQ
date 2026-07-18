"""
FreedomIQ

Module : Rebalancing UI

Purpose :
Displays portfolio rebalancing suggestions.

Author : Gururaj N K
Version : 0.1
"""

import streamlit as st


def show_rebalancing(recommendations):
    """
    Display portfolio rebalancing suggestions.
    """

    st.subheader("⚖️ Portfolio Rebalancing")

    if not recommendations:

        st.success(
            "✅ No rebalancing required."
        )
        return

    st.dataframe(
        recommendations,
        hide_index=True,
        use_container_width=True,
    )