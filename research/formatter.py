from research.models import ResearchReport
from research.utils import (
    format_currency,
    format_indian_currency,
)

REPORT_TITLE = "FreedomIQ Research Report"


def format_markdown(report: ResearchReport) -> str:
    """
    Converts a ResearchReport into a Markdown report.
    """

    lines = []

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    lines.append(f"# {REPORT_TITLE}")
    lines.append("")

    # ---------------------------------------------------------
    # Executive Summary
    # ---------------------------------------------------------

    lines.append("## Executive Summary")
    lines.append("")
    lines.append(report.summary)
    lines.append("")

    # ---------------------------------------------------------
    # Investment Thesis
    # ---------------------------------------------------------

    if report.investment_thesis:
        lines.append("## Investment Thesis")
        lines.append("")
        lines.append(report.investment_thesis)
        lines.append("")

    # ---------------------------------------------------------
    # Company Snapshot
    # ---------------------------------------------------------

    lines.append(f"## {report.snapshot.company}")
    lines.append("")
    lines.append(f"**Ticker:** {report.snapshot.ticker}")
    lines.append(f"**Sector:** {report.snapshot.sector}")
    lines.append(f"**Industry:** {report.snapshot.industry}")
    lines.append(f"**Market Cap:** {report.snapshot.market_cap}")
    lines.append("")

    # ---------------------------------------------------------
    # Financial Summary
    # ---------------------------------------------------------

    lines.append("## Financial Summary")
    lines.append("")

    lines.append(f"- Revenue Growth: {report.financials.revenue_growth}")
    lines.append(f"- Profit Growth: {report.financials.profit_growth}")
    lines.append(
        f"- Free Cash Flow: {format_indian_currency(report.financials.free_cash_flow)}"
    )
    lines.append(f"- ROE: {report.financials.roe}")
    lines.append(f"- ROCE: {report.financials.roce}")
    lines.append(f"- Debt / Equity: {report.financials.debt_equity}")
    lines.append(f"- Operating Margin: {report.financials.operating_margin}")
    lines.append("")

    # ---------------------------------------------------------
    # Valuation
    # ---------------------------------------------------------

    lines.append("## Valuation")
    lines.append("")

    lines.append(f"- PE: {report.valuation.pe}")
    lines.append(f"- PB: {report.valuation.pb}")
    lines.append(f"- EV/EBITDA: {report.valuation.ev_ebitda}")
    lines.append(f"- PEG: {report.valuation.peg}")
    lines.append(f"- Overall: {report.valuation.valuation}")
    lines.append("")

    # ---------------------------------------------------------
    # FreedomIQ Score
    # ---------------------------------------------------------

    lines.append("## FreedomIQ Score")
    lines.append("")

    lines.append(f"**Score:** {report.score.total}/100")
    lines.append(f"**Rating:** {report.score.rating}")
    lines.append(f"**Stars:** {report.score.stars}")
    lines.append("")

    lines.append("### Score Breakdown")
    lines.append(f"- Valuation: {report.score.valuation}/20")
    lines.append(f"- Growth: {report.score.growth}/20")
    lines.append(f"- Profitability: {report.score.profitability}/20")
    lines.append(f"- Financial Strength: {report.score.financial_strength}/20")
    lines.append(f"- Business Quality: {report.score.business_quality}/20")
    lines.append("")

    # ---------------------------------------------------------
    # Reasons
    # ---------------------------------------------------------

    if report.score.reasons:
        lines.append("### Why this score?")

        for reason in report.score.reasons:
            lines.append(f"- {reason}")

        lines.append("")

    # ---------------------------------------------------------
    # Strengths
    # ---------------------------------------------------------

    if report.strengths:
        lines.append("## Strengths")

        for item in report.strengths:
            lines.append(f"- {item}")

        lines.append("")

    # ---------------------------------------------------------
    # Weaknesses
    # ---------------------------------------------------------

    if report.weaknesses:
        lines.append("## Weaknesses")

        for item in report.weaknesses:
            lines.append(f"- {item}")

        lines.append("")

    # ---------------------------------------------------------
    # Risks
    # ---------------------------------------------------------

    if report.risks:
        lines.append("## Risks")

        for item in report.risks:
            lines.append(f"- {item}")

        lines.append("")

    # ---------------------------------------------------------
    # Growth Drivers
    # ---------------------------------------------------------

    if report.growth_drivers:
        lines.append("## Growth Drivers")

        for item in report.growth_drivers:
            lines.append(f"- {item}")

        lines.append("")

    # ---------------------------------------------------------
    # Confidence
    # ---------------------------------------------------------

    lines.append("## Confidence")
    lines.append("")

    confidence = report.confidence

    if isinstance(confidence, dict):
        stars = confidence["stars"]
        level = confidence["level"]
        reasons = confidence["reasons"]

    elif hasattr(confidence, "stars"):
        stars = confidence.stars
        level = confidence.level
        reasons = confidence.reasons

    else:
        lines.append(str(confidence))
        lines.append("")
        stars = None
        level = None
        reasons = None

    if stars is not None:
        lines.append(stars)
        lines.append(f"Level : {level}")
        lines.append("")

        lines.append("Reasons:")

        for reason in reasons:
            lines.append(f"- {reason}")

    lines.append("")

    # ---------------------------------------------------------
    # DCF Valuation
    # ---------------------------------------------------------

    if report.dcf:

        lines.append("## DCF Valuation")
        lines.append("")

        lines.append(
            f"Forecast Cash Flow PV: {report.dcf.forecast_pv:,.0f}"
        )

        lines.append(
            f"Terminal Value: {report.dcf.terminal_value:,.0f}"
        )

        lines.append(
            f"Discounted Terminal Value: {report.dcf.discounted_terminal_value:,.0f}"
        )

        lines.append(
            f"Enterprise Value: {report.dcf.enterprise_value:,.0f}"
        )

        lines.append(
            f"Intrinsic Value: {report.dcf.intrinsic_value:,.0f}"
        )

        lines.append(
            f"Intrinsic Value / Share: {report.dcf.intrinsic_value_per_share:,.2f}"
        )

        lines.append(
            f"Current Price: {report.dcf.current_price:,.2f}"
        )

    return "\n".join(lines)
