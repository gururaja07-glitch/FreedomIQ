"""
FreedomIQ FCF Analysis

Analyzes historical free cash flow quality.
This module does not change DCF valuation assumptions.
"""


def analyze_fcf_history(fcf_history):
    """
    Analyze historical FCF data.

    Expected input:
        [
            {"date": "...", "fcf": value},
            ...
        ]

    Returns a dictionary containing:
        - positive_years
        - negative_years
        - fcf_cagr
        - average_growth
        - volatility
        - trend
        - stability
        - quality
    """

    if not fcf_history:
        return {
            "positive_years": 0,
            "negative_years": 0,
            "fcf_cagr": None,
            "average_growth": None,
            "volatility": None,
            "trend": "Unavailable",
            "stability": "Unavailable",
            "quality": "Unavailable",
        }

    values = []

    for row in fcf_history:

        try:
            value = float(row["fcf"])
            values.append(value)

        except (
            KeyError,
            TypeError,
            ValueError,
        ):
            continue

    if not values:
        return {
            "positive_years": 0,
            "negative_years": 0,
            "fcf_cagr": None,
            "average_growth": None,
            "volatility": None,
            "trend": "Unavailable",
            "stability": "Unavailable",
            "quality": "Unavailable",
        }

    positive_years = sum(
        1 for value in values
        if value > 0
    )

    negative_years = sum(
        1 for value in values
        if value < 0
    )

    # -----------------------------------------------------
    # Year-over-year growth
    # -----------------------------------------------------

    growth_rates = []

    for previous, current in zip(
        values[1:],
        values[:-1],
    ):

        if previous > 0:

            growth = (
                (current - previous)
                / previous
            )

            growth_rates.append(growth)

       # -----------------------------------------------------
    # CAGR
    # -----------------------------------------------------

    fcf_cagr = None

    # CAGR is meaningful only when the oldest and
    # latest observations are both positive.
    #
    # We deliberately do not skip over negative FCF years.
    # A negative year can make a calculated CAGR misleading.

    if len(values) >= 2:

        oldest = values[-1]
        latest = values[0]

        periods = len(values) - 1

        if (
            oldest > 0
            and latest > 0
            and periods > 0
        ):

            fcf_cagr = (
                (latest / oldest)
                ** (1 / periods)
            ) - 1
       # -----------------------------------------------------
    # Average growth
    # -----------------------------------------------------

    average_growth = None

    if growth_rates:

        average_growth = (
            sum(growth_rates)
            / len(growth_rates)
        )

       

    # -----------------------------------------------------
    # Growth volatility
    # -----------------------------------------------------

    volatility = None

    if len(growth_rates) >= 2:

        mean = (
            sum(growth_rates)
            / len(growth_rates)
        )

        variance = (
            sum(
                (growth - mean) ** 2
                for growth in growth_rates
            )
            / len(growth_rates)
        )

        volatility = variance ** 0.5
    # -----------------------------------------------------
    # Average growth quality check
    # -----------------------------------------------------

    if (
        average_growth is not None
        and volatility is not None
        and volatility > 0.50
    ):
        average_growth = None
  

    # -----------------------------------------------------
    # Trend
    # -----------------------------------------------------

    if len(values) < 2:

        trend = "Insufficient Data"

    elif values[0] > values[-1]:

        trend = "Improving"

    elif values[0] < values[-1]:

        trend = "Declining"

    else:

        trend = "Flat"

    # -----------------------------------------------------
    # Stability
    # -----------------------------------------------------

    if volatility is None:

        stability = "Unknown"

    elif volatility <= 0.10:

        stability = "High"

    elif volatility <= 0.30:

        stability = "Moderate"

    else:

        stability = "Low"
    # -----------------------------------------------------
    # Volatility-aware trend
    # -----------------------------------------------------

    if stability == "Low":

     if trend == "Improving":

        trend = "Volatile / Improving"

    elif trend == "Declining":

        trend = "Volatile / Declining"
    # -----------------------------------------------------
    # Overall quality
    # -----------------------------------------------------

    if negative_years > 0:

        quality = "Low"

    elif stability == "High":

        quality = "High"

    elif stability == "Moderate":

        quality = "Moderate"

    else:

        quality = "Low"

    return {
        "positive_years": positive_years,
        "negative_years": negative_years,
        "fcf_cagr": fcf_cagr,
        "average_growth": average_growth,
        "volatility": volatility,
        "trend": trend,
        "stability": stability,
        "quality": quality,
    }