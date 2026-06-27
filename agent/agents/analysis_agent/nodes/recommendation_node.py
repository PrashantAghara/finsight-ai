import json
import re
from clients.clients import groq_client
from agents.analysis_agent.state import AnalysisAgentState

RECOMMENDATION_PROMPT = """
You are a senior financial analyst. Based on the following analysis data,
provide a stock recommendation and detailed reasoning.

You MUST respond ONLY with valid JSON in this exact format:
{{
    "recommendation": "buy",
    "reasoning": "3-4 sentence explanation"
}}

Valid recommendation values: "strong_buy", "buy", "hold", "sell", "strong_sell"

Rules:
- Base recommendation strictly on the data provided
- No personal opinions — only data-driven conclusions
- reasoning must reference specific metrics from the data
- Never recommend based on company name or brand

Analysis Data:
{data}
"""


def recommendation_node(state: AnalysisAgentState) -> dict:
    symbol = state["symbol"]
    errors = state.get("errors", [])

    print(f"🤖 Generating recommendation for {symbol}...")

    analysis_data = f"""
        Symbol:           {symbol}
        Current Price:    ${state.get("current_price")}
        Price Change 1Y:  {state.get("price_change_pct")}%
        52w High:         ${state.get("high_52w")}
        52w Low:          ${state.get("low_52w")}
        vs 52w High:      {state.get("price_vs_52w_high")}%
        vs 52w Low:       +{state.get("price_vs_52w_low")}%

        Technical:
        - SMA 20:         ${state.get("sma_20")}
        - SMA 50:         ${state.get("sma_50")}
        - SMA 200:        ${state.get("sma_200")}
        - RSI:            {state.get("rsi")}
        - MACD:           {state.get("macd")}
        - MACD Signal:    {state.get("macd_signal")}
        - Volatility:     {state.get("volatility")}%
        - Golden Cross:   {state.get("golden_cross")}
        - Death Cross:    {state.get("death_cross")}

        Valuation:
        - P/E Ratio:      {state.get("pe_ratio")}
        - P/E Signal:     {state.get("pe_signal")}
        - EPS:            {state.get("eps")}
        - Profit Margin:  {state.get("profit_margin")}
        - Margin Signal:  {state.get("margin_signal")}
        - Momentum:       {state.get("momentum_signal")}

        Risk:
        - Beta:           {state.get("beta")}
        - Risk Score:     {state.get("risk_score")}/10
        - Risk Label:     {state.get("risk_label")}
        - Sector:         {state.get("sector")}

        Data Summary:
        {state.get("data_summary")}
    """

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": RECOMMENDATION_PROMPT.format(data=analysis_data),
                }
            ],
            temperature=0.1,
        )

        raw = response.choices[0].message.content.strip()
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            result = json.loads(match.group()) if match else {}
        recommendation = result.get("recommendation", "hold")
        reasoning = result.get("reasoning", "")

        print(f"✅ recommendation_node → {symbol}")
        print(f"   Recommendation: {recommendation.upper()}")
        print(f"   Reasoning: {reasoning}")

        return {
            "recommendation": recommendation,
            "reasoning": reasoning,
            "errors": errors,
        }

    except Exception as e:
        error_msg = f"recommendation_node error: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "recommendation": "hold",
            "reasoning": "Unable to generate recommendation",
            "errors": errors + [error_msg],
        }
