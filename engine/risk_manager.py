import pandas as pd
import os
from datetime import datetime

LOG_FILE = "logs/trades.csv"

DAILY_LOSS_LIMIT = -1000   # 🔥 change based on your capital


def is_daily_loss_exceeded():

    if not os.path.exists(LOG_FILE):
        return False

    df = pd.read_csv(LOG_FILE)

    if df.empty or "pnl" not in df.columns:
        return False

    today = datetime.now().strftime("%Y-%m-%d")

    df_today = df[df["date"] == today]

    if df_today.empty:
        return False

    total_pnl = df_today["pnl"].sum()

    print(f"Today's PnL: {total_pnl}")

    return total_pnl <= DAILY_LOSS_LIMIT