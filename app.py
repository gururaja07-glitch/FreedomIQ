import streamlit as st

from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import (
    calculate_metrics,
    calculate_portfolio_summary,
    calculate_asset_allocation,
    calculate_portfolio_insights,
    get_top_performers,
    get_top_losers,
)
from tools.health import calculate_portfolio_health
from tools.charts import (
    portfolio_pie_chart,
    sector_pie_chart,
    top_holdings_chart,
    asset_allocation_chart,
)
from tools.risk import calculate_portfolio_risk
from tools.advisor import generate_portfolio_advice
from tools.rebalance import calculate_rebalancing

from ui.dashboard import (
    show_metrics,
    show_portfolio_insights,
    show_top_performers,
    show_top_losers,
)
from ui.health import show_health
from ui.risk import show_risk
from ui.advisor import show_advisor
from ui.rebalance import show_rebalancing
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
allocation = calculate_asset_allocation(df)
insights = calculate_portfolio_insights(df)

# New Analytics
top_performers = get_top_performers(df)
top_losers = get_top_losers(df)

# ----------------------------------
# Portfolio Health & Risk
# ----------------------------------

health = calculate_portfolio_health(df, allocation)
risk, overall_risk = calculate_portfolio_risk(df, allocation)

# ----------------------------------
# Summary Cards
# ----------------------------------

show_metrics(summary, health, overall_risk)
# ----------------------------------
# Portfolio Insights
# ----------------------------------

show_portfolio_insights(insights)

st.divider()

# ----------------------------------
# Top Performers & Top Losers
# ----------------------------------

col1, col2 = st.columns(2)

with col1:
    show_top_performers(top_performers)

with col2:
    show_top_losers(top_losers)

st.divider()

# ----------------------------------
# Charts
# ----------------------------------

st.subheader("Portfolio Overview")

col1, col2 = st.columns(2)

with col1:
    st.pyplot(portfolio_pie_chart(df))

with col2:
    st.pyplot(sector_pie_chart(df))

st.pyplot(top_holdings_chart(df))

st.divider()

# ----------------------------------
# Asset Allocation
# ----------------------------------

st.subheader("Asset Allocation")

st.pyplot(
    asset_allocation_chart(
        allocation["Equity"],
        allocation["Gold"],
        allocation["Silver"],
        allocation["Cash"],
    )
)

st.divider()

# ----------------------------------
# Portfolio Health
# ----------------------------------

show_health(health)

st.divider()

# ----------------------------------
# Portfolio Risk
# ----------------------------------

show_risk(risk)

st.divider()
# ----------------------------------
# Portfolio Advisor
# ----------------------------------

advisor_recommendations = generate_portfolio_advice(
    df,
    allocation
)

show_advisor(advisor_recommendations)

st.divider()

# ----------------------------------
# Portfolio Rebalancing
# ----------------------------------

rebalancing = calculate_rebalancing(df)

show_rebalancing(rebalancing)

st.divider()