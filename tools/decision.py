from models.decision import InvestmentDecision


def _get_fcf_assessment(company_analysis):
    """
    Read the existing FCF quality analysis produced by the DCF engine.

    No new FCF calculations are performed here.
    """

    dcf = company_analysis.dcf

    if dcf is None:
        return (
            "FCF quality analysis is unavailable.",
            None,
        )

    assumptions = dcf.assumptions or {}

    quality = assumptions.get(
        "fcf_quality",
        "Unavailable",
    )

    stability = assumptions.get(
        "fcf_stability",
        "Unavailable",
    )

    trend = assumptions.get(
        "fcf_trend",
        "Unavailable",
    )

    positive_years = assumptions.get(
        "positive_fcf_years",
        0,
    )

    negative_years = assumptions.get(
        "negative_fcf_years",
        0,
    )

    if quality == "High":

        assessment = (
            "FCF quality is High with "
            f"{positive_years} positive FCF years."
        )

        return assessment, None

    if quality == "Moderate":

        assessment = (
            "FCF quality is Moderate. "
            f"Trend is {trend} and stability is {stability}."
        )

        return (
            assessment,
            "FCF quality is not consistently strong.",
        )

    if quality == "Low":

        assessment = (
            "FCF quality is Low. "
            f"Available history contains "
            f"{negative_years} negative FCF years."
        )

        return (
            assessment,
            "FCF quality requires monitoring.",
        )

    return (
        "FCF quality analysis is unavailable.",
        None,
    )


def _get_dcf_assessment(company_analysis):
    """
    Read the existing DCF result.
    """

    dcf = company_analysis.dcf

    if dcf is None:
        return (
            "DCF valuation is unavailable.",
            None,
        )

    if getattr(dcf, "status", "Unavailable") != "Available":

        reason = getattr(
            dcf,
            "reason",
            "DCF valuation is unavailable.",
        )

        return (
            f"DCF valuation is unavailable: {reason}",
            None,
        )

    verdict = getattr(
        dcf,
        "verdict",
        "Unavailable",
    )

    margin = getattr(
        dcf,
        "margin_of_safety",
        None,
    )

    if margin is not None:

        assessment = (
            f"DCF verdict is {verdict} with a "
            f"{margin:.1f}% margin of safety."
        )

        return assessment, None

    return (
        f"DCF verdict is {verdict}.",
        None,
    )


def make_investment_decision(
    company_analysis,
    portfolio_row,
    portfolio_risk,
):
    """
    Generate an integrated investment decision.

    Combines:

    - Fundamental rating
    - Valuation
    - Existing FCF quality analysis
    - DCF valuation
    - Portfolio exposure
    - Portfolio risk
    - Company-specific risks
    - Confidence
    """

    rating = company_analysis.score.rating

    valuation = (
        company_analysis.valuation.valuation
    )

    confidence = company_analysis.confidence

    weight = float(
        portfolio_row["Weight %"]
    )

    company = portfolio_row["Stock"]

    reasons = []
    risks = []

    # ------------------------------------------------------
    # 1. Fundamental assessment
    # ------------------------------------------------------

    if rating == "Sell":

        decision = "SELL"

        reasons.append(
            "Company fundamentals are rated Sell."
        )

    elif rating == "Reduce":

        decision = "REDUCE"

        reasons.append(
            "Company fundamentals are rated Reduce."
        )

    elif rating == "Hold":

        decision = "HOLD"

        reasons.append(
            "Company fundamentals are rated Hold."
        )

    elif rating in ["Buy", "Strong Buy"]:

        if weight < 15:

            decision = "ADD"

            reasons.append(
                f"Company fundamentals are rated {rating} "
                f"and portfolio weight is only "
                f"{weight:.1f}%."
            )

        else:

            decision = "HOLD"

            reasons.append(
                f"Company fundamentals are rated {rating}, "
                f"but portfolio weight is already "
                f"{weight:.1f}%."
            )

    else:

        decision = "WATCH"

        reasons.append(
            "Company fundamental rating is unavailable."
        )

    # ------------------------------------------------------
    # 2. Valuation
    # ------------------------------------------------------

    reasons.append(
        f"Valuation assessment is {valuation}."
    )

    if valuation in [
        "Expensive",
        "Overvalued",
    ]:

        risks.append(
            "Valuation may limit future return potential."
        )

    # ------------------------------------------------------
    # 3. Existing FCF quality engine
    # ------------------------------------------------------

    fcf_assessment, fcf_risk = (
        _get_fcf_assessment(
            company_analysis
        )
    )

    reasons.append(
        fcf_assessment
    )

    if fcf_risk:

        risks.append(
            fcf_risk
        )

    # ------------------------------------------------------
    # 4. Existing DCF engine
    # ------------------------------------------------------

    dcf_assessment, dcf_risk = (
        _get_dcf_assessment(
            company_analysis
        )
    )

    reasons.append(
        dcf_assessment
    )

    if dcf_risk:

        risks.append(
            dcf_risk
        )

    # ------------------------------------------------------
    # 5. Portfolio concentration
    # ------------------------------------------------------

    if weight >= 20:

        risks.append(
            f"Portfolio weight is high at "
            f"{weight:.1f}%."
        )

        # A high existing position overrides
        # an ADD recommendation.

        if decision == "ADD":

            decision = "HOLD"

            reasons.append(
                "ADD is overridden because portfolio "
                "exposure is already very high."
            )

    elif weight >= 15:

        risks.append(
            f"Portfolio weight is already significant "
            f"at {weight:.1f}%."
        )

    # ------------------------------------------------------
    # 6. Overall portfolio risk
    # ------------------------------------------------------

    if portfolio_risk in [
        "🟡 Medium",
        "🔴 High",
    ]:

        risks.append(
            f"Overall portfolio risk is "
            f"{portfolio_risk}."
        )

    # ------------------------------------------------------
    # 7. Company-specific risks
    # ------------------------------------------------------

    for risk in company_analysis.risks:

        if risk and risk not in risks:

            risks.append(
                risk
            )

    # ------------------------------------------------------
    # 8. Confidence
    # ------------------------------------------------------

    if not confidence:

        confidence = "Low"

    # ------------------------------------------------------
    # Final decision
    # ------------------------------------------------------

    return InvestmentDecision(

        company=company,

        decision=decision,

        fundamental_rating=rating,

        valuation_view=valuation,

        portfolio_weight=weight,

        portfolio_risk=portfolio_risk,

        confidence=confidence,

        reasons=reasons,

        risks=risks,
    )