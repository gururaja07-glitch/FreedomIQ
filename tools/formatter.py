"""
FreedomIQ

Module : Formatter

Purpose :
Common formatting utilities.

Author : Gururaj N K
Version : 0.2
"""


def format_money(value):
    """
    Format Indian currency.
    """

    if value is None:
        return "-"

    return f"₹{value:,.0f}"


def format_percentage(value):
    """
    Format percentage.
    """

    if value is None:
        return "-"

    return f"{value:.1f}%"


def format_number(value):
    """
    Format numbers.
    """

    if value is None:
        return "-"

    return f"{value:,.2f}"