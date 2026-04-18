def detect_market_regime(row):
    adx = row["adx"]
    ema21 = row["ema21"]
    close = row["close"]

    if adx < 15:
        return "RANGE"

    if adx > 30:
        return "TREND_UP" if close > ema21 else "TREND_DOWN"

    return "NO_TRADE"
