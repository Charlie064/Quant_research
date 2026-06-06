import pandas as pd

class Strategy:
    def __init__(self, data_manager):
        self.dm = data_manager
        self.signals = pd.DataFrame(0, index=self.dm.data.index, columns=[self.dm.ticker])
        self.name = self.__class__.__name__

    def generate_signals(self):
        """Compute buy/sell signals (1 = buy, -1 = sell, 0 = hold)"""
        raise NotImplementedError