import yfinance as yf
import pandas as pd
from collections import Counter

from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime


SYMBOL = "^NSEI"      # Yahoo Finance symbol for NIFTY
INTERVAL = "15m"
PERIOD = "1y"


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


print("Fetching 1-year 15-minute NIFTY data...")
df = yf.download(
    SYMBOL,
    period=PERIOD,
    interval=INTERVAL,
    progress=False
)

if df is None or df.empty:
    raise RuntimeError("No data received from Yahoo Finance")

df = df.reset_index()

df = df.rename(columns={
    "Datetime": "datetime",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
})

print("Adding indicators (EMA21, ADX)...")
df = add_trend_indicators(df)

# Drop rows where indicators are not ready
df = df.dropna(subset=["adx", "ema21"])

print("Detecting regimes per candle...")
df["regime"] = df.apply(detect_market_regime, axis=1)
df["date"] = df["datetime"].dt.date

daily_rows = []

for date, group in df.groupby("date"):
    day_type = classify_day(group["regime"].tolist())

    daily_rows.append({
        "date": date,
        "candles": len(group),
        "range_pct": round((group["regime"] == "RANGE").mean(), 2),
        "trend_pct": round(
            group["regime"].isin(["TREND_UP", "TREND_DOWN"]).mean(), 2
        ),
        "day_type": day_type
    })

daily_df = pd.DataFrame(daily_rows)

print("\n=== DAY TYPE DISTRIBUTION (1 YEAR | 15m) ===")
print(daily_df["day_type"].value_counts())

print("\n=== SAMPLE DAILY BREAKDOWN ===")
print(daily_df.head(10))

print("\nTotal trading days analysed:", len(daily_df))
