import streamlit as st

from tools.charts import (
    portfolio_pie_chart,
    sector_pie_chart,
    top_holdings_chart,
    asset_allocation_chart,
)
from services.portfolio_service import get_dashboard_data

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



dashboard = get_dashboard_data()

df = dashboard.portfolio
summary = dashboard.summary
allocation = dashboard.allocation
insights = dashboard.insights
top_performers = dashboard.top_performers
top_losers = dashboard.top_losers
health = dashboard.health
risk = dashboard.risk["details"]
overall_risk = dashboard.risk["overall"]

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

show_advisor(dashboard.advisor)
st.divider()

# ----------------------------------
# Portfolio Rebalancing
# ----------------------------------

show_rebalancing(dashboard.rebalancing)

st.divider()