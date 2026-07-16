import streamlit as st

from tools.portfolio import get_portfolio
from tools.market import update_prices
from ui.health import show_health
from tools.analytics import (
    calculate_metrics,
    calculate_portfolio_summary,
)
from ui.dashboard import show_metrics
from ui.risk import show_risk

st.set_page_config(
    page_title="FreedomIQ",
    page_icon="📈",
    layout="wide",
)

st.title("📈 FreedomIQ")
st.caption("Personal Portfolio Dashboard")

# ----------------------------------
# Load Portfolio
# ----------------------------------

df = get_portfolio()

df = update_prices(df)

df = calculate_metrics(df)

summary = calculate_portfolio_summary(df)

# ----------------------------------
# Summary Cards
# ----------------------------------

health = {"Total": 100}
show_metrics(summary, health, "Low")

st.divider()

# ----------------------------------
# Holdings
# ----------------------------------

st.subheader("Portfolio Holdings")

display_columns = [
    "Stock",
    "Quantity",
    "BuyPrice",
    "CurrentPrice",
    "Investment",
    "Current Value",
    "Profit",
    "Return %",
    "Weight %",
]

st.dataframe(
    df[display_columns],
    use_container_width=True,
    hide_index=True,
)
