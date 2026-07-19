from services.portfolio_service import get_dashboard_data
from tools.serialization import to_python


def register(mcp):

    @mcp.tool()
    def get_portfolio_summary() -> dict:
        """
        Returns the current portfolio summary.
        """
        dashboard = get_dashboard_data()
        return to_python(dashboard.summary)