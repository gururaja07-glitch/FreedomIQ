import yfinance as yf

from research.models import FinancialSummary
from research.utils import (
    format_percent,
    format_ratio,
)


def _get_fx_rate(
    from_currency: str,
    to_currency: str,
):
    """
    Get the latest FX rate from Yahoo Finance.

    Example:
        USD -> INR
        Yahoo symbol: USDINR=X

    Returns None if the FX rate cannot be obtained.
    """

    if not from_currency or not to_currency:
        return None

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == to_currency:
        return 1.0

    fx_symbol = f"{from_currency}{to_currency}=X"

    try:
        fx = yf.Ticker(fx_symbol)

        history = fx.history(period="5d")

        if history is None or history.empty:
            return None

        close = history["Close"].dropna()

        if close.empty:
            return None

        return float(close.iloc[-1])

    except Exception:
        return None


def _convert_value(
    value,
    fx_rate,
):
    """
    Convert a numeric value using the supplied FX rate.
    """

    if value is None or fx_rate is None:
        return None

    try:
        return float(value) * fx_rate

    except (TypeError, ValueError):
        return None


def _get_free_cash_flow(
    info: dict,
    ticker_symbol: str | None = None,
    fx_rate: float = 1.0,
):
    """
    Get free cash flow from Yahoo Finance.

    Primary source:
        ticker.info["freeCashflow"]

    Fallback source:
        ticker.cashflow["Free Cash Flow"]

    The resulting value is converted into the quote
    currency using fx_rate.
    """

    # -----------------------------------------------------
    # Primary source: Yahoo Finance info
    # -----------------------------------------------------

    free_cash_flow = info.get("freeCashflow")

    if free_cash_flow is not None:

        try:
            value = float(free_cash_flow)

            return value * fx_rate

        except (TypeError, ValueError):
            pass

    # -----------------------------------------------------
    # Fallback source: Yahoo Finance cash-flow statement
    # -----------------------------------------------------

    if ticker_symbol is None:
        return None

    try:

        ticker = yf.Ticker(ticker_symbol)

        cashflow = ticker.cashflow

        if cashflow is None or cashflow.empty:
            return None

        if "Free Cash Flow" not in cashflow.index:
            return None

        fcf_series = cashflow.loc["Free Cash Flow"]

        fcf_series = fcf_series.dropna()

        if fcf_series.empty:
            return None

        # Latest annual value
        fcf_series = fcf_series.sort_index(
            ascending=False
        )

        value = float(fcf_series.iloc[0])

        return value * fx_rate

    except Exception:
        return None


def get_financials(
    info: dict,
    ticker_symbol: str | None = None,
) -> FinancialSummary:
    """
    Extract financial metrics from Yahoo Finance.

    Financial statement values may be reported in a
    different currency from the market quote currency.

    When currencies differ, Yahoo Finance FX data is used
    to normalize FCF, cash and debt into the quote currency.

    If currency conversion is required but the FX rate
    cannot be obtained, DCF-relevant values are returned
    as unavailable rather than producing a misleading
    valuation.
    """

    # -----------------------------------------------------
    # Currency information
    # -----------------------------------------------------

    quote_currency = info.get("currency")
    financial_currency = info.get("financialCurrency")

    if not quote_currency:
        quote_currency = financial_currency

    if not financial_currency:
        financial_currency = quote_currency

    # -----------------------------------------------------
    # Currency conversion
    # -----------------------------------------------------

    fx_rate = _get_fx_rate(
        financial_currency,
        quote_currency,
    )

    currency_conversion_available = (
        fx_rate is not None
    )

    # -----------------------------------------------------
    # Basic financial metrics
    # -----------------------------------------------------

    revenue_growth = format_percent(
        info.get("revenueGrowth")
    )

    profit_growth = format_percent(
        info.get("earningsGrowth")
    )

    roe = format_percent(
        info.get("returnOnEquity")
    )

    # Yahoo Finance does not provide ROCE directly.
    roce = "N/A"

    debt_equity = format_ratio(
        info.get("debtToEquity")
    )

    operating_margin = format_percent(
        info.get("operatingMargins")
    )

    # -----------------------------------------------------
    # FCF / Cash / Debt
    # -----------------------------------------------------

    if currency_conversion_available:

        free_cash_flow = _get_free_cash_flow(
            info,
            ticker_symbol,
            fx_rate,
        )

        cash = _convert_value(
            info.get("totalCash"),
            fx_rate,
        )

        total_debt = _convert_value(
            info.get("totalDebt"),
            fx_rate,
        )

    else:

        # If currencies differ and FX data is unavailable,
        # do not pass potentially incompatible monetary
        # values into the DCF.

        if (
            quote_currency
            and financial_currency
            and quote_currency.upper()
            != financial_currency.upper()
        ):

            free_cash_flow = None
            cash = None
            total_debt = None

        else:

            free_cash_flow = _get_free_cash_flow(
                info,
                ticker_symbol,
                1.0,
            )

            cash = info.get("totalCash")
            total_debt = info.get("totalDebt")

    return FinancialSummary(
        revenue_growth=revenue_growth,
        profit_growth=profit_growth,
        roe=roe,
        roce=roce,
        debt_equity=debt_equity,
        operating_margin=operating_margin,

        free_cash_flow=free_cash_flow,

        cash=cash,

        total_debt=total_debt,
    )
def _get_free_cash_flow_history(
    info: dict,
    ticker_symbol: str | None = None,
    fx_rate: float = 1.0,
):
    """
    Get historical annual free cash flow from Yahoo Finance.

    Returns:
        List of dictionaries containing:
            date
            fcf
    """

    if ticker_symbol is None:
        return []

    try:

        ticker = yf.Ticker(ticker_symbol)

        cashflow = ticker.cashflow

        if cashflow is None or cashflow.empty:
            return []

        if "Free Cash Flow" not in cashflow.index:
            return []

        fcf_series = (
            cashflow.loc["Free Cash Flow"]
            .dropna()
            .sort_index(ascending=False)
        )

        history = []

        for date, value in fcf_series.items():

            try:

                fcf = (
                    float(value)
                    * fx_rate
                )

                history.append(
                    {
                        "date": str(date),
                        "fcf": fcf,
                    }
                )

            except (
                TypeError,
                ValueError,
            ):
                continue

        return history

    except Exception:

        return []