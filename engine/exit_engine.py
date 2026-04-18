import pandas as pd
import os
from datetime import datetime, time

from ingestion.option_chain import get_premium
from telegram.sender import send_message

LOG_FILE = "logs/trades.csv"


def check_exit():

    if not os.path.exists(LOG_FILE):
        print("No trade log found")
        return

    try:
        df = pd.read_csv(LOG_FILE)
    except Exception as e:
        print("Error reading log:", e)
        return

    if df.empty:
        print("No trades")
        return

    last_trade = df.iloc[-1]

    # Only check OPEN trades
    if last_trade.get("status") != "OPEN":
        print("No open trade")
        return

    ce_strike = last_trade["ce_strike"]
    pe_strike = last_trade["pe_strike"]

    ce_entry = last_trade["ce_entry"]
    pe_entry = last_trade["pe_entry"]

    ce_sl = last_trade["ce_sl"]
    pe_sl = last_trade["pe_sl"]

    ce_target = last_trade["ce_target"]
    pe_target = last_trade["pe_target"]

    # ===== LIVE PREMIUM FETCH =====
    try:
        ce_price = get_premium(ce_strike, "CE")
        pe_price = get_premium(pe_strike, "PE")
    except Exception as e:
        print("Premium fetch error:", e)
        return

    if ce_price is None or pe_price is None:
        print("Premium data missing")
        return

    exit_reason = None

    # ===== EXIT CONDITIONS =====
    if ce_price >= ce_sl or pe_price >= pe_sl:
        exit_reason = "SL HIT"

    elif ce_price <= ce_target and pe_price <= pe_target:
        exit_reason = "TARGET HIT"

    # 🔥 TIME EXIT (MANDATORY)
    elif datetime.now().time() >= time(15, 15):
        exit_reason = "TIME EXIT"

    if exit_reason is None:
        print("Trade still open")
        return

    # ===== PnL =====
    ce_pnl = ce_entry - ce_price
    pe_pnl = pe_entry - pe_price
    total_pnl = ce_pnl + pe_pnl

    print(f"EXIT: {exit_reason}")
    print(f"PnL: {total_pnl}")

    # ===== UPDATE CSV =====
    df.loc[df.index[-1], "status"] = "CLOSED"
    df.loc[df.index[-1], "exit_ce"] = ce_price
    df.loc[df.index[-1], "exit_pe"] = pe_price
    df.loc[df.index[-1], "pnl"] = total_pnl
    df.loc[df.index[-1], "exit_reason"] = exit_reason

    df.to_csv(LOG_FILE, index=False)

    # ===== TELEGRAM =====
    msg = f"""
📊 SURYANOMICS OPTIONS – EXIT

🚨 {exit_reason}

CE Exit: ₹{round(ce_price, 2)}
PE Exit: ₹{round(pe_price, 2)}

💰 PnL: ₹{round(total_pnl, 2)}
"""
    send_message(msg)