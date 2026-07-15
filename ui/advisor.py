import streamlit as st

def show_advisor(advisor):

    st.divider()

    st.subheader("🤖 FreedomIQ Advisor")

    st.success(
        f'Portfolio Health : {advisor["Health"]}'
    )

    st.markdown("### ✅ Strengths")

    for item in advisor["Strengths"]:
        st.write(item)

    st.markdown("### ⚠️ Watchlist")

    for item in advisor["Warnings"]:
        st.write(item)

    st.markdown("### 📌 Recommended Actions")

    for item in advisor["Actions"]:
        st.write(item)