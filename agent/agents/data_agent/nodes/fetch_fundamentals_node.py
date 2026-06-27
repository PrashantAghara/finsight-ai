import os
import requests
from agents.data_agent.state import DataAgentState

ALPHA_VANTAGE_BASE = "https://www.alphavantage.co/query"


def safe_float(val):
    try:
        return float(val) if val and val != "None" else None
    except Exception:
        return None


def fetch_fundamentals_node(state: DataAgentState) -> dict:
    symbol = state["symbol"]
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    errors = state.get("errors", [])

    print(f"📊 Fetching fundamentals for {symbol}...")

    try:
        response = requests.get(
            ALPHA_VANTAGE_BASE,
            params={"function": "OVERVIEW", "symbol": symbol, "apikey": api_key},
        )
        data = response.json()

        if "Note" in data:
            raise ValueError("Alpha Vantage rate limit hit — wait 1 minute")

        if not data or "Symbol" not in data:
            raise ValueError(f"No fundamental data found for {symbol}")

        market_cap = safe_float(data.get("MarketCapitalization"))
        pe_ratio = safe_float(data.get("PERatio"))
        eps = safe_float(data.get("EPS"))
        revenue = safe_float(data.get("RevenueTTM"))
        profit_margin = safe_float(data.get("ProfitMargin"))
        dividend_yield = safe_float(data.get("DividendYield"))
        beta = safe_float(data.get("Beta"))
        sector = data.get("Sector")
        industry = data.get("Industry")
        description = data.get("Description", "")

        print(f"✅ fetch_fundamentals_node → {symbol}")
        print(
            f"   Market Cap:    ${market_cap:,.0f}"
            if market_cap
            else "   Market Cap: N/A"
        )
        print(f"   P/E Ratio:     {pe_ratio}")
        print(f"   EPS:           {eps}")
        print(f"   Profit Margin: {profit_margin}")
        print(f"   Sector:        {sector}")
        print(f"   Industry:      {industry}")

        return {
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "eps": eps,
            "revenue": revenue,
            "profit_margin": profit_margin,
            "dividend_yield": dividend_yield,
            "beta": beta,
            "sector": sector,
            "industry": industry,
            "description": description,
            "fundamentals_fetch_success": True,
            "errors": errors,
        }
    except Exception as e:
        error_msg = f"fetch_fundamentals_node error: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "fundamentals_fetch_success": False,
            "errors": errors + [error_msg],
        }
