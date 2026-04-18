import pandas as pd

def is_low_volatility(df):
    """
    Detect if market is suitable for short strangle
    """

    if df is None or len(df) < 20:
        return False

    recent_range = (df["high"] - df["low"]).tail(10).mean()
    avg_range = (df["high"] - df["low"]).mean()

    # Low volatility = range shrinking
    return recent_range < avg_range