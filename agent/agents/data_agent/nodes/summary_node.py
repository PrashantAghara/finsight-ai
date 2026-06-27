from clients.clients import groq_client
from agents.data_agent.state import DataAgentState


def summary_node(state: DataAgentState) -> dict:
    symbol = state["symbol"]
    errors = state.get("errors", [])

    print(f"📝 Generating data summary for {symbol}...")
    price_section = (
        f"""
        PRICE DATA ({symbol}):
        - Current Price:    ${state.get("current_price", "N/A")}
        - 52-Week High:     ${state.get("high_52w", "N/A")}
        - 52-Week Low:      ${state.get("low_52w", "N/A")}
        - Price Change:     {state.get("price_change_pct", "N/A")}% over {state.get("period", "1y")}
        - Volume:           {state.get("volume", "N/A"):,} (Avg: {state.get("avg_volume", "N/A"):,})
        """
        if state.get("price_fetch_success")
        else "PRICE DATA: Unavailable"
    )

    fundamentals_section = (
        f"""
        FUNDAMENTALS ({symbol}):
        - Market Cap:       ${state.get("market_cap", 0):,.0f}
        - P/E Ratio:        {state.get("pe_ratio", "N/A")}
        - EPS:              {state.get("eps", "N/A")}
        - Revenue (TTM):    ${state.get("revenue", 0):,.0f}
        - Profit Margin:    {state.get("profit_margin", "N/A")}
        - Dividend Yield:   {state.get("dividend_yield", "N/A")}
        - Beta:             {state.get("beta", "N/A")}
        - Sector:           {state.get("sector", "N/A")}
        - Industry:         {state.get("industry", "N/A")}
        """
        if state.get("fundamentals_fetch_success")
        else "FUNDAMENTALS: Unavailable"
    )

    prompt = f"""
    You are a financial data analyst. Based on the following raw data,
    write a concise 3-4 sentence factual summary of {symbol}'s current
    financial position. No recommendations — just facts.

    {price_section}
    {fundamentals_section}
    """

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        summary = response.choices[0].message.content.strip()
        print("✅ summary_node → Summary generated")
        print("\n── Summary ──────────────────────────────")
        print(summary)

        return {"summary": summary, "errors": errors}

    except Exception as e:
        error_msg = f"summary_node error: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "summary": f"Summary unavailable for {symbol}",
            "errors": errors + [error_msg],
        }
