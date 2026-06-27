from agents.alert_agent.state import AlertAgentState


def check_alerts_node(state: AlertAgentState) -> dict:
    symbol = state["symbol"]
    active_alerts = state.get("active_alerts", [])
    current_price = state.get("current_price")
    rsi = state.get("rsi")
    price_change = state.get("price_change_pct")
    errors = state.get("errors", [])

    print(f"🔍 Checking {len(active_alerts)} alerts for {symbol}...")
    print(f"   Price: ${current_price} | RSI: {rsi} | Change: {price_change}%")

    triggered_alerts = []
    skipped_alerts = []

    for alert in active_alerts:
        alert_type = alert["alert_type"]
        threshold = alert["threshold"]
        triggered = False
        reason = ""

        if alert_type == "price_above" and current_price:
            if current_price > threshold:
                triggered = True
                reason = f"Price ${current_price} > threshold ${threshold}"

        elif alert_type == "price_below" and current_price:
            if current_price < threshold:
                triggered = True
                reason = f"Price ${current_price} < threshold ${threshold}"

        elif alert_type == "rsi_above" and rsi:
            if rsi > threshold:
                triggered = True
                reason = f"RSI {rsi} > threshold {threshold} (overbought)"

        elif alert_type == "rsi_below" and rsi:
            if rsi < threshold:
                triggered = True
                reason = f"RSI {rsi} < threshold {threshold} (oversold)"

        elif alert_type == "change_above" and price_change:
            if price_change > threshold:
                triggered = True
                reason = f"1Y change {price_change}% > threshold {threshold}%"

        elif alert_type == "change_below" and price_change:
            if price_change < threshold:
                triggered = True
                reason = f"1Y change {price_change}% < threshold {threshold}%"

        if triggered:
            triggered_alerts.append({**alert, "reason": reason})
            print(f"   🔔 TRIGGERED [{alert['id']}] {alert_type} — {reason}")
        else:
            skipped_alerts.append(alert)
            print(f"   ⏭️  Skipped  [{alert['id']}] {alert_type} @ {threshold}")

    print(
        f"\n✅ check_alerts_node → {len(triggered_alerts)} triggered / {len(skipped_alerts)} skipped"
    )

    return {
        "triggered_alerts": triggered_alerts,
        "skipped_alerts": skipped_alerts,
        "errors": errors,
    }
