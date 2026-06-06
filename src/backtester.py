import pandas as pd
import mplfinance as mpf

class Backtester:

    def __init__(self, data_manager, strategy,
                 risk=None,
                 sizer=None,
                 initial_capital=10000):

        self.dm = data_manager
        self.strategy = strategy
        self.risk = risk
        self.sizer = sizer

        self.initial_capital = initial_capital

        self.cash = initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = None


    def run(self):

        prices = self.dm.get_prices()
        signals = self.strategy.generate_signals()

        equity_curve = pd.Series(index=prices.index, dtype=float)

        for date in prices.index:

            for asset in prices.columns:

                price = prices.loc[date, asset]
                signal = signals.loc[date, asset]

                self._update_position(date, asset, price, signal)

            equity_curve.loc[date] = self._calculate_equity(prices.loc[date])

        self.equity_curve = equity_curve

        return equity_curve
    
    def _update_position(self, date, asset, price, signal):

        position = self.positions.get(asset)

        # EXIT
        if position is not None:

            if self.risk and self.risk.should_exit(position, price):
                self._close_position(date, asset, price)
                return

            if signal == -position["direction"]:
                self._close_position(date, asset, price)
                return

        # ENTRY
        if position is None and signal != 0:

            size = self.sizer.get_size(self.cash, price)

            self.positions[asset] = {
                "entry_date": date,
                "entry_price": price,
                "size": size,
                "direction": signal
            }

            self.cash -= size * price * signal

    
    def _close_position(self, date, asset, price):

        position = self.positions.pop(asset)

        direction = position["direction"]
        size = position["size"]
        entry_price = position["entry_price"]

        pnl = (price - entry_price) * size * direction

        self.cash += size * price * direction

        self.trades.append({
            "asset": asset,
            "entry_date": position["entry_date"],
            "exit_date": date,
            "entry_price": entry_price,
            "exit_price": price,
            "pnl": pnl
        })


    def _calculate_equity(self, price_row):

        equity = self.cash

        for asset, pos in self.positions.items():

            price = price_row[asset]

            equity += pos["size"] * price * pos["direction"]

        return equity
                