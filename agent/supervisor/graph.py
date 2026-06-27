from langgraph.graph import StateGraph, END
from supervisor.state import SupervisorState
from supervisor.nodes import (
    supervisor_route_node,
    run_data_agent_node,
    run_analysis_agent_node,
    run_rag_agent_node,
    run_report_agent_node,
    run_alert_agent_node,
    final_response_node,
)


def route_by_mode(state: SupervisorState) -> str:
    mode = state["mode"]
    if mode in ("analyse", "report"):
        return "run_data_agent_node"
    elif mode in ("chat", "ingest"):
        return "run_rag_agent_node"
    return "final_response_node"


def after_data_agent(state: SupervisorState) -> str:
    return "run_analysis_agent_node"


def after_analysis_agent(state: SupervisorState) -> str:
    mode = state["mode"]
    if mode == "report":
        return "run_rag_agent_node"
    return "run_alert_agent_node"


def after_rag_agent(state: SupervisorState) -> str:
    mode = state["mode"]
    if mode == "report":
        return "run_report_agent_node"
    return "final_response_node"


def build_supervisor():
    graph = StateGraph(SupervisorState)

    graph.add_node("supervisor_route_node", supervisor_route_node)
    graph.add_node("run_data_agent_node", run_data_agent_node)
    graph.add_node("run_analysis_agent_node", run_analysis_agent_node)
    graph.add_node("run_rag_agent_node", run_rag_agent_node)
    graph.add_node("run_report_agent_node", run_report_agent_node)
    graph.add_node("run_alert_agent_node", run_alert_agent_node)
    graph.add_node("final_response_node", final_response_node)

    graph.set_entry_point("supervisor_route_node")

    graph.add_conditional_edges(
        "supervisor_route_node",
        route_by_mode,
        {
            "run_data_agent_node": "run_data_agent_node",
            "run_rag_agent_node": "run_rag_agent_node",
            "final_response_node": "final_response_node",
        },
    )

    graph.add_conditional_edges(
        "run_data_agent_node",
        after_data_agent,
        {
            "run_analysis_agent_node": "run_analysis_agent_node",
        },
    )

    graph.add_conditional_edges(
        "run_analysis_agent_node",
        after_analysis_agent,
        {
            "run_rag_agent_node": "run_rag_agent_node",
            "run_alert_agent_node": "run_alert_agent_node",
        },
    )

    graph.add_conditional_edges(
        "run_rag_agent_node",
        after_rag_agent,
        {
            "run_report_agent_node": "run_report_agent_node",
            "final_response_node": "final_response_node",
        },
    )

    graph.add_edge("run_report_agent_node", "run_alert_agent_node")
    graph.add_edge("run_alert_agent_node", "final_response_node")
    graph.add_edge("final_response_node", END)

    return graph.compile()
