from typing import TypedDict, Optional, Literal


class AnalysisAgentState(TypedDict):
    symbol: str
    current_price: Optional[float]
    high_52w: Optional[float]
    low_52w: Optional[float]
    price_change_pct: Optional[float]
    price_history: Optional[list[dict]]
    pe_ratio: Optional[float]
    eps: Optional[float]
    market_cap: Optional[float]
    revenue: Optional[float]
    profit_margin: Optional[float]
    beta: Optional[float]
    dividend_yield: Optional[float]
    sector: Optional[str]
    data_summary: Optional[str]

    sma_20: Optional[float]
    sma_50: Optional[float]
    sma_200: Optional[float]
    rsi: Optional[float]
    macd: Optional[float]
    macd_signal: Optional[float]
    volatility: Optional[float]

    price_vs_52w_high: Optional[float]
    price_vs_52w_low: Optional[float]
    golden_cross: Optional[bool]
    death_cross: Optional[bool]

    pe_signal: Optional[str]
    margin_signal: Optional[str]
    momentum_signal: Optional[str]

    risk_score: Optional[float]
    risk_label: Optional[str]
    recommendation: Optional[
        Literal["strong_buy", "buy", "hold", "sell", "strong_sell"]
    ]
    reasoning: Optional[str]

    errors: Optional[list[str]]
