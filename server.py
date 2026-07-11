from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import calculate_metrics
from tools.report import print_summary

# Read portfolio
df = get_portfolio()

# Get today's market prices
df = update_prices(df)

# Calculate metrics
df = calculate_metrics(df)

# Show complete portfolio
print(df)

print()

# Show summary
print_summary(df)
from tools.charts import allocation_chart, top_holdings_chart
print_summary(df)
print(df[["Stock", "Current Value"]])
print("\nChecking Current Value...\n")
allocation_chart(df)
top_holdings_chart(df)