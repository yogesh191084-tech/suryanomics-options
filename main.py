import pandas as pd

from config.settings import INITIAL_CAPITAL, MAX_DAILY_RISK_PCT, INDEX
from config.contract_specs import INDEX_SPECS

from indicators.trend import add_trend_indicators
from engine.regime import detect_market_regime
from engine.strategy_selector import select_strategy
from engine.options_chain import get_atm_strike
from strategies.builders import (
    build_bull_call_spread,
    build_bear_put_spread,
    build_short_strangle
)
from risk.position_sizing import calculate_lots
from risk.risk_guard import DailyRiskGuard
from engine.trade import Trade
from engine.trade_manager import TradeManager


def main():
    print("Suryanomics Options Engine — PAPER MODE")

    # --- Setup ---
    capital = INITIAL_CAPITAL
    risk_guard = DailyRiskGuard(capital, MAX_DAILY_RISK_PCT)
    manager = TradeManager()

    # --- Simulated spot data ---
    spot_df = pd.DataFrame({
        "close": range(1, 50),
        "high": range(2, 51),
        "low": range(0, 49)
    })

    spot_df = add_trend_indicators(spot_df)
    latest = spot_df.iloc[-1]

    regime = detect_market_regime(latest)
    strategy = select_strategy(regime)

    print("Market Regime:", regime)
    print("Selected Strategy:", strategy)

    if strategy == "NO_TRADE" or not risk_guard.can_trade():
        print("No trade allowed today.")
        return

    # --- Simulated options chain ---
    spot_price = 22560
    specs = INDEX_SPECS[INDEX]
    atm = get_atm_strike(spot_price, specs["strike_step"])

    chain = pd.DataFrame([
        {"symbol": "NIFTY22550CE", "strike": atm, "type": "CE", "ltp": 120, "delta": 0.55},
        {"symbol": "NIFTY22600CE", "strike": atm + specs["strike_step"], "type": "CE", "ltp": 80, "delta": 0.35},
        {"symbol": "NIFTY22550PE", "strike": atm, "type": "PE", "ltp": 90, "delta": -0.45},
        {"symbol": "NIFTY22500PE", "strike": atm - specs["strike_step"], "type": "PE", "ltp": 70, "delta": -0.30},
    ])

    # --- Build trade ---
    if strategy == "BULL_CALL_SPREAD":
        trade_def = build_bull_call_spread(chain, atm, specs["strike_step"])
        max_loss = trade_def["max_loss"]
    elif strategy == "BEAR_PUT_SPREAD":
        trade_def = build_bear_put_spread(chain, atm, specs["strike_step"])
        max_loss = trade_def["max_loss"]
    elif strategy == "SHORT_STRANGLE":
        trade_def = build_short_strangle(chain)
        max_loss = trade_def["credit"] * 2
    else:
        return

    lots = calculate_lots(
        capital,
        max_loss,
        specs["lot_size"],
        MAX_DAILY_RISK_PCT
    )

    if lots == 0:
        print("Risk too high. Trade skipped.")
        return

    trade = Trade(
        strategy=trade_def["strategy"],
        legs=trade_def["legs"],
        qty=lots
    )

    manager.open_trade(trade)
    print("Trade opened:", trade.strategy, "Lots:", lots)

    # --- Simulated exit ---
    exit_prices = {
        "NIFTY22550CE": 150,
        "NIFTY22600CE": 100
    }

    manager.close_trade(exit_prices)
    pnl = manager.trade_log[0].pnl
    risk_guard.update_pnl(pnl)

    print("Trade closed. PNL:", pnl)


if __name__ == "__main__":
    main()
