from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import calculate_metrics
from tools.report import print_summary
from tools.charts import allocation_chart, top_holdings_chart
from tools.risk import (
    calculate_risk,
    print_risk
)
from tools.rebalance import (
    calculate_rebalancing,
    print_rebalancing
)
from tools.sector_analysis import (
    add_sector,
    calculate_sector_summary,
    print_sector_summary
)

from tools.summary import (
    calculate_portfolio_summary,
    print_portfolio_summary
)

from tools.health import (
    calculate_health_score,
    print_health_score
)

# Cash & Gold
cash = 450000
gold = 650000

# 1. Read portfolio
df = get_portfolio()

# 2. Update market prices
df = update_prices(df)

# 3. Calculate metrics
df = calculate_metrics(df)

# 4. Add sectors
df = add_sector(df)

total_portfolio = (
    df["Current Value"].sum()
    + cash
    + gold
)

cash_weight = cash / total_portfolio * 100

gold_weight = gold / total_portfolio * 100

df = get_portfolio()

df = update_prices(df)

df = calculate_metrics(df)

df = add_sector(df)

sector_summary = calculate_sector_summary(df)

print_sector_summary(sector_summary)

portfolio_summary = calculate_portfolio_summary(df, cash, gold)

print_portfolio_summary(portfolio_summary)


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


print_health_score(health)

risk = calculate_risk(
    df,
    cash_weight,
    gold_weight
)

print_risk(risk)

actions = calculate_rebalancing(df)

print_rebalancing(actions)

