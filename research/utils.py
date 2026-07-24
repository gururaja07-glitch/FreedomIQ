"""
=========================================================
FreedomIQ Utility Functions
---------------------------------------------------------
Common formatting and conversion helpers used across
the research engine.

These utilities ensure consistent presentation of
financial data throughout the application.
=========================================================
"""


def safe_float(value):
    """
    Safely convert values to float.

    Returns None if conversion fails.
    """

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def format_ratio(value, decimals=2):
    """
    Format valuation ratios like PE, PB, PEG, EV/EBITDA.
    """

    value = safe_float(value)

    if value is None:
        return "N/A"

    return f"{value:.{decimals}f}"


def format_percent(value):
    """
    Convert decimal values into percentages.

    Example:
        0.2386 -> 23.86%
    """

    value = safe_float(value)

    if value is None:
        return "N/A"

    return f"{value * 100:.2f}%"


def format_number(value):
    """
    Format ordinary numbers.

    Example:
        1234567 -> 1,234,567
    """

    value = safe_float(value)

    if value is None:
        return "N/A"

    return f"{value:,.0f}"


def format_market_cap(value):
    """
    Format market capitalization.

    Examples

        8156254568448
            ->
        ₹8.16 T

        145000000000
            ->
        ₹145.00 B
    """

    value = safe_float(value)

    if value is None:
        return "N/A"

    trillion = 1_000_000_000_000
    billion = 1_000_000_000
    million = 1_000_000

    if value >= trillion:
        return f"₹{value / trillion:.2f} T"

    if value >= billion:
        return f"₹{value / billion:.2f} B"

    if value >= million:
        return f"₹{value / million:.2f} M"

    return format_number(value)


def format_currency(value):
    """
    Format currency values.

    Example

        1234.5
            ->
        ₹1,234.50
    """

    value = safe_float(value)

    if value is None:
        return "N/A"

    return f"₹{value:,.2f}"