from research.models import ValuationSummary


def get_valuation(info: dict) -> ValuationSummary:
    """
    Extract valuation metrics from Yahoo Finance info dictionary.
    """

    pe = info.get("trailingPE")
    pb = info.get("priceToBook")
    peg = info.get("pegRatio")

    valuation = "Unknown"

    try:
        if pe is not None:
            pe = float(pe)

            if pe < 20:
                valuation = "Undervalued"

            elif pe < 30:
                valuation = "Fair"

            else:
                valuation = "Expensive"

    except Exception:
        pass

    return ValuationSummary(
        pe=str(pe) if pe is not None else "N/A",
        pb=str(pb) if pb is not None else "N/A",
        ev_ebitda="N/A",
        peg=str(peg) if peg is not None else "N/A",
        valuation=valuation,
    )