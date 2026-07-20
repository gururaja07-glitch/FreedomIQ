"""
FreedomIQ

Module : Review Service

Purpose :
Generates a complete portfolio review.

Author : Gururaj N K
Version : 0.1
"""

from services.portfolio_service import get_dashboard_data
from tools.serialization import to_python


def get_portfolio_review():
    """
    Returns a complete portfolio review.
    """

    dashboard = get_dashboard_data()

    review = {
        "summary": dashboard.summary,
        "health": dashboard.health,
        "risk": dashboard.risk,
        "advice": dashboard.advisor,
        "top_performers": dashboard.top_performers,
        "top_losers": dashboard.top_losers,
    }

    return to_python(review)