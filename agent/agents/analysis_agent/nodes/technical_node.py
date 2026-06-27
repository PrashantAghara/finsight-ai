import numpy as np
import pandas as pd
from agents.analysis_agent.state import AnalysisAgentState


def technical_node(state: AnalysisAgentState) -> dict:
    symbol = state["symbol"]
    price_history = state.get("price_history", [])
    current_price = state.get("current_price")
    high_52w = state.get("high_52w")
    low_52w = state.get("low_52w")
    errors = state.get("errors", [])

    print(f"📐 Calculating technical indicators for {symbol}...")

    if not price_history or len(price_history) < 20:
        error_msg = f"Insufficient price history for {symbol}"
        print(f"❌ {error_msg}")
        return {"errors": errors + [error_msg]}

    df = pd.DataFrame(price_history)
    closes = df["close"].astype(float)

    sma_20 = round(closes.tail(20).mean(), 2)
    sma_50 = round(closes.tail(50).mean(), 2) if len(closes) >= 50 else None
    sma_200 = round(closes.tail(200).mean(), 2) if len(closes) >= 200 else None

    delta = closes.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.tail(14).mean()
    avg_loss = loss.tail(14).mean()
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = round(100 - (100 / (1 + rs)), 2)

    ema_12 = closes.ewm(span=12, adjust=False).mean()
    ema_26 = closes.ewm(span=26, adjust=False).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd = round(macd_line.iloc[-1], 4)
    macd_signal = round(signal_line.iloc[-1], 4)

    daily_returns = closes.pct_change().dropna()
    volatility = round(daily_returns.std() * np.sqrt(252) * 100, 2)

    price_vs_52w_high = (
        round(((current_price - high_52w) / high_52w) * 100, 2) if high_52w else None
    )
    price_vs_52w_low = (
        round(((current_price - low_52w) / low_52w) * 100, 2) if low_52w else None
    )

    golden_cross = bool(sma_20 > sma_50) if sma_50 else None
    death_cross = bool(sma_20 < sma_50) if sma_50 else None

    print(f"✅ technical_node → {symbol}")
    print(f"   SMA20:  ${sma_20} | SMA50: ${sma_50} | SMA200: ${sma_200}")
    print(f"   RSI:    {rsi}")
    print(f"   MACD:   {macd} | Signal: {macd_signal}")
    print(f"   Volatility: {volatility}%")
    print(f"   vs 52w High: {price_vs_52w_high}% | vs 52w Low: +{price_vs_52w_low}%")
    print(f"   Golden Cross: {golden_cross} | Death Cross: {death_cross}")

    return {
        "sma_20": sma_20,
        "sma_50": sma_50,
        "sma_200": sma_200,
        "rsi": rsi,
        "macd": macd,
        "macd_signal": macd_signal,
        "volatility": volatility,
        "price_vs_52w_high": price_vs_52w_high,
        "price_vs_52w_low": price_vs_52w_low,
        "golden_cross": golden_cross,
        "death_cross": death_cross,
        "errors": errors,
    }
