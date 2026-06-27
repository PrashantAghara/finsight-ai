from langchain_core.documents import Document
from agents.rag_agent.state import RAGAgentState
from clients.clients import vector_store


def embed_node(state: RAGAgentState) -> dict:
    symbol = state["symbol"]
    chunks = state.get("chunks", [])
    sources = state.get("sources", [])
    errors = state.get("errors", [])

    if not chunks:
        error = "No chunks to embed"
        print(f"❌ {error}")
        return {"errors": errors + [error]}

    print(f"⏳ Embedding {len(chunks)} chunks for {symbol}...")

    documents = [
        Document(
            page_content=chunk,
            metadata=sources[i] if i < len(sources) else {"symbol": symbol},
        )
        for i, chunk in enumerate(chunks)
    ]

    inserted_ids = vector_store.add_documents(documents)

    print(f"✅ embed_node → {len(inserted_ids)} chunks upserted for {symbol}")
    return {
        "chunks_stored": len(inserted_ids),
        "errors": errors,
    }
