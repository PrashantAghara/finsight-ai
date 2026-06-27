from agents.report_agent.state import ReportAgentState
from clients.clients import groq_client

REPORT_SYSTEM_PROMPT = """
You are a senior equity research analyst at a top investment bank.
Generate a professional investment research report section.
Be precise, data-driven, and use financial terminology correctly.
Never speculate beyond the data provided.
"""


def draft_section(prompt: str) -> str:
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": REPORT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


def draft_node(state: ReportAgentState) -> dict:
    symbol = state["symbol"]
    errors = state.get("errors", [])

    print(f"✍️  Drafting report sections for {symbol}...")

    try:
        print("   Drafting executive summary...")
        exec_prompt = f"""
        Write a 3-4 sentence executive summary for {symbol}.

        Data:
        - Current Price: ${state.get("current_price")}
        - 1Y Price Change: {state.get("price_change_pct")}%
        - Market Cap: ${state.get("market_cap", 0):,.0f}
        - Sector: {state.get("sector")}
        - Recommendation: {state.get("recommendation", "").upper()}
        - Risk Label: {state.get("risk_label")}

        Data Summary: {state.get("data_summary")}
        """
        executive_summary = draft_section(exec_prompt)

        print("   Drafting financial analysis...")
        fin_prompt = f"""
        Write a financial analysis paragraph for {symbol}.

        Metrics:
        - Revenue: ${state.get("revenue", 0):,.0f}
        - EPS: {state.get("eps")}
        - P/E Ratio: {state.get("pe_ratio")} ({state.get("pe_signal")})
        - Profit Margin: {state.get("profit_margin")} ({state.get("margin_signal")})
        - Dividend Yield: {state.get("beta")}
        - Beta: {state.get("beta")}

        RAG Context (from annual report):
        {state.get("rag_context", "No document context available.")}

        Focus on valuation, profitability, and growth metrics.
        """
        financial_analysis = draft_section(fin_prompt)

        print("   Drafting technical analysis...")
        tech_prompt = f"""
        Write a technical analysis paragraph for {symbol}.

        Indicators:
        - SMA 20: ${state.get("sma_20")} | SMA 50: ${state.get("sma_50")}
        - RSI: {state.get("rsi")}
        - MACD: {state.get("macd")} | Signal: N/A
        - Volatility: {state.get("volatility")}%
        - Golden Cross: {state.get("golden_cross")}
        - Momentum: {state.get("momentum_signal")}

        Focus on trend direction, momentum, and key support/resistance levels.
        """
        technical_analysis = draft_section(tech_prompt)

        print("   Drafting risk assessment...")
        risk_prompt = f"""
        Write a risk assessment paragraph for {symbol}.

        Risk Data:
        - Risk Score: {state.get("risk_score")}/10
        - Risk Label: {state.get("risk_label")}
        - Beta: {state.get("beta")}
        - Volatility: {state.get("volatility")}%
        - P/E Signal: {state.get("pe_signal")}

        RAG Context (risk factors from documents):
        {state.get("rag_context", "No document context available.")}

        Focus on key risk factors and their potential impact.
        """
        risk_assessment = draft_section(risk_prompt)

        print("   Drafting recommendation section...")
        rec_prompt = f"""
        Write a recommendation section for {symbol}.

        Recommendation: {state.get("recommendation", "").upper()}
        Reasoning: {state.get("reasoning")}
        Risk Label: {state.get("risk_label")}

        Write 2-3 sentences expanding on the recommendation with specific
        price targets or conditions to watch. Be direct and actionable.
        """
        recommendation_section = draft_section(rec_prompt)

        print(f"✅ draft_node → All sections drafted for {symbol}")
        return {
            "executive_summary": executive_summary,
            "financial_analysis": financial_analysis,
            "technical_analysis": technical_analysis,
            "risk_assessment": risk_assessment,
            "recommendation_section": recommendation_section,
            "errors": errors,
        }

    except Exception as e:
        error = f"draft_node error: {str(e)}"
        print(f"❌ {error}")
        return {"errors": errors + [error]}
