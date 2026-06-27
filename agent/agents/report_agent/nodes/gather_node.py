from agents.report_agent.state import ReportAgentState


def gather_node(state: ReportAgentState) -> dict:
    symbol = state["symbol"]
    print(f"📦 Gathering all inputs for {symbol} report...")

    missing = []
    if not state.get("data_summary"):
        missing.append("data_summary")
    if not state.get("recommendation"):
        missing.append("recommendation")
    if not state.get("risk_score"):
        missing.append("risk_score")

    if missing:
        print(f"⚠️  Missing inputs: {missing} — report will be partial")
    else:
        print(f"✅ gather_node → All inputs present for {symbol}")

    return {}
