from agents.alert_agent.state import AlertAgentState
from db.session import get_connection


def load_alerts_node(state: AlertAgentState) -> dict:
    symbol = state["symbol"]
    user_id = state.get("user_id")
    errors = state.get("errors", [])

    print(f"📋 Loading active alerts for {symbol} (user: {user_id})...")

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT id, symbol, alert_type, threshold, status
            FROM alerts
            WHERE symbol = %s
            AND status = 'active'
        """
        params = [symbol]

        if user_id:
            query += " AND user_id = %s"
            params.append(user_id)

        query += " ORDER BY id;"

        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        active_alerts = [
            {
                "id": row[0],
                "symbol": row[1],
                "alert_type": row[2],
                "threshold": row[3],
                "status": row[4],
            }
            for row in rows
        ]

        print(f"✅ load_alerts_node → {len(active_alerts)} active alerts for {symbol}")
        for alert in active_alerts:
            print(f"   [{alert['id']}] {alert['alert_type']} @ {alert['threshold']}")

        return {
            "active_alerts": active_alerts,
            "errors": errors,
        }

    except Exception as e:
        error = f"load_alerts_node error: {str(e)}"
        print(f"❌ {error}")
        return {
            "active_alerts": [],
            "errors": errors + [error],
        }
