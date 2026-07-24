from research.models import FinancialSummary
from research.utils import format_percent, format_ratio


def get_financials(info: dict) -> FinancialSummary:
    """
    Extract financial metrics from Yahoo Finance.
    """

    return FinancialSummary(
        revenue_growth=format_percent(info.get("revenueGrowth")),
        profit_growth=format_percent(info.get("earningsGrowth")),
        roe=format_percent(info.get("returnOnEquity")),
        roce="N/A",  # Yahoo does not provide this reliably
        debt_equity=format_ratio(info.get("debtToEquity")),
        operating_margin=format_percent(info.get("operatingMargins")),
    )