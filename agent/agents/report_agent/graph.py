from langgraph.graph import StateGraph, END
from agents.report_agent.state import ReportAgentState
from agents.report_agent.nodes import (
    gather_node,
    draft_node,
    format_node,
    save_node,
)


def build_report_agent():
    graph = StateGraph(ReportAgentState)

    graph.add_node("gather_node", gather_node)
    graph.add_node("draft_node", draft_node)
    graph.add_node("format_node", format_node)
    graph.add_node("save_node", save_node)

    graph.set_entry_point("gather_node")

    graph.add_edge("gather_node", "draft_node")
    graph.add_edge("draft_node", "format_node")
    graph.add_edge("format_node", "save_node")
    graph.add_edge("save_node", END)

    return graph.compile()
