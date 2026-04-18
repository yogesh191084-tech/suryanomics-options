from risk.position_sizing import calculate_lots
from risk.risk_guard import DailyRiskGuard

capital = 500000
max_loss_per_lot = 40      # from spread example
lot_size = 50
max_risk_pct = 0.01

lots = calculate_lots(capital, max_loss_per_lot, lot_size, max_risk_pct)
print("Calculated lots:", lots)

guard = DailyRiskGuard(capital, 0.01)
print("Can trade initially:", guard.can_trade())

guard.update_pnl(-3000)
print("After loss, can trade:", guard.can_trade())

guard.update_pnl(-3000)
print("After more loss, can trade:", guard.can_trade())
