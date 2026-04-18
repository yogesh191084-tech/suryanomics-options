import time
import os
import sys
from datetime import datetime, time as dtime
from collections import Counter

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.spot_fetcher import fetch_spot_5m
from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime
from engine.strategy_selector import select_strategy
from engine.option_engine import build_short_strangle
from telegram.sender import send_message


SYMBOL = "NIFTY"
MARKET_CLOSE_TIME = dtime(15, 30)


# =====================================================
# HELPERS
# =====================================================

def classify_day(regimes):
    counts = Counter(regimes)
    total = sum(counts.values())

    if total == 0:
        return "NO_DATA"

    range_pct = counts.get("RANGE", 0) / total
    trend_pct = (
        counts.get("TREND_UP", 0) + counts.get("TREND_DOWN", 0)
    ) / total

    if range_pct >= 0.6:
        return "RANGE_DAY"
    elif trend_pct >= 0.6:
        return "TREND_DAY"
    else:
        return "MIXED_DAY"


# =====================================================
# TELEGRAM MESSAGE
# =====================================================

def send_trade_alert(trade):

    msg = f"""
📊 SURYANOMICS OPTIONS – LIVE TRADE

🚨 SHORT STRANGLE ACTIVATED

Spot: ₹{round(trade['spot'], 2)}

📉 CE SELL
Strike: {trade['ce']['strike']} CE  
Entry: ₹{trade['ce']['entry']}  
SL: ₹{trade['ce']['sl']}  
Target: ₹{trade['ce']['target']}

📉 PE SELL
Strike: {trade['pe']['strike']} PE  
Entry: ₹{trade['pe']['entry']}  
SL: ₹{trade['pe']['sl']}  
Target: ₹{trade['pe']['target']}

⚡ System-based execution
"""
    send_message(msg)


# =====================================================
# MAIN LOOP
# =====================================================

def start_live_loop(sleep_seconds=60):
    print("🚀 Suryanomics Live Trading Started\n")

    day_regimes = []
    signal_sent = False

    while True:
        now = datetime.now()
        print(f"\n--- Live Cycle @ {now} ---")

        if now.time() >= MARKET_CLOSE_TIME:
            print("Market closed")
            break

        df = fetch_spot_5m(SYMBOL)

        if df is None or df.empty:
            print("No data")
            time.sleep(sleep_seconds)
            continue

        df = add_trend_indicators(df)
        row = df.iloc[-1]

        if pd.isna(row.get("adx")):
            print("Indicators not ready")
            time.sleep(sleep_seconds)
            continue

        regime = detect_market_regime(row)
        strategy = select_strategy(regime)

        day_regimes.append(regime)
        day_type = classify_day(day_regimes)

        print(f"Regime: {regime}")
        print(f"Strategy: {strategy}")
        print(f"Day Type: {day_type}")

        # ===== REAL SIGNAL =====
        if not signal_sent:

            print("✅ VALID TRADE CONDITION")

            if not signal_sent:
                price = row.get("close", 0)

                trade = build_short_strangle(price)

                send_trade_alert(trade)

                signal_sent = True
                print("🚀 TRADE SENT TO TELEGRAM")

        else:
            print("❌ NO TRADE")

        time.sleep(sleep_seconds)


# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":
    start_live_loop()