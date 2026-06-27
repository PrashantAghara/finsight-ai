import yfinance as yf
from agents.data_agent.state import DataAgentState


def fetch_price_node(state: DataAgentState) -> dict:
    symbol = state["symbol"]
    period = state["period"]
    errors = state["errors"]

    print(f"📈 Fetching price data for {symbol}...")

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        current_price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
        )
        high_52w = info.get("fiftyTwoWeekHigh")
        low_52w = info.get("fiftyTwoWeekLow")
        volume = info.get("volume") or info.get("regularMarketVolume")
        avg_volume = info.get("averageVolume")
        open_price = info.get("open") or info.get("regularMarketOpen")
        hist = ticker.history(period=period)
        if hist.empty:
            raise ValueError(f"No price history found for {symbol}")

        price_history = [
            {
                "date": str(idx.date()),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"]),
            }
            for idx, row in hist.iterrows()
        ]
        if len(price_history) >= 2:
            first_close = price_history[0]["close"]
            last_close = price_history[-1]["close"]
            price_change_pct = round(
                ((last_close - first_close) / first_close) * 100, 2
            )
        else:
            price_change_pct = 0.0

        print(f"✅ fetch_price_node → {symbol} @ ${current_price}")
        print(f"   52w High: ${high_52w} | 52w Low: ${low_52w}")
        print(f"   Price change ({period}): {price_change_pct}%")
        print(f"   History records: {len(price_history)}")

        return {
            "current_price": current_price,
            "open_price": open_price,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "volume": volume,
            "avg_volume": avg_volume,
            "price_history": price_history,
            "price_change_pct": price_change_pct,
            "price_fetch_success": True,
            "errors": errors,
        }
    except Exception as e:
        error_msg = f"fetch_price_node error: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "price_fetch_success": False,
            "errors": errors + [error_msg],
        }
