from supervisor.state import SupervisorState
from agents.rag_agent import build_rag_agent

rag_agent = build_rag_agent()


def run_rag_agent_node(state: SupervisorState) -> dict:
    symbol = state["symbol"]
    mode = state["mode"]
    question = state.get("question")
    file_path = state.get("file_path")
    errors = state.get("errors", [])

    print(f"\n{'─' * 50}")
    print(f"🤖 Supervisor → Running RAG Agent for {symbol} | mode: {mode}")
    print(f"{'─' * 50}")

    try:
        rag_mode = "ingest" if mode == "ingest" else "query"

        result = rag_agent.invoke(
            {
                "symbol": symbol,
                "mode": rag_mode,
                "file_path": file_path,
                "question": question,
                "errors": [],
            }
        )

        if rag_mode == "ingest":
            print(
                f"✅ RAG Agent complete → {result.get('chunks_stored')} chunks ingested"
            )
        else:
            print("✅ RAG Agent complete → answer generated")

        return {
            "rag_output": result,
            "errors": errors + result.get("errors", []),
        }

    except Exception as e:
        error = f"run_rag_agent_node error: {str(e)}"
        print(f"❌ {error}")
        return {"rag_output": None, "errors": errors + [error]}
