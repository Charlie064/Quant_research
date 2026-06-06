class PositionSizer:
    def __init__(self, fraction=1.0):
        self.fraction = fraction


    def get_size(self, cash, price):
        capital = cash * self.fraction
        
        return capital / price