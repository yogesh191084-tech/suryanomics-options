import pandas as pd

from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime
from engine.strategy_selector import select_strategy
from engine.pnl_model import compute_intraday_pnl


MAX_TRADES_PER_SESSION = 15  # HARD DAILY CAP (LOCKED)


def run_session(df):
    """
    Runs one paper-live session on intraday data
    Applies a strict daily trade cap for risk control
    """
    df = add_trend_indicators(df)

    session_pnl = 0
    trades = 0

    for i in range(len(df) - 1):

        # ---- DAILY TRADE CAP ENFORCEMENT ----
        if trades >= MAX_TRADES_PER_SESSION:
            break

        row = df.iloc[i]
        next_row = df.iloc[i + 1]

        # Skip until indicators are valid
        if pd.isna(row["adx"]) or pd.isna(row["ema21"]):
            continue

        regime = detect_market_regime(row)
        strategy = select_strategy(regime)

        if strategy == "NO_TRADE":
            continue

        pnl = compute_intraday_pnl(
            entry_close=row["close"],
            exit_close=next_row["close"],
            strategy=strategy
        )

        session_pnl += pnl
        trades += 1

    return {
        "trades": trades,
        "pnl": session_pnl
    }
