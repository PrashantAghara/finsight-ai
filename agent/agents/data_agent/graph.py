from langgraph.graph import StateGraph, END
from agents.data_agent.state import DataAgentState
from agents.data_agent.nodes import (
    fetch_price_node,
    fetch_fundamentals_node,
    validate_node,
    summary_node,
)

MAX_RETRIES = 2


def should_retry(state: DataAgentState) -> str:
    if not state.get("data_ready") and state.get("retry_count", 0) < MAX_RETRIES:
        return "fetch_price_node"
    return "summary_node"


def build_data_agent():
    graph = StateGraph(DataAgentState)

    graph.add_node("fetch_price_node", fetch_price_node)
    graph.add_node("fetch_fundamentals_node", fetch_fundamentals_node)
    graph.add_node("validate_node", validate_node)
    graph.add_node("summary_node", summary_node)

    graph.set_entry_point("fetch_price_node")

    graph.add_edge("fetch_price_node", "fetch_fundamentals_node")
    graph.add_edge("fetch_fundamentals_node", "validate_node")

    graph.add_conditional_edges(
        "validate_node",
        should_retry,
        {
            "fetch_price_node": "fetch_price_node",
            "summary_node": "summary_node",
        },
    )

    graph.add_edge("summary_node", END)

    return graph.compile()
