import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd


def plot_candles(dm, ticker=None, add_indicators = False, add_equity=None, style="mike", figsize=(12, 9)):
    """
    Plot candlestick chart for a given ticker, with indicators and optional equity curve.
    """

    if ticker is None:
        ticker = dm.ticker

    if ticker not in dm.tickers:
        raise ValueError(f"{ticker} not in DataManager.tickers")

    # Trim warmup rows
    if dm.required_warmup > 0:
        df = dm.data.iloc[dm.required_warmup:].copy()
        indicators = dm.indicators[ticker].iloc[dm.required_warmup:].copy()
    else:
        df = dm.data.copy()
        indicators = dm.indicators[ticker].copy()

    # Ensure df has OHLC columns
    required_cols = ["Open", "High", "Low", "Close"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' missing in data for plotting")


    # Additional plots
    apds = []

    # Optional: Prepare addplots for indicators
    if add_indicators:
        for col in indicators.columns:
            apds.append(mpf.make_addplot(indicators[col], panel=0, color='orange'))

    # Optional: add equity as a separate panel
    if add_equity is not None:

        # Convert to Series if needed
        if isinstance(add_equity, pd.DataFrame):
            add_equity = add_equity.squeeze()

        # Trim warmup rows so lengths match
        if dm.required_warmup > 0:
            add_equity = add_equity.iloc[dm.required_warmup:]

        # Align index to price dataframe
        add_equity = add_equity.reindex(df.index)

        apds.append(
            mpf.make_addplot(
                add_equity,
                panel=2,
                color="blue",
                secondary_y=False,
                ylabel="Equity"
            )
        )


    # Call mplfinance.plot with or without addplot
    if apds:
        mpf.plot(
            df,
            type="candle",
            volume=True,
            addplot=apds,
            style=style,
            figsize=figsize,
            title=f"{ticker} Candles + Indicators"
        )
    else:
        mpf.plot(
            df,
            type="candle",
            volume=True,
            style=style,
            figsize=figsize,
            title=f"{ticker} Candles"
        )