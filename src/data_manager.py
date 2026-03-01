import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import yfinance as yf

class DataManager:
    def __init__(self, ticker="SPY", interval="1d", period="10y"):
        """
        ticker: symbol to download
        interval: Yahoo interval ('1m', '5m', '60m', '1d', '1mo')
        period: period to download ('7d', '60d', '1y', 'max', etc.)
        """
        self.ticker = ticker
        self.interval = interval
        self.period = period

        # Download data
        df = yf.download(
            tickers=self.ticker,
            interval=self.interval,
            period=self.period,
            auto_adjust=True,  # Adjusted close includes splits/dividends
            progress=False
        )

        if df.empty:
            raise ValueError("No data downloaded. Check interval, period and internet connection.")
        
        df = df.ffill() # Fill any small gaps to avoid breaks in backtest

        # Flatten MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        self.data = df
        self.indicators = pd.DataFrame(index=df.index)
        self.required_warmup = 0


    def __str__(self):
        return (
            f"\nDataManager Summary\n"
            f"-------------------\n"
            f"Ticker   : {self.ticker}\n"
            f"Start    : {self.data.index.min()}\n"
            f"End      : {self.data.index.max()}\n"
            f"Rows     : {self.data.shape[0]}\n"
            f"Columns  : {self.data.shape[1]}\n"
        )
    

    # ---------------------------
    # Indicator Methods
    # ---------------------------

    def add_sma(self, window):
        col_name = f"SMA_{window}"
        self.indicators[col_name] = self.data["Close"].rolling(window).mean()
        self.required_warmup = max(self.required_warmup, window)

    # ---------------------------
    # Internal
    # ---------------------------

    def _get_stable_data(self):
        """
        Automatically trims warmup rows.
        """
        if self.required_warmup > 0:
            df = self.data.iloc[self.required_warmup:].copy()
            ind = self.indicators.iloc[self.required_warmup:].copy()
        else:
            df = self.data.copy()
            ind = self.indicators.copy()

        return df, ind
    

    def get_prices(self):
        if "Adj Close" in self.data.columns:
            return self.data["Adj Close"]
        elif "Close" in self.data.columns:
            return self.data["Close"]
        elif "close" in self.data.columns:
            return self.data["close"]
        else:
            raise ValueError("No usable price column found.")


    def get_returns(self):
        prices = self.get_prices()
        return prices.pct_change().dropna()
    

    # ---------------------------
    # Plot
    # ---------------------------

    def plot(self, style="mike"):
        df, ind = self._get_stable_data()

        # Always plot candles
        if ind.empty:
            mpf.plot(
                df,
                type="candle",
                volume=True,
                style=style,
                title=f"{self.ticker} {self.interval}",
                figsize=(10, 5)
            )
            return

        # Build addplots explicitly
        apds = []
        for column in ind.columns:
            apds.append(mpf.make_addplot(ind[column]))

        mpf.plot(
            df,
            type="candle",
            volume=True,
            addplot=apds,
            style=style,
            title=f"{self.ticker} {self.interval}",
            figsize=(10, 5)
        )
    


if __name__ == "__main__":
    pass