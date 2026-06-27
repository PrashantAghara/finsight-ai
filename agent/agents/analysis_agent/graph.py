from langgraph.graph import StateGraph, END
from agents.analysis_agent.state import AnalysisAgentState
from agents.analysis_agent.nodes import (
    technical_node,
    valuation_node,
    risk_node,
    recommendation_node,
)


def build_analysis_agent():
    graph = StateGraph(AnalysisAgentState)

    graph.add_node("technical_node", technical_node)
    graph.add_node("valuation_node", valuation_node)
    graph.add_node("risk_node", risk_node)
    graph.add_node("recommendation_node", recommendation_node)

    graph.set_entry_point("technical_node")

    graph.add_edge("technical_node", "valuation_node")
    graph.add_edge("valuation_node", "risk_node")
    graph.add_edge("risk_node", "recommendation_node")
    graph.add_edge("recommendation_node", END)

    return graph.compile()
