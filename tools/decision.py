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

    if getattr(
        dcf,
        "status",
        "Unavailable",
    ) != "Available":

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


def _build_reasoning_summary(
    rating,
    valuation,
    fcf_quality,
    dcf_verdict,
    weight,
    confidence,
):
    """
    Synthesize the major investment signals into a
    concise reasoning summary.
    """

    positive_signals = []
    caution_signals = []
    negative_signals = []

    # ------------------------------------------------------
    # Fundamentals
    # ------------------------------------------------------

    if rating in ["Buy", "Strong Buy"]:

        positive_signals.append(
            f"fundamentals are rated {rating}"
        )

    elif rating == "Hold":

        caution_signals.append(
            "fundamentals are rated Hold"
        )

    elif rating in ["Reduce", "Sell"]:

        negative_signals.append(
            f"fundamentals are rated {rating}"
        )

    # ------------------------------------------------------
    # Valuation
    # ------------------------------------------------------

    if valuation == "Undervalued":

        positive_signals.append(
            "valuation is undervalued"
        )

    elif valuation == "Fairly Valued":

        caution_signals.append(
            "valuation is fairly valued"
        )

    elif valuation in ["Expensive", "Overvalued"]:

        negative_signals.append(
            f"valuation is {valuation.lower()}"
        )

    # ------------------------------------------------------
    # FCF
    # ------------------------------------------------------

    if fcf_quality == "High":

        positive_signals.append(
            "FCF quality is strong"
        )

    elif fcf_quality in ["Moderate", "Low"]:

        caution_signals.append(
            f"FCF quality is {fcf_quality.lower()}"
        )

    # ------------------------------------------------------
    # DCF
    # ------------------------------------------------------

    if dcf_verdict in ["Strong Buy", "Buy"]:

        positive_signals.append(
            f"DCF supports {dcf_verdict}"
        )

    elif dcf_verdict == "Hold":

        caution_signals.append(
            "DCF supports Hold"
        )

    elif dcf_verdict in ["Reduce", "Sell"]:

        negative_signals.append(
            f"DCF supports {dcf_verdict}"
        )

    # ------------------------------------------------------
    # Portfolio exposure
    # ------------------------------------------------------

    if weight >= 20:

        negative_signals.append(
            f"portfolio exposure is already high at "
            f"{weight:.1f}%"
        )

    elif weight >= 15:

        caution_signals.append(
            f"portfolio exposure is significant at "
            f"{weight:.1f}%"
        )

    elif weight < 5:

        positive_signals.append(
            f"portfolio exposure is low at "
            f"{weight:.1f}%"
        )

    # ------------------------------------------------------
    # Overall classification
    # ------------------------------------------------------

    if negative_signals:

        if positive_signals:

            return (
                "The evidence is mixed but leans cautious: "
                + ", ".join(positive_signals)
                + ". However, "
                + ", ".join(negative_signals)
                + ". "
                + f"Confidence is {confidence}."
            )

        return (
            "The balance of evidence is cautious: "
            + ", ".join(negative_signals)
            + ". "
            + (
                "Additional caution comes from "
                + ", ".join(caution_signals)
                + ". "
                if caution_signals
                else ""
            )
            + f"Confidence is {confidence}."
        )

    if positive_signals and caution_signals:

        if len(positive_signals) > len(caution_signals):

            return (
                "The balance of evidence is positive: "
                + ", ".join(positive_signals)
                + ". "
                + "The main caution is "
                + ", ".join(caution_signals)
                + ". "
                + f"Confidence is {confidence}."
            )

        return (
            "The evidence is mixed: "
            + ", ".join(positive_signals)
            + ", while "
            + ", ".join(caution_signals)
            + ". "
            + f"Confidence is {confidence}."
        )

    if positive_signals:

        return (
            "The balance of evidence is positive: "
            + ", ".join(positive_signals)
            + ". "
            + f"Confidence is {confidence}."
        )

    if caution_signals:

        return (
            "The balance of evidence is cautious: "
            + ", ".join(caution_signals)
            + ". "
            + f"Confidence is {confidence}."
        )

    return (
        f"Evidence is limited. Confidence is {confidence}."
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
    - FCF quality
    - DCF valuation
    - Portfolio exposure
    - Portfolio risk
    - Company-specific risks
    - Confidence
    - Evidence synthesis
    """

    rating = company_analysis.score.rating

    valuation = (
        company_analysis.valuation.valuation
    )

    confidence = (
        company_analysis.confidence
        or "Low"
    )

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

    elif rating in [
        "Buy",
        "Strong Buy",
    ]:

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
    # 3. FCF quality
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
    # 4. DCF
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
    # 6. Portfolio risk
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
    # 8. Evidence synthesis
    # ------------------------------------------------------

    dcf_verdict = "Unavailable"

    if company_analysis.dcf is not None:

        dcf_verdict = getattr(
            company_analysis.dcf,
            "verdict",
            "Unavailable",
        )

    fcf_quality = "Unavailable"

    if company_analysis.dcf is not None:

        assumptions = (
            company_analysis.dcf.assumptions
            or {}
        )

        fcf_quality = assumptions.get(
            "fcf_quality",
            "Unavailable",
        )

    reasoning_summary = (
        _build_reasoning_summary(
            rating=rating,
            valuation=valuation,
            fcf_quality=fcf_quality,
            dcf_verdict=dcf_verdict,
            weight=weight,
            confidence=confidence,
        )
    )
    # ------------------------------------------------------
    # Financial data quality
    # ------------------------------------------------------

    financial_data_quality = "Unavailable"

    data_quality = getattr(
        company_analysis.financials,
        "data_quality",
        None,
    )

    if data_quality is not None:

        financial_data_quality = getattr(
            data_quality,
            "overall",
            "Unavailable",
        )

    reasons.insert(
        0,
        reasoning_summary,
    )

    # ------------------------------------------------------
    # Final decision
    # ------------------------------------------------------

    return InvestmentDecision(
        company=company,
        decision=decision,
        fundamental_rating=rating,
        valuation_view=valuation,
        fcf_quality=fcf_quality,
        dcf_verdict=dcf_verdict,
        financial_data_quality=financial_data_quality,
        evidence_summary=reasoning_summary,
        portfolio_weight=weight,
        portfolio_risk=portfolio_risk,
        confidence=confidence,
        reasons=reasons,
        risks=risks,
    )
