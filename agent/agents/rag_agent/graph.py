from langgraph.graph import StateGraph, END
from agents.rag_agent.state import RAGAgentState
from agents.rag_agent.nodes import (
    route_node,
    ingest_node,
    embed_node,
    retrieve_node,
    answer_node,
)


def route_by_mode(state: RAGAgentState) -> str:
    return "ingest_node" if state.get("mode") == "ingest" else "retrieve_node"


def build_rag_agent():
    graph = StateGraph(RAGAgentState)

    graph.add_node("route_node", route_node)
    graph.add_node("ingest_node", ingest_node)
    graph.add_node("embed_node", embed_node)
    graph.add_node("retrieve_node", retrieve_node)
    graph.add_node("answer_node", answer_node)

    graph.set_entry_point("route_node")

    graph.add_conditional_edges(
        "route_node",
        route_by_mode,
        {
            "ingest_node": "ingest_node",
            "retrieve_node": "retrieve_node",
        },
    )

    graph.add_edge("ingest_node", "embed_node")
    graph.add_edge("embed_node", END)
    graph.add_edge("retrieve_node", "answer_node")
    graph.add_edge("answer_node", END)

    return graph.compile()
