from agents.rag_agent.state import RAGAgentState
from clients.clients import vector_store

SIMILARITY_THRESHOLD = 0.65


def retrieve_node(state: RAGAgentState) -> dict:
    symbol = state["symbol"]
    question = state.get("question")
    errors = state.get("errors", [])

    if not question:
        error = "No question provided for retrieval"
        print(f"❌ {error}")
        return {"errors": errors + [error]}

    print(f"🔍 Retrieving docs for {symbol}: '{question}'")

    results = vector_store.similarity_search_with_score(
        query=question,
        k=4,
        filter={"symbol": symbol},
    )

    if not results:
        print(f"⚠️  No results found for {symbol}")
        return {
            "retrieved_docs": [],
            "retrieved_sources": [],
            "errors": errors,
        }

    retrieved_docs = []
    retrieved_sources = []

    for doc, score in results:
        if score >= SIMILARITY_THRESHOLD:
            retrieved_docs.append(doc.page_content)
            retrieved_sources.append(
                {
                    **doc.metadata,
                    "similarity_score": round(score, 4),
                }
            )
            print(f"   Score: {round(score, 4)} | {doc.page_content[:80]}...")
        else:
            print(f"   ⚠️ Discarded (score: {round(score, 4)}) — below threshold")

    print(f"✅ retrieve_node → {len(retrieved_docs)} relevant chunks for {symbol}")
    return {
        "retrieved_docs": retrieved_docs,
        "retrieved_sources": retrieved_sources,
        "errors": errors,
    }
