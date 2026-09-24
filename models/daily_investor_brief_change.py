from dataclasses import dataclass


@dataclass
class DailyInvestorBriefChange:
    """
    Represents one meaningful change between two Daily Investor Briefs.
    """

    category: str
    title: str
    previous_value: str
    current_value: str
    priority: str
    description: str


@dataclass
class DailyInvestorBriefChangeResult:
    """
    Represents the complete comparison between two Daily Investor Briefs.
    """

    previous_date: str | None
    current_date: str
    changes: list[DailyInvestorBriefChange]
    summary: str