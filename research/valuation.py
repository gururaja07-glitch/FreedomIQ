from research.models import ValuationSummary
from research.utils import safe_float, format_ratio


def get_valuation(info: dict) -> ValuationSummary:
    """
    Extract valuation metrics and assign a valuation score based on
    multiple valuation parameters.

    The 'valuation' field is derived from the overall score rather than
    a single metric like PE.
    """

    pe = safe_float(info.get("trailingPE"))
    pb = safe_float(info.get("priceToBook"))
    peg = safe_float(info.get("pegRatio"))
    ev_ebitda = safe_float(info.get("enterpriseToEbitda"))

    score = 0
    metrics_used = 0

    # -------------------------
    # PE Score
    # -------------------------
    if pe is not None:
        metrics_used += 1

        if pe <= 15:
            score += 5
        elif pe <= 20:
            score += 4
        elif pe <= 25:
            score += 3
        elif pe <= 35:
            score += 2
        else:
            score += 1

    # -------------------------
    # PB Score
    # -------------------------
    if pb is not None:
        metrics_used += 1

        if pb <= 2:
            score += 5
        elif pb <= 4:
            score += 4
        elif pb <= 6:
            score += 3
        elif pb <= 8:
            score += 2
        else:
            score += 1

    # -------------------------
    # PEG Score
    # -------------------------
    if peg is not None:
        metrics_used += 1

        if peg <= 1:
            score += 5
        elif peg <= 1.5:
            score += 4
        elif peg <= 2:
            score += 3
        elif peg <= 3:
            score += 2
        else:
            score += 1

    # -------------------------
    # EV / EBITDA Score
    # -------------------------
    if ev_ebitda is not None:
        metrics_used += 1

        if ev_ebitda <= 8:
            score += 5
        elif ev_ebitda <= 12:
            score += 4
        elif ev_ebitda <= 16:
            score += 3
        elif ev_ebitda <= 20:
            score += 2
        else:
            score += 1

    # -------------------------
    # Overall Valuation Label
    # -------------------------
    if metrics_used == 0:
        valuation = "Unknown"
    else:
        max_score = metrics_used * 5
        percentage = score / max_score

        if percentage >= 0.80:
            valuation = "Undervalued"
        elif percentage >= 0.60:
            valuation = "Fairly Valued"
        else:
            valuation = "Expensive"

    return ValuationSummary(
        pe=format_ratio(pe),
        pb=format_ratio(pb),
        ev_ebitda=format_ratio(ev_ebitda),
        peg=format_ratio(peg),
        valuation=valuation,
    )