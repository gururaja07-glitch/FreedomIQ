from research.models import FinancialSummary
from research.utils import (
    format_percent,
    format_ratio,
)


def get_financials(info: dict) -> FinancialSummary:
    """
    Extract financial metrics from Yahoo Finance.
    """

    revenue_growth = format_percent(info.get("revenueGrowth"))
    profit_growth = format_percent(info.get("earningsGrowth"))

    roe = format_percent(info.get("returnOnEquity"))
    roce = "N/A"   # Yahoo Finance does not provide ROCE directly

    debt_equity = format_ratio(info.get("debtToEquity"))
    operating_margin = format_percent(info.get("operatingMargins"))

    return FinancialSummary(
        revenue_growth=revenue_growth,
        profit_growth=profit_growth,
        roe=roe,
        roce=roce,
        debt_equity=debt_equity,
        operating_margin=operating_margin,

        free_cash_flow=info.get("freeCashflow"),

        cash=info.get("totalCash"),

        total_debt=info.get("totalDebt"),
    )