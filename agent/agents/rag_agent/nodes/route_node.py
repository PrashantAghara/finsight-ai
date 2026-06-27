from agents.rag_agent.state import RAGAgentState


def route_node(state: RAGAgentState) -> dict:
    mode = state.get("mode")
    symbol = state["symbol"]
    print(f"🔀 route_node → {symbol} | mode: {mode}")
    return {}
