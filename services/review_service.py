"""
FreedomIQ

Module : Review Service

Purpose :
Generates a complete portfolio review.

Author : Gururaj N K
Version : 0.2
"""

from services.portfolio_service import get_dashboard_data
from services.investor_action_brief_service import (
    get_investor_action_brief,
)
from tools.serialization import to_python


def get_portfolio_review():
    """
    Returns the complete FreedomIQ portfolio review.
    """

    dashboard = get_dashboard_data()
    action_brief = get_investor_action_brief()

    review = {
        "portfolio": {
            "summary": dashboard.summary,
            "health": dashboard.health,
            "risk": dashboard.risk,
            "advice": dashboard.advisor,
            "top_performers": dashboard.top_performers,
            "top_losers": dashboard.top_losers,
        },
        "investor_action_brief": action_brief,
    }

    return to_python(review)
