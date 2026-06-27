import os
import shutil
import tempfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from supervisor.graph import build_supervisor


router = APIRouter()
supervisor = build_supervisor()

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}


class AnalyseRequest(BaseModel):
    symbol: str
    user_id: Optional[int] = None


class ChatRequest(BaseModel):
    symbol: str
    question: str
    user_id: Optional[int] = None


class AnalyseResponse(BaseModel):
    symbol: str
    mode: str
    final_response: str
    recommendation: Optional[str] = None
    risk_label: Optional[str] = None
    risk_score: Optional[float] = None
    current_price: Optional[float] = None
    triggered_alerts: Optional[list] = None
    report_id: Optional[str] = None
    errors: Optional[list] = None


def build_initial_state(
    symbol: str,
    mode: str,
    user_id: Optional[int] = None,
    question: Optional[str] = None,
    file_path: Optional[str] = None,
) -> dict:
    return {
        "symbol": symbol.upper(),
        "user_id": user_id,
        "mode": mode,
        "question": question,
        "file_path": file_path,
        "errors": [],
    }


def extract_response(result: dict, mode: str) -> AnalyseResponse:
    data = result.get("data_output") or {}
    analysis = result.get("analysis_output") or {}

    return AnalyseResponse(
        symbol=result["symbol"],
        mode=mode,
        final_response=result.get("final_response", ""),
        recommendation=analysis.get("recommendation"),
        risk_label=analysis.get("risk_label"),
        risk_score=analysis.get("risk_score"),
        current_price=data.get("current_price"),
        triggered_alerts=result.get("triggered_alerts", []),
        report_id=result.get("report_id"),
        errors=result.get("errors", []),
    )


@router.post("/analyse", response_model=AnalyseResponse)
def analyse(payload: AnalyseRequest):
    """
    Run Data Agent + Analysis Agent + Alert Agent.
    Returns price, technicals, risk score, recommendation.
    """
    try:
        state = build_initial_state(
            symbol=payload.symbol,
            mode="analyse",
            user_id=payload.user_id,
        )
        result = supervisor.invoke(state)
        return extract_response(result, "analyse")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/report", response_model=AnalyseResponse)
def generate_report(payload: AnalyseRequest):
    """
    Run full pipeline — Data + Analysis + RAG + Report + Alert agents.
    Generates and saves a full investment memo.
    """
    try:
        state = build_initial_state(
            symbol=payload.symbol,
            mode="report",
            user_id=payload.user_id,
            question=f"What are the key insights and risks for {payload.symbol}?",
        )
        result = supervisor.invoke(state)
        return extract_response(result, "report")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=AnalyseResponse)
def chat(payload: ChatRequest):
    """
    Run RAG Agent only — answer a question from uploaded documents.
    """
    try:
        state = build_initial_state(
            symbol=payload.symbol,
            mode="chat",
            user_id=payload.user_id,
            question=payload.question,
        )
        result = supervisor.invoke(state)
        return extract_response(result, "chat")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest", response_model=AnalyseResponse)
async def ingest(
    symbol: str,
    user_id: Optional[int] = None,
    file: UploadFile = File(...),
):
    """
    Upload a financial document (PDF, TXT, DOCX) for a symbol.
    Chunks and embeds into AstraDB.
    """
    ext = Path(file.filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {ALLOWED_EXTENSIONS}",
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        state = build_initial_state(
            symbol=symbol,
            mode="ingest",
            user_id=user_id,
            file_path=tmp_path,
        )
        result = supervisor.invoke(state)
        return extract_response(result, "ingest")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        os.unlink(tmp_path)
