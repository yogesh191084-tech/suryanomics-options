from engine.trade import Trade
from engine.trade_manager import TradeManager

legs = [
    {"action": "BUY", "symbol": "NIFTY22550CE", "price": 120},
    {"action": "SELL", "symbol": "NIFTY22600CE", "price": 80}
]

trade = Trade(
    strategy="BULL_CALL_SPREAD",
    legs=legs,
    qty=2
)

manager = TradeManager()
manager.open_trade(trade)

exit_prices = {
    "NIFTY22550CE": 150,
    "NIFTY22600CE": 100
}

manager.close_trade(exit_prices)

print("PNL:", manager.trade_log[0].pnl)
print("Status:", manager.trade_log[0].status)
