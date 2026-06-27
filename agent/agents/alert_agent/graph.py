from langgraph.graph import StateGraph, END
from agents.alert_agent.state import AlertAgentState
from agents.alert_agent.nodes import (
    load_alerts_node,
    check_alerts_node,
    trigger_node,
)


def build_alert_agent():
    graph = StateGraph(AlertAgentState)

    graph.add_node("load_alerts_node", load_alerts_node)
    graph.add_node("check_alerts_node", check_alerts_node)
    graph.add_node("trigger_node", trigger_node)

    graph.set_entry_point("load_alerts_node")

    graph.add_edge("load_alerts_node", "check_alerts_node")
    graph.add_edge("check_alerts_node", "trigger_node")
    graph.add_edge("trigger_node", END)

    return graph.compile()
