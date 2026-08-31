
from tools.portfolio import get_portfolio
from tools.market import update_prices
from tools.analytics import calculate_metrics

def prepare_portfolio_data():
    df = get_portfolio()
    df = update_prices(df)
    df = calculate_metrics(df)
    return df