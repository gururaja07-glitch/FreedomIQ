from research.models import ResearchReport

from research.utils import (
    format_indian_currency,
)

REPORT_TITLE = "FreedomIQ Research Report"


def _format_percent(value):
    """Format decimal percentage values."""

    if value is None:
        return "N/A"

    return f"{value * 100:.2f}%"


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

    lines.append(
        f"## {report.snapshot.company}"
    )

    lines.append("")

    lines.append(
        f"**Ticker:** {report.snapshot.ticker}"
    )

    lines.append(
        f"**Sector:** {report.snapshot.sector}"
    )

    lines.append(
        f"**Industry:** {report.snapshot.industry}"
    )

    lines.append(
        f"**Market Cap:** {report.snapshot.market_cap}"
    )

    lines.append("")

    # ---------------------------------------------------------
    # Financial Summary
    # ---------------------------------------------------------

    lines.append("## Financial Summary")
    lines.append("")

    lines.append(
        f"- Revenue Growth: "
        f"{report.financials.revenue_growth}"
    )

    lines.append(
        f"- Profit Growth: "
        f"{report.financials.profit_growth}"
    )

    lines.append(
        f"- Free Cash Flow: "
        f"{format_indian_currency(report.financials.free_cash_flow)}"
    )

    lines.append(
        f"- ROE: {report.financials.roe}"
    )

    lines.append(
        f"- ROCE: {report.financials.roce}"
    )

    lines.append(
        f"- Debt / Equity: "
        f"{report.financials.debt_equity}"
    )

    lines.append(
        f"- Operating Margin: "
        f"{report.financials.operating_margin}"
    )

    lines.append("")

    # ---------------------------------------------------------
    # Valuation
    # ---------------------------------------------------------

    lines.append("## Valuation")
    lines.append("")

    lines.append(
        f"- PE: {report.valuation.pe}"
    )

    lines.append(
        f"- PB: {report.valuation.pb}"
    )

    lines.append(
        f"- EV/EBITDA: {report.valuation.ev_ebitda}"
    )

    lines.append(
        f"- PEG: {report.valuation.peg}"
    )

    lines.append(
        f"- Overall: {report.valuation.valuation}"
    )

    lines.append("")

    # ---------------------------------------------------------
    # FreedomIQ Score
    # ---------------------------------------------------------

    lines.append("## FreedomIQ Score")
    lines.append("")

    lines.append(
        f"**Score:** "
        f"{report.score.total}/100"
    )

    lines.append(
        f"**Rating:** "
        f"{report.score.rating}"
    )

    lines.append(
        f"**Stars:** "
        f"{report.score.stars}"
    )

    lines.append("")

    lines.append("### Score Breakdown")

    lines.append(
        f"- Valuation: "
        f"{report.score.valuation}/20"
    )

    lines.append(
        f"- Growth: "
        f"{report.score.growth}/20"
    )

    lines.append(
        f"- Profitability: "
        f"{report.score.profitability}/20"
    )

    lines.append(
        f"- Financial Strength: "
        f"{report.score.financial_strength}/20"
    )

    lines.append(
        f"- Business Quality: "
        f"{report.score.business_quality}/20"
    )

    lines.append("")

    # ---------------------------------------------------------
    # Reasons
    # ---------------------------------------------------------

    if report.score.reasons:

        lines.append("### Why this score?")
        lines.append("")

        for reason in report.score.reasons:
            lines.append(f"- {reason}")

        lines.append("")

    # ---------------------------------------------------------
    # Strengths
    # ---------------------------------------------------------

    if report.strengths:

        lines.append("## Strengths")
        lines.append("")

        for item in report.strengths:
            lines.append(f"- {item}")

        lines.append("")

    # ---------------------------------------------------------
    # Weaknesses
    # ---------------------------------------------------------

    if report.weaknesses:

        lines.append("## Weaknesses")
        lines.append("")

        for item in report.weaknesses:
            lines.append(f"- {item}")

        lines.append("")

    # ---------------------------------------------------------
    # Risks
    # ---------------------------------------------------------

    if report.risks:

        lines.append("## Risks")
        lines.append("")

        for item in report.risks:
            lines.append(f"- {item}")

        lines.append("")

    # ---------------------------------------------------------
    # Growth Drivers
    # ---------------------------------------------------------

    if report.growth_drivers:

        lines.append("## Growth Drivers")
        lines.append("")

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
        lines.append(
            f"Level : {level}"
        )

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

        # -----------------------------------------------------
        # DCF unavailable
        # -----------------------------------------------------

        if getattr(
            report.dcf,
            "status",
            "Available",
        ) == "Unavailable":

            lines.append(
                "**Status:** DCF Unavailable"
            )

            lines.append("")

            lines.append(
                f"**Reason:** "
                f"{report.dcf.reason}"
            )

            lines.append("")

            lines.append(
                "No intrinsic value or DCF verdict "
                "is provided because the required "
                "free cash flow data is unavailable."
            )

            lines.append("")

        # -----------------------------------------------------
        # Valid DCF
        # -----------------------------------------------------

        else:

            assumptions = (
                report.dcf.assumptions
                or {}
            )

            # -------------------------------------------------
            # Scenario Analysis
            # -------------------------------------------------

            scenarios = assumptions.get(
                "scenarios",
                {},
            )

            if scenarios:

                lines.append(
                    "### DCF Scenario Analysis"
                )

                lines.append("")

                lines.append(
                    "| Scenario | Starting Growth | "
                    "Intrinsic Value / Share |"
                )

                lines.append(
                    "|---|---:|---:|"
                )

                scenario_order = [
                    "Conservative",
                    "Base",
                    "Optimistic",
                ]

                scenario_values = []

                for scenario_name in scenario_order:

                    scenario = scenarios.get(
                        scenario_name
                    )

                    if not scenario:
                        continue

                    start_growth = scenario.get(
                        "start_growth"
                    )

                    value_per_share = scenario.get(
                        "intrinsic_value_per_share"
                    )

                    if value_per_share is not None:
                        scenario_values.append(
                            value_per_share
                        )

                    lines.append(
                        f"| {scenario_name} | "
                        f"{_format_percent(start_growth)} | "
                        f"₹{value_per_share:,.2f} |"
                    )

                lines.append("")

                if scenario_values:

                    lowest = min(
                        scenario_values
                    )

                    highest = max(
                        scenario_values
                    )

                    lines.append(
                        f"**DCF Valuation Range:** "
                        f"₹{lowest:,.2f} – "
                        f"₹{highest:,.2f} per share"
                    )

                    lines.append("")

            # -------------------------------------------------
            # Growth Path
            # -------------------------------------------------

            base_forecasts = (
                report.dcf.forecast_cashflows
                or []
            )

            if base_forecasts:

                lines.append(
                    "### Base Case Growth Path"
                )

                lines.append("")

                lines.append(
                    "| Year | FCF Growth | "
                    "Forecast FCF |"
                )

                lines.append(
                    "|---:|---:|---:|"
                )

                for row in base_forecasts:

                    growth = row.get(
                        "growth"
                    )

                    fcf = row.get(
                        "fcf"
                    )

                    lines.append(
                        f"| {row['year']} | "
                        f"{_format_percent(growth)} | "
                        f"{format_indian_currency(fcf)} |"
                    )

                lines.append("")

                lines.append(
                    f"Terminal Growth: "
                    f"{_format_percent(assumptions.get('terminal_growth'))}"
                )

                lines.append("")
            # -------------------------------------------------
            # DCF Sensitivity Analysis
            # -------------------------------------------------

            sensitivity = assumptions.get(
                "sensitivity",
                {},
            )

            if sensitivity:

                lines.append(
                    "### DCF Sensitivity Analysis"
                )

                lines.append("")

                lines.append(
                    "Base Case FCF forecast with varying "
                    "discount rate and terminal growth."
                )

                lines.append("")

                terminal_growths = [
                    "3.00%",
                    "4.00%",
                    "5.00%",
                ]

                lines.append(
                    "| Discount Rate | 3.00% Terminal | "
                    "4.00% Terminal | 5.00% Terminal |"
                )

                lines.append(
                    "|---:|---:|---:|---:|"
                )

                for rate, values in sensitivity.items():

                    row = [
                        f"| **{rate}** |"
                    ]

                    for growth in terminal_growths:

                        value = values.get(
                            growth
                        )

                        if value is None:

                            row.append(
                                " N/A |"
                            )

                        else:

                            row.append(
                                f" ₹{value:,.2f} |"
                            )

                    lines.append(
                        "".join(row)
                    )

                lines.append("")

                lines.append(
                    "Sensitivity shows how the Base Case "
                    "valuation changes when the discount "
                    "rate and terminal growth assumptions "
                    "change."
                )

                lines.append("")
            # -------------------------------------------------
            # Primary Base Case DCF
            # -------------------------------------------------

            lines.append(
                "### DCF Valuation — Base Case"
            )

            lines.append("")

            lines.append(
                f"Forecast Cash Flow PV: "
                f"{report.dcf.forecast_pv:,.0f}"
            )

            lines.append(
                f"Terminal Value: "
                f"{report.dcf.terminal_value:,.0f}"
            )

            lines.append(
                f"Discounted Terminal Value: "
                f"{report.dcf.discounted_terminal_value:,.0f}"
            )

            lines.append(
                f"Enterprise Value: "
                f"{report.dcf.enterprise_value:,.0f}"
            )

            lines.append(
                f"Intrinsic Value: "
                f"{report.dcf.intrinsic_value:,.0f}"
            )

            lines.append(
                f"Intrinsic Value / Share: "
                f"{report.dcf.intrinsic_value_per_share:,.2f}"
            )

            lines.append(
                f"Current Price: "
                f"{report.dcf.current_price:,.2f}"
            )

            lines.append(
                f"Margin of Safety: "
                f"{report.dcf.margin_of_safety:.2f}%"
            )

            lines.append(
                f"Verdict: "
                f"{report.dcf.verdict}"
            )

            lines.append("")

            # -------------------------------------------------
            # DCF Assumptions & Audit
            # -------------------------------------------------

            lines.append(
                "### DCF Assumptions & Audit"
            )

            lines.append("")

            if "base_fcf" in assumptions:

                lines.append(
                    f"- Base FCF: "
                    f"{format_indian_currency(assumptions['base_fcf'])}"
                )

            if "growth_method" in assumptions:

                lines.append(
                    f"- Growth Method: "
                    f"{assumptions['growth_method']}"
                )

            if "discount_rate" in assumptions:

                lines.append(
                    f"- Discount Rate: "
                    f"{_format_percent(assumptions['discount_rate'])}"
                )

            if "terminal_growth" in assumptions:

                lines.append(
                    f"- Terminal Growth: "
                    f"{_format_percent(assumptions['terminal_growth'])}"
                )

            if "years" in assumptions:

                lines.append(
                    f"- Forecast Period: "
                    f"{assumptions['years']} years"
                )

            if "cash" in assumptions:

                lines.append(
                    f"- Cash: "
                    f"{format_indian_currency(assumptions['cash'])}"
                )

            if "debt" in assumptions:

                lines.append(
                    f"- Debt: "
                    f"{format_indian_currency(assumptions['debt'])}"
                )

            if "shares_outstanding" in assumptions:

                lines.append(
                    f"- Shares Outstanding: "
                    f"{assumptions['shares_outstanding']:,.0f}"
                )

            if "terminal_value_percentage" in assumptions:

                lines.append(
                    f"- Base Terminal Value Contribution: "
                    f"{assumptions['terminal_value_percentage']:.2f}%"
                )

            lines.append("")

    return "\n".join(lines)