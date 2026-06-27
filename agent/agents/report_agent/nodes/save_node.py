from agents.report_agent.state import ReportAgentState
from db.session import get_connection


def save_node(state: ReportAgentState) -> dict:
    symbol = state["symbol"]
    full_report = state.get("full_report", "")
    report_id = state.get("report_id", "")
    errors = state.get("errors", [])

    print(f"💾 Saving report {report_id} to PostgreSQL...")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO reports (
                report_id, symbol, full_report,
                recommendation, risk_label, risk_score, generated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (report_id) DO NOTHING
            RETURNING id;
        """,
            (
                report_id,
                symbol,
                full_report,
                state.get("recommendation"),
                state.get("risk_label"),
                state.get("risk_score"),
            ),
        )

        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if result:
            print(f"✅ save_node → Report saved (db id: {result[0]})")
        else:
            print("⚠️  save_node → Report already exists, skipped")

        return {"errors": errors}

    except Exception as e:
        error = f"save_node error: {str(e)}"
        print(f"❌ {error}")
        return {"errors": errors + [error]}
