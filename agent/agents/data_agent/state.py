from typing import TypedDict, Optional


class DataAgentState(TypedDict):
    symbol: str
    period: str

    current_price: Optional[float]
    open_price: Optional[float]
    high_52w: Optional[float]
    low_52w: Optional[float]
    volume: Optional[int]
    avg_volume: Optional[int]
    price_history: Optional[list[dict]]
    price_change_pct: Optional[float]

    market_cap: Optional[float]
    pe_ratio: Optional[float]
    eps: Optional[float]
    revenue: Optional[float]
    profit_margin: Optional[float]
    dividend_yield: Optional[float]
    beta: Optional[float]
    sector: Optional[str]
    industry: Optional[str]
    description: Optional[str]

    price_fetch_success: Optional[bool]
    fundamentals_fetch_success: Optional[bool]
    retry_count: Optional[int]
    errors: Optional[list[str]]

    data_ready: Optional[bool]
    summary: Optional[str]
