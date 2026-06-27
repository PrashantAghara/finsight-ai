from typing import TypedDict, Optional, Literal


class SupervisorState(TypedDict):
    symbol: str
    user_id: Optional[int]
    mode: Literal["analyse", "report", "chat", "ingest"]

    question: Optional[str]
    file_path: Optional[str]

    data_output: Optional[dict]
    analysis_output: Optional[dict]
    rag_output: Optional[dict]
    report_output: Optional[dict]
    alert_output: Optional[dict]

    final_response: Optional[str]
    triggered_alerts: Optional[list[dict]]
    report_id: Optional[str]

    errors: Optional[list[str]]
