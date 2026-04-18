import pandas as pd
import os
from telegram.sender import send_message

LOG_FILE = "logs/trades.csv"


def generate_performance():

    if not os.path.exists(LOG_FILE):
        print("No trade log found")
        return

    df = pd.read_csv(LOG_FILE)

    if df.empty:
        print("No trades available")
        return

    print(f"Total rows in log: {len(df)}")

    # Check CLOSED trades
    closed_df = df[df["status"] == "CLOSED"]

    if closed_df.empty:
        print("No CLOSED trades yet (waiting for exit)")
        return

    total_trades = len(closed_df)
    total_pnl = closed_df["pnl"].sum()
    avg_pnl = closed_df["pnl"].mean()

    wins = closed_df[closed_df["pnl"] > 0]
    win_rate = (len(wins) / total_trades) * 100

    best_trade = closed_df["pnl"].max()
    worst_trade = closed_df["pnl"].min()

    print("\n===== PERFORMANCE =====")
    print(f"Total Trades: {total_trades}")
    print(f"Win Rate: {round(win_rate,2)}%")
    print(f"Total PnL: {round(total_pnl,2)}")
    print(f"Avg PnL: {round(avg_pnl,2)}")
    print(f"Best Trade: {round(best_trade,2)}")
    print(f"Worst Trade: {round(worst_trade,2)}")

    # Telegram
    msg = f"""
📊 SURYANOMICS OPTIONS – PERFORMANCE

Total Trades: {total_trades}
Win Rate: {round(win_rate,2)}%

Total PnL: ₹{round(total_pnl,2)}
Avg Trade: ₹{round(avg_pnl,2)}

Best Trade: ₹{round(best_trade,2)}
Worst Trade: ₹{round(worst_trade,2)}
"""
    send_message(msg)


if __name__ == "__main__":
    generate_performance()