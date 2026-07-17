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

from tools.charts import (
    portfolio_pie_chart,
    sector_pie_chart,
    top_holdings_chart,
    asset_allocation_chart,
)

from ui.dashboard import show_metrics
from ui.health import show_health
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
allocation = calculate_asset_allocation(df)
insights = calculate_portfolio_insights(df)

# New Analytics
top_performers = get_top_performers(df)
top_losers = get_top_losers(df)

# ----------------------------------
# Summary Cards
# ----------------------------------

health = {"Total": 100}

show_metrics(summary, health, "Low")

st.divider()

# ----------------------------------
# Portfolio Insights
# ----------------------------------

st.subheader("📊 Portfolio Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🏆 Best Performer",
        insights["Best Performer"],
        f'{insights["Best Return"]:.2f}%'
    )

with col2:
    st.metric(
        "📉 Worst Performer",
        insights["Worst Performer"],
        f'{insights["Worst Return"]:.2f}%'
    )

with col3:
    st.metric(
        "⚖ Largest Holding",
        insights["Largest Holding"],
        f'{insights["Largest Weight"]:.2f}%'
    )

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