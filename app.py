import streamlit as st

# ==========================================
# Backend
# ==========================================

from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import calculate_metrics
from tools.sector_analysis import add_sector
from tools.summary import calculate_portfolio_summary
from tools.health import calculate_health_score
from tools.rebalance import calculate_rebalancing
from tools.performance import (
    calculate_top_performers,
    calculate_top_losers
)

# ==========================================
# Utilities
# ==========================================

from tools.charts import (
    portfolio_pie_chart,
    top_holdings_chart
)

# ==========================================
# UI
# ==========================================

from ui.dashboard import show_metrics
from ui.summary import show_summary
from ui.recommendations import show_recommendations

# ==========================================
# Page Config
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
# Portfolio Loader
# ==========================================

@st.cache_data(ttl=300)
def load_portfolio():

    df = get_portfolio()

    df = update_prices(df)

    df = calculate_metrics(df)

    df = add_sector(df)

    return df


cash = 450000
gold = 650000

df = load_portfolio()

# ==========================================
# Summary
# ==========================================

summary = calculate_portfolio_summary(
    df,
    cash,
    gold
)

# ==========================================
# Health
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
# Rebalancing
# ==========================================

actions = calculate_rebalancing(df)

# ==========================================
# Performance
# ==========================================

top_winners = calculate_top_performers(df)

top_losers = calculate_top_losers(df)

# ==========================================
# Dashboard
# ==========================================

st.title("📈 FreedomIQ")

st.caption("AI Powered Portfolio Analytics")

show_metrics(
    summary,
    health
)

show_summary(summary)

show_recommendations(actions)

# ==========================================
# Portfolio Allocation
# ==========================================

st.divider()

st.subheader("🥧 Portfolio Allocation")

fig = portfolio_pie_chart(df)

st.pyplot(fig)

# ==========================================
# Top Holdings
# ==========================================

st.divider()

st.subheader("📊 Top 10 Holdings")

fig = top_holdings_chart(df)

st.pyplot(fig)

# ==========================================
# Portfolio Holdings
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

# ==========================================
# Performance
# ==========================================

st.divider()

st.subheader("🏆 Performance")

left, right = st.columns(2)

with left:

    st.success("🏆 Top Winners")

    for _, row in top_winners.iterrows():

        st.write(
            f"**{row['Stock']}**  "
            f"₹{row['Profit']:,.0f}  "
            f"({row['Return %']:.2f}%)"
        )

with right:

    st.error("📉 Top Losers")

    for _, row in top_losers.iterrows():

        st.write(
            f"**{row['Stock']}**  "
            f"₹{row['Profit']:,.0f}  "
            f"({row['Return %']:.2f}%)"
        )