import pandas as pd

def iv_percentile(iv_series, lookback=100):
    """
    Rolling IV Percentile
    """
    return iv_series.rolling(lookback).apply(
        lambda x: (x.rank(pct=True).iloc[-1]) * 100,
        raw=False
    )
