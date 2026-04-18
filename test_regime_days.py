import pandas as pd
from collections import Counter

from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime


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


# Load intraday spot data
df = pd.read_csv("data/raw/spot_5m.csv", parse_dates=["datetime"])

# Add indicators
df = add_trend_indicators(df)

# Keep only valid rows
df = df.dropna(subset=["adx", "ema21"])

# Detect regime per candle
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

print("\n=== DAY TYPE DISTRIBUTION ===")
print(daily_df["day_type"].value_counts())

print("\n=== DAILY BREAKDOWN ===")
print(daily_df)
