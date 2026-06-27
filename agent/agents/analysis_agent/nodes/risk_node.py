from agents.analysis_agent.state import AnalysisAgentState


def risk_node(state: AnalysisAgentState) -> dict:
    symbol = state["symbol"]
    beta = state.get("beta")
    volatility = state.get("volatility")
    rsi = state.get("rsi")
    pe_signal = state.get("pe_signal")
    price_vs_52w_high = state.get("price_vs_52w_high")
    momentum_signal = state.get("momentum_signal")
    errors = state.get("errors", [])

    print(f"⚠️  Calculating risk score for {symbol}...")

    risk_score = 5.0

    if beta:
        if beta > 1.5:
            risk_score += 1.5
        elif beta > 1.2:
            risk_score += 0.8
        elif beta < 0.8:
            risk_score -= 0.5

    if volatility:
        if volatility > 40:
            risk_score += 1.5
        elif volatility > 25:
            risk_score += 0.8
        elif volatility < 15:
            risk_score -= 0.5

    if rsi:
        if rsi > 75:
            risk_score += 1.0
        elif rsi < 25:
            risk_score += 0.5
        elif 40 <= rsi <= 60:
            risk_score -= 0.5

    if pe_signal == "overvalued":
        risk_score += 1.0
    elif pe_signal == "undervalued":
        risk_score -= 0.5

    if price_vs_52w_high:
        if price_vs_52w_high > -5:
            risk_score += 0.5
        elif price_vs_52w_high < -30:
            risk_score += 1.0

    if momentum_signal == "bearish":
        risk_score += 0.5
    elif momentum_signal == "bullish":
        risk_score -= 0.5

    risk_score = round(max(0.0, min(10.0, risk_score)), 2)

    if risk_score <= 3.5:
        risk_label = "low"
    elif risk_score <= 6.5:
        risk_label = "medium"
    else:
        risk_label = "high"

    print(f"✅ risk_node → {symbol}")
    print(f"   Risk Score: {risk_score}/10")
    print(f"   Risk Label: {risk_label}")

    return {
        "risk_score": risk_score,
        "risk_label": risk_label,
        "errors": errors,
    }
