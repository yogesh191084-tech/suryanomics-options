class TradeManager:
    def __init__(self):
        self.active_trade = None
        self.trade_log = []

    def open_trade(self, trade):
        self.active_trade = trade

    def close_trade(self, prices):
        self.active_trade.update_exit(prices)
        self.trade_log.append(self.active_trade)
        self.active_trade = None
