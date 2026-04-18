import os
import sys
from datetime import datetime
from collections import Counter

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.spot_fetcher import fetch_spot_5m
from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime
from engine.strategy_selector import select_strategy
from engine.option_engine import build_short_strangle
from engine.trade_logger import log_trade
from telegram.sender import send_message


SYMBOL = "NIFTY"
LOG_FILE = "logs/trades.csv"


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


def is_trade_allowed(day_type, adx):

    if day_type == "TREND_DAY":
        return False

    if adx is None or pd.isna(adx):
        return False

    # RANGE + controlled MIXED
    return adx < 20


def already_traded_today():
    """
    Prevent duplicate trades in same day
    """

    if not os.path.exists(LOG_FILE):
        return False

    try:
        df = pd.read_csv(LOG_FILE)
        today = datetime.now().strftime("%Y-%m-%d")

        if "date" not in df.columns:
            return False

        return (df["date"] == today).any()

    except Exception:
        return False


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

⚡ Regime-filtered execution
"""
    send_message(msg)


# =====================================================
# MAIN RUN (GITHUB SAFE)
# =====================================================

def run_once():
   send_message("🚀 TELEGRAM TEST WORKING")
    print("Running Suryanomics bot (single cycle)\n")

    # ❌ Skip if already traded today
    if already_traded_today():
        print("WARNING: Trade already taken today - skipping")
        return

    df = fetch_spot_5m(SYMBOL)

    if df is None or df.empty:
        print("No data")
        return

    df = add_trend_indicators(df)
    row = df.iloc[-1]

    adx = row.get("adx")

    regime = detect_market_regime(row)
    strategy = select_strategy(regime)

    day_type = classify_day([regime])

    print(f"Regime: {regime}")
    print(f"Day Type: {day_type}")
    print(f"ADX: {adx}")

    # ===== FINAL DECISION =====
    if is_trade_allowed(day_type, adx):

        print("✅ TRADE ALLOWED")

        price = row.get("close", 0)

        trade = build_short_strangle(price)

        # ✅ Send Telegram
        send_trade_alert(trade)

        # ✅ Log Trade
        log_trade(trade)

        print("📊 Trade logged successfully")

    else:
        print("❌ NO TRADE")


# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":
    run_once()