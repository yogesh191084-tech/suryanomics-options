import pandas as pd

from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime
from engine.strategy_selector import select_strategy

# Load full spot data
df = pd.read_csv("data/raw/spot_5m.csv", parse_dates=["datetime"])

# Filter ONLY today's data
today = df["datetime"].dt.date.max()
today_df = df[df["datetime"].dt.date == today].copy()

print("Testing date:", today)
print("Total candles:", len(today_df))

# Add indicators
today_df = add_trend_indicators(today_df)

print("\n--- SYSTEM DECISIONS (TODAY) ---")

for i in range(len(today_df)):
    row = today_df.iloc[i]

    if pd.isna(row["adx"]) or pd.isna(row["ema21"]):
        continue

    regime = detect_market_regime(row)
    strategy = select_strategy(regime)

    print(
        row["datetime"],
        "| Close:", round(row["close"], 2),
        "| Regime:", regime,
        "| Strategy:", strategy
    )
