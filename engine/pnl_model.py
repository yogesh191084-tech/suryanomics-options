def compute_intraday_pnl(entry_close, exit_close, strategy):
    """
    Conservative intraday PnL model (unit-based)
    """
    move_pct = (exit_close - entry_close) / entry_close * 100

    threshold = 0.25  # percent

    if strategy == "BULL_CALL_SPREAD":
        if move_pct > threshold:
            return 1
        elif move_pct < -threshold:
            return -1
        else:
            return 0

    if strategy == "BEAR_PUT_SPREAD":
        if move_pct < -threshold:
            return 1
        elif move_pct > threshold:
            return -1
        else:
            return 0

    if strategy == "SHORT_STRANGLE":
        if abs(move_pct) < threshold:
            return 1
        else:
            return -1

    return 0
