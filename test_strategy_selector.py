from engine.strategy_selector import select_strategy

regimes = ["TREND_UP", "TREND_DOWN", "RANGE", "NO_TRADE"]

for r in regimes:
    print(r, "→", select_strategy(r))
