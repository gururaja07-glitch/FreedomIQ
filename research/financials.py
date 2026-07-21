from research.models import FinancialSummary


def get_financials(info: dict) -> FinancialSummary:
    """
    Extract financial metrics from Yahoo Finance.
    """

    revenue_growth = info.get("revenueGrowth")
    earnings_growth = info.get("earningsGrowth")
    roe = info.get("returnOnEquity")
    operating_margin = info.get("operatingMargins")
    debt_equity = info.get("debtToEquity")

    return FinancialSummary(
        revenue_growth=(
            f"{revenue_growth * 100:.2f}%"
            if revenue_growth is not None
            else "N/A"
        ),
        profit_growth=(
            f"{earnings_growth * 100:.2f}%"
            if earnings_growth is not None
            else "N/A"
        ),
        roe=(
            f"{roe * 100:.2f}%"
            if roe is not None
            else "N/A"
        ),
        roce="N/A",   # Yahoo does not provide this reliably
        debt_equity=str(debt_equity) if debt_equity is not None else "N/A",
        operating_margin=(
            f"{operating_margin * 100:.2f}%"
            if operating_margin is not None
            else "N/A"
        ),
    )