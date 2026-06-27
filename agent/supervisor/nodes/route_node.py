from supervisor.state import SupervisorState


def supervisor_route_node(state: SupervisorState) -> dict:
    symbol = state["symbol"]
    mode = state["mode"]
    print(f"🎯 Supervisor routing → {symbol} | mode: {mode}")
    return {}
