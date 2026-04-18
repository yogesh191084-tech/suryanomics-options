from engine.backtest_intraday import run_intraday_backtest
from engine.analysis import compute_expectancy, compute_max_drawdown

# Load backtest results
df = run_intraday_backtest("data/raw/spot_5m.csv")

print("\n=== REGIME-WISE EXPECTANCY ===")
for regime in df["strategy"].unique():
    sub = df[df["strategy"] == regime]
    stats = compute_expectancy(sub)
    dd = compute_max_drawdown(sub["pnl"])

    print(f"\nStrategy: {regime}")
    for k, v in stats.items():
        print(f"{k}: {round(v, 3)}")
    print("max_drawdown:", dd)
