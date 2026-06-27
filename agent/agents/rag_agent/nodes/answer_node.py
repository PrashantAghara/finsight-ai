from agents.rag_agent.state import RAGAgentState
from clients.clients import groq_client

RAG_SYSTEM_PROMPT = """
You are FinSight, an AI financial analyst assistant.
Answer the user's question strictly based on the provided document context.

Rules:
1. Answer ONLY from the provided context
2. If context is insufficient say: "I don't have enough information in the uploaded documents to answer this."
3. Always cite the source filename and page number
4. Be concise and precise — financial accuracy matters
5. Never speculate beyond what the documents say
"""


def answer_node(state: RAGAgentState) -> dict:
    symbol = state["symbol"]
    question = state.get("question")
    retrieved_docs = state.get("retrieved_docs", [])
    sources = state.get("retrieved_sources", [])
    errors = state.get("errors", [])

    print(f"💬 Generating answer for {symbol}: '{question}'")

    if not retrieved_docs:
        answer = (
            "I don't have enough information in the uploaded "
            f"documents to answer this question about {symbol}."
        )
        print("⚠️  No retrieved docs — returning default answer")
        return {"answer": answer, "errors": errors}

    context = "\n\n---\n\n".join(
        [
            f"[Source: {src.get('filename', 'unknown')}, Page {src.get('page', 0)}]\n{doc}"
            for doc, src in zip(retrieved_docs, sources)
        ]
    )

    prompt = f"""
    Context from {symbol} financial documents:

    {context}

    Question: {question}

    Answer based strictly on the context above.
    """

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
        answer = response.choices[0].message.content.strip()
        print(f"✅ answer_node → Answer generated for {symbol}")
        print("\n── Answer ───────────────────────────────")
        print(answer)
        return {"answer": answer, "errors": errors}

    except Exception as e:
        error = f"answer_node error: {str(e)}"
        print(f"❌ {error}")
        return {
            "answer": "Unable to generate answer due to an error.",
            "errors": errors + [error],
        }
