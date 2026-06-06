class StopLossTakeProfit:
    def __init__(self, stop_loss=0.4, take_profit=0.9):
        self.stop = stop_loss
        self.tp = take_profit


    def should_exit(self, position, price):
        entry = position["entry_price"]
        direction = position["direction"]

        if direction == 1:
            stop = price <= entry * (1 - self.stop)
            tp = price >= entry * (1 + self.tp)

        else:
            stop = price >= entry * (1 + self.stop)
            tp = price <= entry * (1 - self.tp)

        return stop or tp