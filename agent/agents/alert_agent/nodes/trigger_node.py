from datetime import datetime
from agents.alert_agent.state import AlertAgentState
from db.session import get_connection


def trigger_node(state: AlertAgentState) -> dict:
    symbol = state["symbol"]
    triggered_alerts = state.get("triggered_alerts", [])
    errors = state.get("errors", [])

    if not triggered_alerts:
        print(f"✅ trigger_node → No alerts to trigger for {symbol}")
        return {
            "alerts_triggered": 0,
            "errors": errors,
        }

    print(f"🔔 Triggering {len(triggered_alerts)} alerts for {symbol}...")

    conn = get_connection()
    cur = conn.cursor()

    for alert in triggered_alerts:
        try:
            cur.execute(
                """
                UPDATE alerts
                SET status       = 'triggered',
                    triggered_at = %s
                WHERE id = %s;
            """,
                (datetime.now(), alert["id"]),
            )

            print(f"   ✅ Alert [{alert['id']}] marked as triggered")
            print(f"      Type:   {alert['alert_type']}")
            print(f"      Reason: {alert['reason']}")

        except Exception as e:
            error = f"Failed to trigger alert {alert['id']}: {str(e)}"
            print(f"   ❌ {error}")
            errors.append(error)

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n✅ trigger_node → {len(triggered_alerts)} alerts triggered for {symbol}")

    return {
        "alerts_triggered": len(triggered_alerts),
        "errors": errors,
    }
