import yfinance as yf
import pandas as pd

from indicators.trend import add_trend_indicators


SYMBOL = "^NSEI"   # NIFTY 50 Yahoo symbol
PERIOD = "1y"
INTERVAL = "1d"


def detect_daily_regime(row):
    adx = row["adx"]
    close = row["close"]
    ema21 = row["ema21"]

    if pd.isna(adx) or pd.isna(ema21):
        return "NO_DATA"

    if adx < 15:
        return "RANGE"

    if adx > 30:
        return "TREND_UP" if close > ema21 else "TREND_DOWN"

    return "NO_TRADE"


def classify_day(regime):
    if regime == "RANGE":
        return "RANGE_DAY"
    if regime in ("TREND_UP", "TREND_DOWN"):
        return "TREND_DAY"
    return "MIXED_DAY"


print("Fetching 1-year DAILY NIFTY data...")
df = yf.download(
    SYMBOL,
    period=PERIOD,
    interval=INTERVAL,
    progress=False
)

if df is None or df.empty:
    raise RuntimeError("No daily data received from Yahoo Finance")

# ---- Normalize columns ----
df.columns = [c[0].lower() if isinstance(c, tuple) else c.lower() for c in df.columns]

# ---- Reset index and FORCE first column to datetime ----
df = df.reset_index()
df = df.rename(columns={df.columns[0]: "datetime"})

print("Adding indicators (EMA21, ADX)...")
df = add_trend_indicators(df)

df = df.dropna(subset=["adx", "ema21"])

print("Detecting daily regimes...")
df["regime"] = df.apply(detect_daily_regime, axis=1)
df["day_type"] = df["regime"].apply(classify_day)

print("\n=== DAY TYPE DISTRIBUTION (1 YEAR | DAILY) ===")
print(df["day_type"].value_counts())

print("\n=== SAMPLE DAILY BREAKDOWN ===")
print(df[["datetime", "close", "ema21", "adx", "day_type"]].head(10))

print("\nTotal trading days analysed:", len(df))
