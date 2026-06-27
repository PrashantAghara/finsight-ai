from typing import TypedDict, Optional


class ReportAgentState(TypedDict):
    symbol: str

    current_price: Optional[float]
    price_change_pct: Optional[float]
    market_cap: Optional[float]
    pe_ratio: Optional[float]
    eps: Optional[float]
    revenue: Optional[float]
    profit_margin: Optional[float]
    beta: Optional[float]
    sector: Optional[str]
    industry: Optional[str]
    data_summary: Optional[str]

    sma_20: Optional[float]
    sma_50: Optional[float]
    rsi: Optional[float]
    macd: Optional[float]
    volatility: Optional[float]
    golden_cross: Optional[bool]
    pe_signal: Optional[str]
    margin_signal: Optional[str]
    momentum_signal: Optional[str]
    risk_score: Optional[float]
    risk_label: Optional[str]
    recommendation: Optional[str]
    reasoning: Optional[str]

    rag_context: Optional[str]

    executive_summary: Optional[str]
    financial_analysis: Optional[str]
    technical_analysis: Optional[str]
    risk_assessment: Optional[str]
    recommendation_section: Optional[str]

    full_report: Optional[str]
    report_id: Optional[str]
    generated_at: Optional[str]

    errors: Optional[list[str]]
