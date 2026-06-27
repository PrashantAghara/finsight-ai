from supervisor.state import SupervisorState
from agents.data_agent import build_data_agent

data_agent = build_data_agent()


def run_data_agent_node(state: SupervisorState) -> dict:
    symbol = state["symbol"]
    errors = state.get("errors", [])

    print(f"\n{'─' * 50}")
    print(f"🤖 Supervisor → Running Data Agent for {symbol}")
    print(f"{'─' * 50}")

    try:
        result = data_agent.invoke(
            {
                "symbol": symbol,
                "period": "1y",
                "retry_count": 0,
                "errors": [],
            }
        )

        print(
            f"✅ Data Agent complete → ${result.get('current_price')} | ready: {result.get('data_ready')}"
        )

        return {
            "data_output": result,
            "errors": errors + result.get("errors", []),
        }

    except Exception as e:
        error = f"run_data_agent_node error: {str(e)}"
        print(f"❌ {error}")
        return {"data_output": None, "errors": errors + [error]}
