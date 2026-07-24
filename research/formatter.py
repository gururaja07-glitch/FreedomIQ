from research.models import ResearchReport


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
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(report.summary)
    lines.append("")
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
    # Score
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
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(report.summary)
        lines.append("")

    # ---------------------------------------------------------
    # Confidence
    # ---------------------------------------------------------

    lines.append("## Confidence")
    lines.append("")
    lines.append(report.confidence)

    return "\n".join(lines)