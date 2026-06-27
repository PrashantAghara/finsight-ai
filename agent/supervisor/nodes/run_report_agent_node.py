from supervisor.state import SupervisorState
from agents.report_agent import build_report_agent

report_agent = build_report_agent()


def run_report_agent_node(state: SupervisorState) -> dict:
    symbol = state["symbol"]
    data_output = state.get("data_output", {})
    analysis_output = state.get("analysis_output", {})
    rag_output = state.get("rag_output", {})
    errors = state.get("errors", [])

    print(f"\n{'─' * 50}")
    print(f"🤖 Supervisor → Running Report Agent for {symbol}")
    print(f"{'─' * 50}")

    rag_context = None
    if rag_output and rag_output.get("retrieved_docs"):
        rag_context = "\n\n".join(rag_output["retrieved_docs"][:3])

    try:
        result = report_agent.invoke(
            {
                "symbol": symbol,
                "current_price": data_output.get("current_price"),
                "price_change_pct": data_output.get("price_change_pct"),
                "market_cap": data_output.get("market_cap"),
                "pe_ratio": data_output.get("pe_ratio"),
                "eps": data_output.get("eps"),
                "revenue": data_output.get("revenue"),
                "profit_margin": data_output.get("profit_margin"),
                "beta": data_output.get("beta"),
                "sector": data_output.get("sector"),
                "industry": data_output.get("industry"),
                "data_summary": data_output.get("summary"),
                "sma_20": analysis_output.get("sma_20"),
                "sma_50": analysis_output.get("sma_50"),
                "rsi": analysis_output.get("rsi"),
                "macd": analysis_output.get("macd"),
                "volatility": analysis_output.get("volatility"),
                "golden_cross": analysis_output.get("golden_cross"),
                "pe_signal": analysis_output.get("pe_signal"),
                "margin_signal": analysis_output.get("margin_signal"),
                "momentum_signal": analysis_output.get("momentum_signal"),
                "risk_score": analysis_output.get("risk_score"),
                "risk_label": analysis_output.get("risk_label"),
                "recommendation": analysis_output.get("recommendation"),
                "reasoning": analysis_output.get("reasoning"),
                "rag_context": rag_context,
                "errors": [],
            }
        )

        print(f"✅ Report Agent complete → {result.get('report_id')}")

        return {
            "report_output": result,
            "report_id": result.get("report_id"),
            "errors": errors + result.get("errors", []),
        }

    except Exception as e:
        error = f"run_report_agent_node error: {str(e)}"
        print(f"❌ {error}")
        return {"report_output": None, "errors": errors + [error]}
