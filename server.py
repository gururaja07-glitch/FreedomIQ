from mcp.server.fastmcp import FastMCP

from services.portfolio_service import get_dashboard_data
from tools.serialization import to_python

mcp = FastMCP("FreedomIQ")


@mcp.tool()
def get_portfolio_summary() -> dict:
    """
    Returns the current portfolio summary.
    """
    dashboard = get_dashboard_data()
    return to_python(dashboard.summary)


@mcp.tool()
def get_top_performers() -> list:
    """
    Returns the top performing holdings.
    """
    dashboard = get_dashboard_data()
    return to_python(dashboard.top_performers)


@mcp.tool()
def get_portfolio_health() -> dict:
    """
    Returns the portfolio health assessment.
    """
    dashboard = get_dashboard_data()
    return to_python(dashboard.health)


if __name__ == "__main__":
    mcp.run()