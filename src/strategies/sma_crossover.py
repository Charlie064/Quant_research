import pandas as pd
from strategies.strategy import Strategy

class SMACrossover(Strategy):
    """
    Simple Moving Average Crossover strategy.

    Buy when short SMA crosses above long SMA.
    Sell when short SMA crosses below long SMA.
    """
    def __init__(self, dm, short_window=20, long_window=50, cross_only=True):
        super().__init__(dm)
        self.short_window = short_window
        self.long_window = long_window
        self.cross_only = cross_only

        # Add SMAs if not already present
        if f"SMA_{short_window}" not in self.dm.indicators[self.dm.ticker].columns:
            self.dm.add_sma(short_window)
        if f"SMA_{long_window}" not in self.dm.indicators[self.dm.ticker].columns:
            self.dm.add_sma(long_window)


    def generate_signals(self):
        df = self.dm.data
        signals = pd.DataFrame(0, index=df.index, columns=self.dm.tickers)

        for ticker in self.dm.tickers:
            short = self.dm.indicators[ticker][f"SMA_{self.short_window}"]
            long = self.dm.indicators[ticker][f"SMA_{self.long_window}"]

            if self.cross_only:
                cross_up = (short > long) & (short.shift(1) <= long.shift(1))
                cross_down = (short < long) & (short.shift(1) >= long.shift(1))
                signals.loc[cross_up, ticker] = 1
                signals.loc[cross_down, ticker] = -1
            else:
                signals.loc[short > long, ticker] = 1
                signals.loc[short < long, ticker] = -1
                            
        self.signals = signals.fillna(0)
        return self.signals