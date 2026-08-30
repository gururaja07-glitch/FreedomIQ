from dataclasses import dataclass


@dataclass
class QuarterlyResult:
    """Structured quarterly financial result."""

    company: str
    ticker: str

    latest_period: str
    previous_period: str
    year_ago_period: str

    revenue: float | None = None
    previous_revenue: float | None = None
    year_ago_revenue: float | None = None

    revenue_qoq: float | None = None
    revenue_yoy: float | None = None

    profit: float | None = None
    previous_profit: float | None = None
    year_ago_profit: float | None = None

    profit_qoq: float | None = None
    profit_yoy: float | None = None

    operating_income: float | None = None
    previous_operating_income: float | None = None

    operating_margin: float | None = None
    previous_operating_margin: float | None = None
    margin_change: float | None = None

    cash: float | None = None
    previous_cash: float | None = None

    total_debt: float | None = None
    previous_total_debt: float | None = None

    net_debt: float | None = None
    previous_net_debt: float | None = None

    working_capital: float | None = None
    previous_working_capital: float | None = None

    positive_changes: list[str] | None = None
    negative_changes: list[str] | None = None

    assessment: str = "N/A"

    data_quality: str = "Unknown"