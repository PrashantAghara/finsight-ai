from typing import TypedDict, Optional


class AlertAgentState(TypedDict):
    symbol: str
    user_id: Optional[int]

    current_price: Optional[float]
    rsi: Optional[float]
    price_change_pct: Optional[float]
    risk_score: Optional[float]

    active_alerts: Optional[list[dict]]  # loaded from PostgreSQL

    triggered_alerts: Optional[list[dict]]
    skipped_alerts: Optional[list[dict]]
    alerts_triggered: Optional[int]

    errors: Optional[list[str]]
