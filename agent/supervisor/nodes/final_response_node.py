from supervisor.state import SupervisorState


def final_response_node(state: SupervisorState) -> dict:
    symbol = state["symbol"]
    mode = state["mode"]
    data_output = state.get("data_output", {})
    analysis_output = state.get("analysis_output", {})
    rag_output = state.get("rag_output", {})
    report_output = state.get("report_output", {})
    triggered_alerts = state.get("triggered_alerts", [])

    print(f"\n{'─' * 50}")
    print(f"📤 Supervisor → Building final response for {symbol}")
    print(f"{'─' * 50}")

    if mode == "ingest":
        chunks = state.get("rag_output", {}).get("chunks_stored", 0)
        response = (
            f"✅ Document successfully ingested for {symbol}. "
            f"{chunks} chunks added to knowledge base."
        )

    elif mode == "chat":
        response = rag_output.get("answer", "No answer generated.")

    elif mode == "analyse":
        response = f"""
        ANALYSIS SUMMARY — {symbol}
        {"─" * 40}
        Price:          ${data_output.get("current_price")}
        1Y Change:      {data_output.get("price_change_pct")}%
        RSI:            {analysis_output.get("rsi")}
        Risk:           {analysis_output.get("risk_score")}/10 ({analysis_output.get("risk_label")})
        Recommendation: {analysis_output.get("recommendation", "").upper()}

        {analysis_output.get("reasoning", "")}
        """
        if triggered_alerts:
            response += f"\n🔔 {len(triggered_alerts)} alert(s) triggered:\n"
            for alert in triggered_alerts:
                response += f"  • {alert['alert_type']} — {alert['reason']}\n"

    elif mode == "report":
        response = report_output.get("full_report", "Report generation failed.")
        if triggered_alerts:
            response += (
                f"\n🔔 {len(triggered_alerts)} alert(s) triggered during analysis."
            )

    else:
        response = "Unknown mode."

    print(f"✅ final_response_node → Response built for {symbol} ({mode} mode)")

    return {"final_response": response}
