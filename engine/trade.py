from datetime import datetime
from datetime import datetime

class Trade:
    def __init__(self, strategy, legs, qty, entry_time=None):
        self.strategy = strategy
        self.legs = legs
        self.qty = qty
        self.entry_time = entry_time or datetime.now()
        self.exit_time = None
        self.status = "OPEN"
        self.entry_value = self._calculate_entry_value()
        self.exit_value = None
        self.pnl = 0

    def _calculate_entry_value(self):
        value = 0
        for leg in self.legs:
            if leg["action"] == "BUY":
                value -= leg["price"]
            else:
                value += leg["price"]
        return value * self.qty

    def update_exit(self, prices):
        """
        prices: dict {symbol: ltp}
        """
        value = 0
        for leg in self.legs:
            ltp = prices.get(leg["symbol"], leg["price"])
            if leg["action"] == "BUY":
                value += ltp
            else:
                value -= ltp

        self.exit_value = value * self.qty
        self.pnl = self.exit_value + self.entry_value
        self.exit_time = datetime.now()
        self.status = "CLOSED"
