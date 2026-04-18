class DailyRiskGuard:
    def __init__(self, capital, max_daily_risk_pct):
        self.max_daily_loss = capital * max_daily_risk_pct
        self.realized_pnl = 0
        self.locked = False

    def update_pnl(self, pnl):
        self.realized_pnl += pnl
        if self.realized_pnl <= -self.max_daily_loss:
            self.locked = True

    def can_trade(self):
        return not self.locked
