from mcp.server.fastmcp import FastMCP
from services.decision_service import (
    get_investment_decision as generate_investment_decision
)

from portfolio.loader import get_portfolio as legacy_get_portfolio
from portfolio.metrics import calculate_metrics as legacy_calculate_metrics
from portfolio.dashboard import get_portfolio_dashboard

from services.portfolio_service import get_dashboard_data
from services.review_service import get_portfolio_review
from services.research_service import analyze_company

from research.report import build_report
from research.formatter import format_markdown
from research.dcf import DCFEngine

from tools.portfolio import get_portfolio
from tools.analytics import calculate_metrics
from tools.serialization import to_python
from services.portfolio_decision_service import (
    get_portfolio_decisions as generate_portfolio_decisions
)
from services.portfolio_committee_service import (
    get_portfolio_investment_committee as generate_portfolio_committee,
)
from services.prepare_portfolio_data import prepare_portfolio_data
from tools.analytics import calculate_portfolio_summary

mcp = FastMCP("FreedomIQ")


# ==========================================================
# Portfolio Summary
# ==========================================================

@mcp.tool()
def get_portfolio_summary() -> dict:
    """
    Returns the current portfolio summary.
    """
    try:
        df = prepare_portfolio_data()
        summary = calculate_portfolio_summary(df)
        return summary

    except Exception as e:
        import traceback

        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
        }

# ==========================================================
# Portfolio Performance
# ==========================================================

@mcp.tool()
def get_top_performers() -> list:
    """
    Returns the top performing holdings.
    """
    dashboard = get_dashboard_data()
    return to_python(dashboard.top_performers)


@mcp.tool()
def get_top_losers() -> list:
    """
    Returns the worst performing holdings.
    """
    dashboard = get_dashboard_data()
    return to_python(dashboard.top_losers)


# ==========================================================
# Portfolio Health
# ==========================================================

@mcp.tool()
def get_portfolio_health() -> dict:
    """
    Returns the portfolio health assessment.
    """
    dashboard = get_dashboard_data()
    return to_python(dashboard.health)


@mcp.tool()
def get_portfolio_advice() -> list:
    """
    Returns portfolio recommendations.
    """
    dashboard = get_dashboard_data()
    return to_python(dashboard.advisor)


@mcp.tool()
def get_portfolio_risk() -> dict:
    """
    Returns portfolio risk analysis.
    """
    dashboard = get_dashboard_data()
    return to_python(dashboard.risk)


# ==========================================================
# Complete Portfolio Review
# ==========================================================

@mcp.tool()
def review_portfolio() -> dict:
    """
    Returns a complete portfolio review.
    """
    return get_portfolio_review()


# ==========================================================
# Company Research
# ==========================================================

@mcp.tool()
def analyze_company_research(company_name: str) -> str:
    """
    Analyze a company and return a formatted research report
    including DCF valuation.
    """

    analysis = analyze_company(company_name)

    report = build_report(analysis)

    markdown = format_markdown(report)
    # ==========================================================
# Investment Decision
# ==========================================================

@mcp.tool()
def get_investment_decision(company_name: str) -> dict:
    """
    Returns the personal investment decision for a portfolio holding.

    Includes:
    - Fundamental rating
    - Valuation
    - FCF quality
    - DCF verdict
    - Financial data quality
    - Portfolio exposure
    - Confidence
    - Evidence
    - Risks
    """
    decision = generate_investment_decision(
        company_name
    )

    return to_python(decision)

    # ------------------------------------------------------
    # DCF
    # ------------------------------------------------------

    dcf_engine = DCFEngine(
        analysis.snapshot,
        analysis.financials,
    )

    dcf_result = dcf_engine.calculate()

    if dcf_result.status == "Available":
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


# ==========================================================
# Portfolio Metrics
# ==========================================================

@mcp.tool()
def get_portfolio_metrics() -> dict:
    """
    Returns portfolio concentration metrics.
    """
    try:
        portfolio = get_portfolio()
        df = calculate_metrics(portfolio)

        sorted_df = df.sort_values(
            "Weight %",
            ascending=False
        )

        return {
            "Top 5 Weight": round(
                sorted_df.head(5)["Weight %"].sum(), 2
            ),
            "Top 10 Weight": round(
                sorted_df.head(10)["Weight %"].sum(), 2
            ),
            "Largest Holding": sorted_df.iloc[0]["Stock"],
            "Largest Weight": round(
                sorted_df.iloc[0]["Weight %"], 2
            ),
        }

    except Exception as e:
        import traceback

        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
        }

# ==========================================================
# Portfolio Score
# ==========================================================

@mcp.tool()
def get_portfolio_score() -> dict:
    """
    Returns the current FreedomIQ portfolio health score.
    """
    dashboard = get_dashboard_data()

    return {
        "Health Score": dashboard.health["Total"]
    }


# ==========================================================
# AI Portfolio Advice
# ==========================================================

@mcp.tool()
def get_portfolio_ai_advice() -> list:
    """
    Returns portfolio recommendations.
    """
    dashboard = get_dashboard_data()

    return to_python(dashboard.advisor)


# ==========================================================
# Complete Portfolio Dashboard
# ==========================================================

@mcp.tool()
def get_portfolio_dashboard_data() -> dict:
    """
    Returns the complete FreedomIQ portfolio dashboard.
    """
    dashboard = get_dashboard_data()

    return to_python(dashboard)


# ==========================================================
# Portfolio Decisions
# ==========================================================
@mcp.tool()
def get_portfolio_decisions() -> list:
    """
    Returns portfolio-level investment decisions.
    """
    return to_python(generate_portfolio_decisions())
# ==========================================================
# Portfolio Investment Committee
# ==========================================================

@mcp.tool()
def get_portfolio_investment_committee() -> dict:
    """
    Returns the complete portfolio investment committee analysis.
    """
    return to_python(
        generate_portfolio_committee()
    )

# ==========================================================
# Start MCP Server
# ==========================================================

if __name__ == "__main__":
    mcp.run()