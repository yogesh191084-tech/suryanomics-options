from engine.backtest import run_backtest_spot

df = run_backtest_spot("data/raw/spot_5m.csv")

print(df.head())
print("\nStrategy distribution:")
print(df["strategy"].value_counts())

