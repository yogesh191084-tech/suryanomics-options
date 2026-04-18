import pandas as pd

def compute_expectancy(df):
    """
    Computes expectancy metrics for a given dataframe
    """
    return {
        "trades": len(df),
        "total_pnl": df["pnl"].sum(),
        "mean_pnl": df["pnl"].mean(),
        "win_rate": (df["pnl"] > 0).mean() if len(df) > 0 else 0
    }


def compute_max_drawdown(pnl_series):
    """
    Unit-based max drawdown
    """
    cumulative = pnl_series.cumsum()
    running_max = cumulative.cummax()
    drawdown = cumulative - running_max
    return drawdown.min()
