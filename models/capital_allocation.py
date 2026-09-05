from dataclasses import dataclass


@dataclass
class CapitalAllocationRecommendation:
    """
    Recommended allocation of new capital
    to an individual portfolio holding.
    """

    company: str
    amount: float
    allocation_percent: float

    decision: str
    confidence: str

    reason: str


@dataclass
class CapitalAllocationPlan:
    """
    Complete recommendation for deploying
    new capital across the portfolio.
    """

    available_capital: float

    recommendations: list[
        CapitalAllocationRecommendation
    ]

    unallocated_capital: float

    summary: str