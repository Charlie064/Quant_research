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
        self.data = yf.download(
            tickers=self.ticker,
            interval=self.interval,
            period=self.period,
            auto_adjust=True,  # Adjusted close includes splits/dividends
            progress=False
        )

        if self.data.empty:
            raise ValueError("No data downloaded. Check interval and period.")

        # Fill any small gaps to avoid breaks in backtest
        self.data = self.data.ffill()

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
    

    def plot_candles(self):
        df = self.data.copy()

        # Flatten MultiIndex if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Ensure numeric
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        mpf.plot(
            df,
            type="candle",
            volume=True,
            style="yahoo",
            title=f"{self.ticker} {self.interval}",
            figsize=(10, 5)
        )
    

def example_1():
    dm = DataManager(
        ticker="SPY", 
        interval="1m", 
        period="1d", 
        )
    
    # Get info
    print(dm)

    # See last 5 returns (%)
    returns = dm.get_returns()
    print(returns.tail())
    

if __name__ == "__main__":
    example_1()