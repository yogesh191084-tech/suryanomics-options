import pandas as pd
from engine.session_replay import run_session

df = pd.read_csv("data/raw/spot_5m.csv", parse_dates=["datetime"])

# Group by date → each date = one session
sessions = df.groupby(df["datetime"].dt.date)

results = []

for date, day_df in sessions:
    stats = run_session(day_df)
    stats["date"] = date
    results.append(stats)

result_df = pd.DataFrame(results)

print(result_df)
print("\nAverage PnL:", result_df["pnl"].mean())
print("Average trades per session:", result_df["trades"].mean())
