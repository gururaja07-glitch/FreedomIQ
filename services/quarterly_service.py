@'
from research.quarterly import analyze_quarterly_result


def get_quarterly_result(company_name: str):
    """
    Return the structured quarterly result for a company.
    """

    return analyze_quarterly_result(company_name)
'@ | Set-Content services\quarterly_service.py