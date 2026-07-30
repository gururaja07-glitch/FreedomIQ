from mcp.server.fastmcp import FastMCP

from research import dcf
from services.portfolio_service import get_dashboard_data
from services.review_service import get_portfolio_review
from services.research_service import analyze_company

from research.report import build_report
from research.formatter import format_markdown
from research.dcf import DCFEngine

from tools.serialization import to_python


mcp = FastMCP("FreedomIQ")


@mcp.tool()
def get_portfolio_summary() -> dict:
    """Returns the current portfolio summary."""
    dashboard = get_dashboard_data()
    return to_python(dashboard.summary)


@mcp.tool()
def get_top_performers() -> list:
    """Returns the top performing holdings."""
    dashboard = get_dashboard_data()
    return to_python(dashboard.top_performers)


@mcp.tool()
def get_top_losers() -> list:
    """Returns the worst performing holdings."""
    dashboard = get_dashboard_data()
    return to_python(dashboard.top_losers)


@mcp.tool()
def get_portfolio_health() -> dict:
    """Returns the portfolio health assessment."""
    dashboard = get_dashboard_data()
    return to_python(dashboard.health)


@mcp.tool()
def get_portfolio_advice() -> list:
    """Returns portfolio recommendations."""
    dashboard = get_dashboard_data()
    return to_python(dashboard.advisor)


@mcp.tool()
def get_portfolio_risk() -> dict:
    """Returns portfolio risk analysis."""
    dashboard = get_dashboard_data()
    return to_python(dashboard.risk)


@mcp.tool()
def review_portfolio() -> dict:
    """
    Returns a complete portfolio review.
    """
    return get_portfolio_review()



@mcp.tool()
def analyze_company_research(company_name: str) -> str:
    """
    Analyze a company and return a formatted research report.
    """

    analysis = analyze_company(company_name)

    report = build_report(analysis)

    markdown = format_markdown(report)

    return markdown

    # -----------------------------------------------------
    # DCF Forecast Test
    # -----------------------------------------------------

    dcf = DCFEngine(
        analysis.snapshot,
        analysis.financials,
    )

    dcf_result = dcf.calculate()
    forecasts = dcf.forecast_cashflows()

    markdown += "\n\n## DCF Summary\n\n"

    markdown += (
        f"Forecast PV: "
        f"{dcf_result.forecast_pv:,.0f}\n\n"
    )

    markdown += (
        f"Terminal Value: "
        f"{dcf_result.terminal_value:,.0f}\n\n"
    )

    markdown += (
        f"Discounted Terminal Value: "
        f"{dcf_result.discounted_terminal_value:,.0f}\n\n"
    )

    markdown += (
        f"Enterprise Value: "
        f"{dcf_result.enterprise_value:,.0f}\n"
    )

    return markdown


if __name__ == "__main__":
    mcp.run()