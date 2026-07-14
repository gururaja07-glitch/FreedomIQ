import streamlit as st

from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import calculate_metrics
from tools.sector_analysis import add_sector
from tools.summary import calculate_portfolio_summary
from tools.health import calculate_health_score
from tools.rebalance import calculate_rebalancing
from tools.formatter import format_money
from tools.charts import portfolio_pie_chart

# --------------------------------------------------
# Load Portfolio
# --------------------------------------------------

cash = 450000
gold = 650000

df = get_portfolio()
df = update_prices(df)
df = calculate_metrics(df)
df = add_sector(df)

# --------------------------------------------------
# Portfolio Summary
# --------------------------------------------------

summary = calculate_portfolio_summary(df, cash, gold)

# --------------------------------------------------
# Health Score
# --------------------------------------------------

total_portfolio = df["Current Value"].sum() + cash + gold

cash_weight = cash / total_portfolio * 100
gold_weight = gold / total_portfolio * 100

health = calculate_health_score(
    df,
    cash_weight,
    gold_weight
)

# --------------------------------------------------
# Rebalancing Suggestions
# --------------------------------------------------

actions = calculate_rebalancing(df)

# --------------------------------------------------
# Streamlit Page
# --------------------------------------------------

st.set_page_config(
    page_title="FreedomIQ",
    page_icon="📈",
    layout="wide"
)

st.sidebar.title("📈 FreedomIQ")

st.sidebar.markdown("---")

st.sidebar.success("Portfolio Loaded")

st.sidebar.markdown("### Navigation")

st.sidebar.write("🏠 Dashboard")

st.sidebar.write("📊 Portfolio")

st.sidebar.write("❤️ Health")

st.sidebar.write("⚠️ Risk")

st.sidebar.write("♻️ Rebalancing")

st.title("📈 FreedomIQ")

st.caption("AI Powered Portfolio Analytics")

# --------------------------------------------------
# Top Metrics
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Investment",
        format_money(summary["Investment"])
    )

with col2:
    st.metric(
        "Current Value",
       format_money(summary["Current Value"])
    )

with col3:
    st.metric(
        "Return",
        f'{summary["Return %"]:.2f}%'
    )

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Health Score",
        f'{health["Total"]:.2f}'
    )

with col5:
    st.metric(
        "Risk",
        "HIGH"
    )

# --------------------------------------------------
# Portfolio Summary
# --------------------------------------------------

st.divider()

st.subheader("📊 Portfolio Summary")

col1, col2 = st.columns(2)

with col1:

    st.write(f'**Number of Stocks:** {summary["Number of Stocks"]}')
    st.write(f'**Number of Sectors:** {summary["Number of Sectors"]}')
    st.write(f'**Largest Holding:** {summary["Largest Holding"]}')

with col2:

    st.write(f'**Largest Weight:** {summary["Largest Weight"]:.2f}%')
    st.write(f'**Cash Weight:** {summary["Cash Weight"]:.2f}%')
    st.write(f'**Gold Weight:** {summary["Gold Weight"]:.2f}%')

# --------------------------------------------------
# Recommendations
# --------------------------------------------------

st.divider()

st.subheader("📌 Today's Recommendations")

st.divider()

st.subheader("🥧 Portfolio Allocation")

chart = df.set_index("Stock")["Current Value"]


if not actions:

    st.success("✅ Your portfolio is well balanced.")

else:

    for action in actions:

        st.warning(
            f"""
**{action["Type"]} : {action["Name"]}**

Current Weight : **{action["Current Weight"]:.2f}%**

Target Weight : **{action["Target Weight"]:.2f}%**

Excess : **{action["Excess"]:.2f}%**
"""
        )

st.divider()

st.subheader("🥧 Portfolio Allocation")

fig = portfolio_pie_chart(df)

st.pyplot(fig)