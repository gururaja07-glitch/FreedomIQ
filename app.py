import streamlit as st

st.set_page_config(
    page_title="FreedomIQ",
    page_icon="📈",
    layout="wide"
)

st.title("📈 FreedomIQ")

st.write("Welcome to FreedomIQ")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Investment", "₹31.59 L")

with col2:
    st.metric("Current Value", "₹48.76 L")

with col3:
    st.metric("Return", "54.34%")

col4, col5 = st.columns(2)

with col4:
    st.metric("Health Score", "98.36")

with col5:
    st.metric("Risk", "HIGH")