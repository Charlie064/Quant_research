import numpy as np


class MonteCarlo:
    def __init__(self, initial_capital=100_000):
        self.initial_capital = initial_capital


    def _generate_returns(self, shape, winrate, reward, risk):
        wins = np.random.rand(*shape) < winrate # Boolean mask where True is winning trade
        returns = np.where(wins, risk * reward, -risk)
        return returns

    def simulate_run(self, n_trades=100, winrate=0.5, reward=2, risk=0.01):
        """
        n_trades (int): number of trades
        winrate (float): probability of win 0 - 1.0
        reward (float): factor by which the risked capital changes e.g. 0.8, 1.2...
        risk (float): risked amount of capital e.g 1% means risk=0.01 
        """

        returns = self._generate_returns(n_trades, winrate, reward, risk)
        factors = 1 + returns

        # Compute equity curve
        equity = self.initial_capital * np.cumprod(factors)

        # Prepend starting capital
        equity = np.insert(equity, 0, self.initial_capital)

        return equity


    def run_monte_carlo(
        self,
        n_runs=10000,
        n_trades=100,
        winrate=0.5,
        reward=2,
        risk=0.01
    ):

        returns = self._generate_returns((n_runs, n_trades), winrate, reward, risk)
        factors = 1 + returns
        
        equity = self.initial_capital * np.cumprod(factors, axis=1)

        # Prepend every run (row) with initial capital value.
        equity = np.hstack([
            np.full((n_runs, 1), self.initial_capital),
            equity
        ])

        return equity


    def compute_metrics(self, equity):
        final_equity = equity[:, -1]

        peaks = np.maximum.accumulate(equity, axis=1)
        drawdowns = (equity - peaks) / peaks
        max_dd = np.min(drawdowns, axis=1)

        metrics = {
            "mean_final_equity": np.mean(final_equity),
            "median_final_equity": np.median(final_equity),
            "worst_drawdown": np.min(max_dd),
            "median_drawdown": np.median(max_dd),
            "probability_of_loss": np.mean(final_equity < self.initial_capital)
        }

        return metrics