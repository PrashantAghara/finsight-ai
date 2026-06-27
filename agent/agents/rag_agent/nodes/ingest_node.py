from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from agents.rag_agent.state import RAGAgentState


def ingest_node(state: RAGAgentState) -> dict:
    symbol = state["symbol"]
    file_path = state.get("file_path")
    errors = state.get("errors", [])

    if not file_path:
        error = "No file_path provided for ingest"
        print(f"❌ {error}")
        return {"errors": errors + [error]}

    print(f"📄 Ingesting document for {symbol}: {file_path}")

    try:
        ext = Path(file_path).suffix.lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        docs = loader.load()
        print(f"   Loaded {len(docs)} page(s)")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=64,
            separators=["\n\n", "\n", ".", " "],
        )
        split_docs = splitter.split_documents(docs)
        print(f"   Split into {len(split_docs)} chunks")

        chunks = [doc.page_content for doc in split_docs]
        sources = [
            {
                "symbol": symbol,
                "filename": Path(file_path).name,
                "page": doc.metadata.get("page", 0),
                "chunk_index": i,
                "char_count": len(doc.page_content),
            }
            for i, doc in enumerate(split_docs)
        ]

        print(f"✅ ingest_node → {len(chunks)} chunks ready for {symbol}")
        return {
            "chunks": chunks,
            "sources": sources,
            "errors": errors,
        }

    except Exception as e:
        error = f"ingest_node error: {str(e)}"
        print(f"❌ {error}")
        return {"errors": errors + [error]}
