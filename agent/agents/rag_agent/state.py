from typing import TypedDict, Optional, Literal


class RAGAgentState(TypedDict):
    symbol: str
    mode: Literal["ingest", "query"]
    file_path: Optional[str]
    question: Optional[str]

    chunks: Optional[list[str]]
    sources: Optional[list[dict]]
    chunks_stored: Optional[int]

    retrieved_docs: Optional[list[str]]
    retrieved_sources: Optional[list[dict]]
    answer: Optional[str]

    errors: Optional[list[str]]
