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
from engine.exit_engine import check_exit
from telegram.sender import send_message
from engine.volatility import is_low_volatility
from engine.risk_manager import is_daily_loss_exceeded


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

    return 10 < adx < 23


def already_traded_today():

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
SURYANOMICS OPTIONS - LIVE TRADE

SHORT STRANGLE ACTIVATED

Spot: Rs {round(trade['spot'], 2)}

CE SELL
Strike: {trade['ce']['strike']} CE
Entry: Rs {trade['ce']['entry']}
SL: Rs {trade['ce']['sl']}
Target: Rs {trade['ce']['target']}

PE SELL
Strike: {trade['pe']['strike']} PE
Entry: Rs {trade['pe']['entry']}
SL: Rs {trade['pe']['sl']}
Target: Rs {trade['pe']['target']}

Regime + Volatility filtered execution
"""
    send_message(msg)


def send_risk_stop_message():

    msg = """
SURYANOMICS OPTIONS

Daily loss limit hit

System stopped for today
"""
    send_message(msg)


# =====================================================
# MAIN RUN
# =====================================================

def run_once():

    print("Running Suryanomics bot (single cycle)\n")

    try:
        # STEP 1 → EXIT CHECK
        check_exit()

        # STEP 2 → RISK CONTROL
        if is_daily_loss_exceeded():
            print("DAILY LOSS LIMIT HIT - STOP TRADING")
            send_risk_stop_message()
            return

        # STEP 3 → PREVENT MULTIPLE TRADES
        if already_traded_today():
            print("Trade already taken today - skipping")
            return

        # STEP 4 → FETCH DATA
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
        print(f"Strategy: {strategy}")
        print(f"Day Type: {day_type}")
        print(f"ADX: {adx}")

        # FINAL ENTRY
        if (
            strategy == "SHORT_STRANGLE"
            and is_trade_allowed(day_type, adx)
            and is_low_volatility(df)
        ):

            print("TRADE ALLOWED")

            price = row.get("close", 0)

            trade = build_short_strangle(price)

            send_trade_alert(trade)
            log_trade(trade)

            print("Trade logged successfully")

        else:
            print("NO TRADE")
            # ❌ NO TELEGRAM MESSAGE HERE (FIXED)

    except Exception as e:
        print("ERROR:", e)


# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":
    run_once()