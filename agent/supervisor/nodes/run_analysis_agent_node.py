from supervisor.state import SupervisorState
from agents.analysis_agent import build_analysis_agent

analysis_agent = build_analysis_agent()


def run_analysis_agent_node(state: SupervisorState) -> dict:
    symbol = state["symbol"]
    data_output = state.get("data_output", {})
    errors = state.get("errors", [])

    print(f"\n{'─' * 50}")
    print(f"🤖 Supervisor → Running Analysis Agent for {symbol}")
    print(f"{'─' * 50}")

    if not data_output:
        error = "No data_output available for analysis"
        print(f"❌ {error}")
        return {"analysis_output": None, "errors": errors + [error]}

    try:
        result = analysis_agent.invoke(
            {
                "symbol": data_output.get("symbol", symbol),
                "current_price": data_output.get("current_price"),
                "high_52w": data_output.get("high_52w"),
                "low_52w": data_output.get("low_52w"),
                "price_change_pct": data_output.get("price_change_pct"),
                "price_history": data_output.get("price_history"),
                "pe_ratio": data_output.get("pe_ratio"),
                "eps": data_output.get("eps"),
                "market_cap": data_output.get("market_cap"),
                "revenue": data_output.get("revenue"),
                "profit_margin": data_output.get("profit_margin"),
                "beta": data_output.get("beta"),
                "dividend_yield": data_output.get("dividend_yield"),
                "sector": data_output.get("sector"),
                "data_summary": data_output.get("summary"),
                "errors": [],
            }
        )

        print(
            f"✅ Analysis Agent complete → {result.get('recommendation', '').upper()} | risk: {result.get('risk_label')}"
        )

        return {
            "analysis_output": result,
            "errors": errors + result.get("errors", []),
        }

    except Exception as e:
        error = f"run_analysis_agent_node error: {str(e)}"
        print(f"❌ {error}")
        return {"analysis_output": None, "errors": errors + [error]}
