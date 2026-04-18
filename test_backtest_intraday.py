from engine.backtest_intraday import run_intraday_backtest

df = run_intraday_backtest("data/raw/spot_5m.csv")

print(df.head())
print("\nTotal Trades:", len(df))
print("Total PnL:", df["pnl"].sum())
print("\nPnL by strategy:")
print(df.groupby("strategy")["pnl"].agg(["count", "sum", "mean"]))
