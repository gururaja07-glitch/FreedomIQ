import pandas as pd
import yfinance as yf

from models.quarterly_result import QuarterlyResult
from research.ticker_lookup import get_ticker


def _safe_float(value):
    try:
        if pd.isna(value):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _growth(current, previous):
    if current is None or previous in (None, 0):
        return None

    return ((current - previous) / abs(previous)) * 100


def _get_value(statement, fields, period):
    if statement is None or statement.empty:
        return None

    if period is None or period not in statement.columns:
        return None

    for field in fields:
        if field not in statement.index:
            continue

        value = _safe_float(
            statement.loc[field, period]
        )

        if value is not None:
            return value

    return None


def _get_periods(statement):
    if statement is None or statement.empty:
        return []

    return list(statement.columns)


def _find_balance_period(balance_periods, target_period):
    if target_period is None or not balance_periods:
        return None

    target = pd.Timestamp(target_period)

    valid_periods = [
        period
        for period in balance_periods
        if pd.Timestamp(period) <= target
    ]

    if not valid_periods:
        return None

    return max(
        valid_periods,
        key=lambda period: pd.Timestamp(period),
    )


def _calculate_assessment(
    revenue_yoy,
    profit_yoy,
    margin_change,
):
    positive = 0
    negative = 0

    for value in (
        revenue_yoy,
        profit_yoy,
    ):
        if value is None:
            continue

        if value > 5:
            positive += 1

        elif value < -5:
            negative += 1

    if margin_change is not None:

        if margin_change > 1:
            positive += 1

        elif margin_change < -1:
            negative += 1

    if positive > negative:
        return "Positive"

    if negative > positive:
        return "Negative"

    return "Neutral"


def analyze_quarterly_result(
    company_name: str,
) -> QuarterlyResult:
    """
    Analyze the latest available quarterly financial result.

    Uses Yahoo Finance quarterly income statement and
    quarterly balance sheet data.

    Balance-sheet values are matched using actual
    reporting dates rather than column position.
    """

    ticker_symbol = get_ticker(
        company_name
    )

    if ticker_symbol is None:
        raise ValueError(
            f"No market ticker available for "
            f"{company_name}."
        )

    ticker = yf.Ticker(
        ticker_symbol
    )

    income = ticker.quarterly_income_stmt
    balance = ticker.quarterly_balance_sheet

    income_periods = _get_periods(
        income
    )

    balance_periods = _get_periods(
        balance
    )

    if not income_periods:
        raise ValueError(
            f"No quarterly income statement "
            f"available for {company_name}."
        )

    latest = income_periods[0]

    previous = (
        income_periods[1]
        if len(income_periods) > 1
        else None
    )

    year_ago = None

    if len(income_periods) > 4:
        year_ago = income_periods[4]

    # -------------------------------------------------
    # Revenue
    # -------------------------------------------------

    revenue_fields = (
        "Total Revenue",
        "Operating Revenue",
    )

    revenue = _get_value(
        income,
        revenue_fields,
        latest,
    )

    previous_revenue = _get_value(
        income,
        revenue_fields,
        previous,
    )

    year_ago_revenue = _get_value(
        income,
        revenue_fields,
        year_ago,
    )

    revenue_qoq = _growth(
        revenue,
        previous_revenue,
    )

    revenue_yoy = _growth(
        revenue,
        year_ago_revenue,
    )

    # -------------------------------------------------
    # Profit
    # -------------------------------------------------

    profit_fields = (
        "Net Income",
        "Net Income Common Stockholders",
        "Net Income From Continuing Operation "
        "Net Minority Interest",
    )

    profit = _get_value(
        income,
        profit_fields,
        latest,
    )

    previous_profit = _get_value(
        income,
        profit_fields,
        previous,
    )

    year_ago_profit = _get_value(
        income,
        profit_fields,
        year_ago,
    )

    profit_qoq = _growth(
        profit,
        previous_profit,
    )

    profit_yoy = _growth(
        profit,
        year_ago_profit,
    )

    # -------------------------------------------------
    # Operating income
    # -------------------------------------------------

    operating_income_fields = (
        "OperatingIncome",
        "Operating Income",
        "EBIT",
    )

    operating_income = _get_value(
        income,
        operating_income_fields,
        latest,
    )

    previous_operating_income = _get_value(
        income,
        operating_income_fields,
        previous,
    )

    operating_margin = None

    if (
        revenue not in (None, 0)
        and operating_income is not None
    ):
        operating_margin = (
            operating_income / revenue
        ) * 100

    previous_operating_margin = None

    if (
        previous_revenue not in (None, 0)
        and previous_operating_income is not None
    ):
        previous_operating_margin = (
            previous_operating_income
            / previous_revenue
        ) * 100

    margin_change = None

    if (
        operating_margin is not None
        and previous_operating_margin is not None
    ):
        margin_change = (
            operating_margin
            - previous_operating_margin
        )

    # -------------------------------------------------
    # Balance sheet
    # -------------------------------------------------

    latest_balance_period = (
        _find_balance_period(
            balance_periods,
            latest,
        )
    )

    previous_balance_period = (
        _find_balance_period(
            balance_periods,
            previous,
        )
    )

    cash = _get_value(
        balance,
        (
            "Cash And Cash Equivalents",
            "Cash Financial",
        ),
        latest_balance_period,
    )

    previous_cash = _get_value(
        balance,
        (
            "Cash And Cash Equivalents",
            "Cash Financial",
        ),
        previous_balance_period,
    )

    total_debt = _get_value(
        balance,
        (
            "Total Debt",
        ),
        latest_balance_period,
    )

    previous_total_debt = _get_value(
        balance,
        (
            "Total Debt",
        ),
        previous_balance_period,
    )

    net_debt = _get_value(
        balance,
        (
            "Net Debt",
        ),
        latest_balance_period,
    )

    previous_net_debt = _get_value(
        balance,
        (
            "Net Debt",
        ),
        previous_balance_period,
    )

    # Yahoo may return Net Debt as NaN.
    if net_debt is None and (
        total_debt is not None
        and cash is not None
    ):
        net_debt = total_debt - cash

    if previous_net_debt is None and (
        previous_total_debt is not None
        and previous_cash is not None
    ):
        previous_net_debt = (
            previous_total_debt
            - previous_cash
        )

    working_capital = _get_value(
        balance,
        (
            "Working Capital",
        ),
        latest_balance_period,
    )

    previous_working_capital = _get_value(
        balance,
        (
            "Working Capital",
        ),
        previous_balance_period,
    )

    # -------------------------------------------------
    # Positive / negative developments
    # -------------------------------------------------

    positive_changes = []
    negative_changes = []

    if revenue_yoy is not None:

        if revenue_yoy > 5:
            positive_changes.append(
                f"Revenue increased "
                f"{revenue_yoy:.1f}% YoY."
            )

        elif revenue_yoy < -5:
            negative_changes.append(
                f"Revenue declined "
                f"{abs(revenue_yoy):.1f}% YoY."
            )

    if profit_yoy is not None:

        if profit_yoy > 5:
            positive_changes.append(
                f"Profit increased "
                f"{profit_yoy:.1f}% YoY."
            )

        elif profit_yoy < -5:
            negative_changes.append(
                f"Profit declined "
                f"{abs(profit_yoy):.1f}% YoY."
            )

    if margin_change is not None:

        if margin_change > 1:
            positive_changes.append(
                f"Operating margin improved "
                f"{margin_change:.1f} percentage points."
            )

        elif margin_change < -1:
            negative_changes.append(
                f"Operating margin declined "
                f"{abs(margin_change):.1f} percentage points."
            )

    if (
        total_debt is not None
        and previous_total_debt is not None
    ):

        if total_debt < previous_total_debt:
            positive_changes.append(
                "Total debt decreased QoQ."
            )

        elif total_debt > previous_total_debt:
            negative_changes.append(
                "Total debt increased QoQ."
            )

    # -------------------------------------------------
    # Overall assessment
    # -------------------------------------------------

    assessment = _calculate_assessment(
        revenue_yoy,
        profit_yoy,
        margin_change,
    )

    # -------------------------------------------------
    # Data quality
    # -------------------------------------------------

    available = sum(
        value is not None
        for value in (
            revenue,
            profit,
            operating_margin,
            cash,
            total_debt,
            working_capital,
        )
    )

    if available >= 5:
        data_quality = "Good"

    elif available >= 3:
        data_quality = "Partial"

    else:
        data_quality = "Limited"

    return QuarterlyResult(
        company=company_name,
        ticker=ticker_symbol,

        latest_period=str(latest),

        previous_period=(
            str(previous)
            if previous is not None
            else "N/A"
        ),

        year_ago_period=(
            str(year_ago)
            if year_ago is not None
            else "N/A"
        ),

        revenue=revenue,
        previous_revenue=previous_revenue,
        year_ago_revenue=year_ago_revenue,

        revenue_qoq=revenue_qoq,
        revenue_yoy=revenue_yoy,

        profit=profit,
        previous_profit=previous_profit,
        year_ago_profit=year_ago_profit,

        profit_qoq=profit_qoq,
        profit_yoy=profit_yoy,

        operating_income=operating_income,
        previous_operating_income=(
            previous_operating_income
        ),

        operating_margin=operating_margin,
        previous_operating_margin=(
            previous_operating_margin
        ),

        margin_change=margin_change,

        cash=cash,
        previous_cash=previous_cash,

        total_debt=total_debt,
        previous_total_debt=previous_total_debt,

        net_debt=net_debt,
        previous_net_debt=previous_net_debt,

        working_capital=working_capital,
        previous_working_capital=(
            previous_working_capital
        ),

        positive_changes=positive_changes,
        negative_changes=negative_changes,

        assessment=assessment,
        data_quality=data_quality,
    )