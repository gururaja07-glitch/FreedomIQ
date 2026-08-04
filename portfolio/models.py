"""
FreedomIQ

Module : Portfolio Models

Purpose :
Contains all portfolio data models.

Author : Gururaj N K
Version : 1.0
"""

from dataclasses import dataclass


@dataclass
class InvestmentDecision:
    """
    Represents a portfolio investment decision.
    """

    issue: str
    reason: str
    action: str
    priority: str
