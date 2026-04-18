def select_strategy(regime):
    """
    Maps market regime to allowed option strategy
    """
    if regime == "TREND_UP":
        return "BULL_CALL_SPREAD"

    if regime == "TREND_DOWN":
        return "BEAR_PUT_SPREAD"

    if regime == "RANGE":
        return "SHORT_STRANGLE"

    return "NO_TRADE"
