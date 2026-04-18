import pandas as pd

from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime
from engine.strategy_selector import select_strategy


def run_backtest_spot(path):
    """
    Backtests regime + strategy selection on historical spot data
    """
    df = pd.read_csv(path, parse_dates=["datetime"])

    df = add_trend_indicators(df)

    results = []

    for i in range(len(df)):
        row = df.iloc[i]

        # Skip until indicators are valid
        if pd.isna(row.get("adx")) or pd.isna(row.get("ema21")):
            continue

        regime = detect_market_regime(row)
        strategy = select_strategy(regime)

        results.append({
            "datetime": row["datetime"],
            "close": row["close"],
            "adx": row["adx"],
            "ema21": row["ema21"],
            "regime": regime,
            "strategy": strategy
        })

    return pd.DataFrame(results)
