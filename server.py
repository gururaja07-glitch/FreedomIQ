from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import calculate_metrics
from tools.report import print_summary
from tools.charts import allocation_chart, top_holdings_chart
from tools.sector_analysis import add_sector, sector_summary
from tools.health import health_score

df = get_portfolio()
df = update_prices(df)
df = calculate_metrics(df)

df = add_sector(df)

print_summary(df)

sector_summary(df)

health_score(df)

allocation_chart(df)

top_holdings_chart(df)