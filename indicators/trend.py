import pandas as pd
from ta.trend import EMAIndicator, ADXIndicator

def add_trend_indicators(df):
    """
    Adds:
    - ema21
    - adx
    """
    df = df.copy()

    df["ema21"] = EMAIndicator(close=df["close"], window=21).ema_indicator()

    adx = ADXIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"],
        window=14
    )

    df["adx"] = adx.adx()

    return df
