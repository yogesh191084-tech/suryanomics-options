import pandas as pd

from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime
from engine.strategy_selector import select_strategy
from engine.pnl_model import compute_intraday_pnl


def run_intraday_backtest(path):
    df = pd.read_csv(path, parse_dates=["datetime"])
    df = add_trend_indicators(df)

    trades = []

    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        if pd.isna(row["adx"]) or pd.isna(row["ema21"]):
            continue

        regime = detect_market_regime(row)
        strategy = select_strategy(regime)

        pnl = compute_intraday_pnl(
            entry_close=row["close"],
            exit_close=next_row["close"],
            strategy=strategy
        )

        trades.append({
            "datetime": row["datetime"],
            "strategy": strategy,
            "pnl": pnl
        })

    return pd.DataFrame(trades)
