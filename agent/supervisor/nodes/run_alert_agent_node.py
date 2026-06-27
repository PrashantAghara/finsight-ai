from supervisor.state import SupervisorState
from agents.alert_agent import build_alert_agent

alert_agent = build_alert_agent()


def run_alert_agent_node(state: SupervisorState) -> dict:
    symbol = state["symbol"]
    user_id = state.get("user_id")
    data_output = state.get("data_output", {})
    analysis_output = state.get("analysis_output", {})
    errors = state.get("errors", [])

    print(f"\n{'─' * 50}")
    print(f"🤖 Supervisor → Running Alert Agent for {symbol}")
    print(f"{'─' * 50}")

    try:
        result = alert_agent.invoke(
            {
                "symbol": symbol,
                "user_id": user_id,
                "current_price": data_output.get("current_price"),
                "rsi": analysis_output.get("rsi"),
                "price_change_pct": data_output.get("price_change_pct"),
                "risk_score": analysis_output.get("risk_score"),
                "errors": [],
            }
        )

        triggered = result.get("triggered_alerts", [])
        print(f"✅ Alert Agent complete → {len(triggered)} alerts triggered")

        return {
            "alert_output": result,
            "triggered_alerts": triggered,
            "errors": errors + result.get("errors", []),
        }

    except Exception as e:
        error = f"run_alert_agent_node error: {str(e)}"
        print(f"❌ {error}")
        return {"alert_output": None, "errors": errors + [error]}
