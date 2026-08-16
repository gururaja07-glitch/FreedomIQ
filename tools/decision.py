from models.decision import InvestmentDecision


def make_investment_decision(
    company_analysis,
    portfolio_row,
    portfolio_risk,
):
    """
    Combine company research with the current portfolio position.
    """

    rating = company_analysis.score.rating
    valuation = company_analysis.valuation.valuation
    confidence = company_analysis.confidence

    weight = float(portfolio_row["Weight %"])
    company = portfolio_row["Stock"]

    reasons = []
    risks = []

    # Company rating
    if rating == "Sell":
        decision = "SELL"
        reasons.append("Company rating is Sell.")

    elif rating == "Reduce":
        decision = "REDUCE"
        reasons.append("Company rating is Reduce.")

    elif rating == "Hold":
        decision = "HOLD"
        reasons.append("Company rating is Hold.")

    elif rating in ["Buy", "Strong Buy"]:

        if weight < 15:
            decision = "ADD"
            reasons.append(
                f"Company rating is {rating} and portfolio weight is {weight:.1f}%."
            )
        else:
            decision = "HOLD"
            reasons.append(
                f"Company rating is {rating}, but portfolio weight is already "
                f"{weight:.1f}%."
            )

    else:
        decision = "WATCH"
        reasons.append("Company rating is unavailable.")

    # Valuation
    reasons.append(
        f"Valuation is {valuation}."
    )

    # Portfolio concentration
    if weight >= 20:
        risks.append(
            f"Portfolio weight is high at {weight:.1f}%."
        )

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
    if portfolio_risk in ["🟡 Medium", "🔴 High"]:
     risks.append(
       f"Overall portfolio risk is {portfolio_risk}."
        )