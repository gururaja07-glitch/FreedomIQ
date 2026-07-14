import streamlit as st

# ==========================================
# Backend Imports
# ==========================================

from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import calculate_metrics
from tools.sector_analysis import add_sector
from tools.summary import calculate_portfolio_summary
from tools.health import calculate_health_score
from tools.rebalance import calculate_rebalancing

# ==========================================
# Utility Imports
# ==========================================

from tools.charts import (
    portfolio_pie_chart,
    top_holdings_chart
)

# ==========================================
# UI Imports
# ==========================================

from ui.dashboard import show_metrics
from ui.summary import show_summary
from ui.recommendations import show_recommendations

# ==========================================
# Streamlit Page Configuration
# ==========================================

st.set_page_config(
    page_title="FreedomIQ",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.title("📈 FreedomIQ")

    st.caption("AI Powered Portfolio Analytics")

    st.divider()

    st.success("Portfolio Loaded")

    st.divider()

    st.subheader("Navigation")

    st.write("🏠 Dashboard")
    st.write("📊 Portfolio")
    st.write("❤️ Health")
    st.write("⚠️ Risk")
    st.write("♻️ Rebalancing")

# ==========================================
# Load Portfolio
# ==========================================

cash = 450000
gold = 650000

df = get_portfolio()

df = update_prices(df)

df = calculate_metrics(df)

df = add_sector(df)

# ==========================================
# Portfolio Summary
# ==========================================

summary = calculate_portfolio_summary(
    df,
    cash,
    gold
)

# ==========================================
# Health Score
# ==========================================

total_portfolio = (
    df["Current Value"].sum()
    + cash
    + gold
)

cash_weight = cash / total_portfolio * 100

gold_weight = gold / total_portfolio * 100

health = calculate_health_score(
    df,
    cash_weight,
    gold_weight
)

# ==========================================
# Rebalancing Suggestions
# ==========================================

actions = calculate_rebalancing(df)

# ==========================================
# Dashboard Title
# ==========================================

st.title("📈 FreedomIQ")

st.caption("AI Powered Portfolio Analytics")

# ==========================================
# KPI Cards
# ==========================================

show_metrics(
    summary,
    health
)

# ==========================================
# Portfolio Summary
# ==========================================

show_summary(summary)

# ==========================================
# Recommendations
# ==========================================

show_recommendations(actions)

# ==========================================
# Portfolio Allocation Chart
# ==========================================

st.divider()

st.subheader("🥧 Portfolio Allocation")

fig = portfolio_pie_chart(df)

st.pyplot(fig)

# ==========================================
# Top Holdings Chart
# ==========================================

st.divider()

st.subheader("📊 Top 10 Holdings")

fig = top_holdings_chart(df)

st.pyplot(fig)

# ==========================================
# Portfolio Table
# ==========================================

st.divider()

st.subheader("📋 Portfolio Holdings")

portfolio = df.copy()

portfolio = portfolio[
    [
        "Stock",
        "Quantity",
        "BuyPrice",
        "CurrentPrice",
        "Investment",
        "Current Value",
        "Profit",
        "Return %",
        "Weight %"
    ]
]

portfolio = portfolio.sort_values(
    "Current Value",
    ascending=False
)

portfolio["BuyPrice"] = portfolio["BuyPrice"].round(2)
portfolio["CurrentPrice"] = portfolio["CurrentPrice"].round(2)
portfolio["Investment"] = portfolio["Investment"].round(2)
portfolio["Current Value"] = portfolio["Current Value"].round(2)
portfolio["Profit"] = portfolio["Profit"].round(2)
portfolio["Return %"] = portfolio["Return %"].round(2)
portfolio["Weight %"] = portfolio["Weight %"].round(2)

st.dataframe(
    portfolio,
    use_container_width=True
)