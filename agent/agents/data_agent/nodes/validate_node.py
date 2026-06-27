from agents.data_agent.state import DataAgentState

MAX_RETRIES = 2


def validate_node(state: DataAgentState) -> dict:
    price_ok = state.get("price_fetch_success", False)
    fundamentals_ok = state.get("fundamentals_fetch_success", False)
    retry_count = state.get("retry_count", 0)
    errors = state.get("errors", [])
    symbol = state["symbol"]

    print(f"🔍 Validating data for {symbol}...")
    print(f"   Price fetch:        {'✅' if price_ok else '❌'}")
    print(f"   Fundamentals fetch: {'✅' if fundamentals_ok else '❌'}")
    print(f"   Retry count:        {retry_count}/{MAX_RETRIES}")

    if price_ok and fundamentals_ok:
        print("✅ validate_node → All data valid, proceeding")
        return {
            "data_ready": True,
            "retry_count": retry_count,
            "errors": errors,
        }

    if retry_count < MAX_RETRIES:
        print(
            f"⚠️  validate_node → Incomplete data, retrying ({retry_count + 1}/{MAX_RETRIES})"
        )
        return {
            "data_ready": False,
            "retry_count": retry_count + 1,
            "errors": errors,
        }

    print("⚠️  validate_node → Max retries hit, proceeding with partial data")
    return {
        "data_ready": True,
        "retry_count": retry_count,
        "errors": errors + [f"Max retries hit for {symbol} — partial data"],
    }
