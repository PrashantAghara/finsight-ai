from agents.analysis_agent.state import AnalysisAgentState


def valuation_node(state: AnalysisAgentState) -> dict:
    symbol = state["symbol"]
    pe_ratio = state.get("pe_ratio")
    profit_margin = state.get("profit_margin")
    price_change = state.get("price_change_pct")
    rsi = state.get("rsi")
    macd = state.get("macd")
    macd_signal = state.get("macd_signal")
    errors = state.get("errors", [])

    print(f"💰 Calculating valuation signals for {symbol}...")

    if pe_ratio is None:
        pe_signal = "unknown"
    elif pe_ratio < 15:
        pe_signal = "undervalued"
    elif pe_ratio < 25:
        pe_signal = "fair"
    elif pe_ratio < 40:
        pe_signal = "slightly_overvalued"
    else:
        pe_signal = "overvalued"

    if profit_margin is None:
        margin_signal = "unknown"
    elif profit_margin >= 0.30:
        margin_signal = "strong"
    elif profit_margin >= 0.15:
        margin_signal = "moderate"
    elif profit_margin >= 0.05:
        margin_signal = "weak"
    else:
        margin_signal = "negative"

    bullish_signals = 0
    bearish_signals = 0

    if price_change and price_change > 10:
        bullish_signals += 1
    elif price_change and price_change < -10:
        bearish_signals += 1

    if rsi:
        if rsi < 30:
            bullish_signals += 1
        elif rsi > 70:
            bearish_signals += 1

    if macd and macd_signal:
        if macd > macd_signal:
            bullish_signals += 1
        else:
            bearish_signals += 1

    if bullish_signals > bearish_signals:
        momentum_signal = "bullish"
    elif bearish_signals > bullish_signals:
        momentum_signal = "bearish"
    else:
        momentum_signal = "neutral"

    print(f"✅ valuation_node → {symbol}")
    print(f"   P/E Signal:      {pe_signal} (P/E: {pe_ratio})")
    print(f"   Margin Signal:   {margin_signal} (margin: {profit_margin})")
    print(f"   Momentum Signal: {momentum_signal}")
    print(f"   Bullish: {bullish_signals} | Bearish: {bearish_signals}")

    return {
        "pe_signal": pe_signal,
        "margin_signal": margin_signal,
        "momentum_signal": momentum_signal,
        "errors": errors,
    }
