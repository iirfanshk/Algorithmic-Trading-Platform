import pandas as pd
import ta


def add_features(df):

    df = df.copy()

    # ---------------------------------------
    # Flatten MultiIndex columns (yfinance)
    # ---------------------------------------

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # ---------------------------------------
    # Convert 2D columns to Series
    # ---------------------------------------

    for col in ["Open", "High", "Low", "Close", "Volume"]:

        if col in df.columns:

            if isinstance(df[col], pd.DataFrame):

                df[col] = df[col].iloc[:, 0]

    # ---------------------------------------
    # Convert numeric
    # ---------------------------------------

    numeric_cols = [

        "Open",

        "High",

        "Low",

        "Close",

        "Volume"

    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------------------------------
    # Moving Averages
    # ---------------------------------------

    df["SMA20"] = ta.trend.sma_indicator(

        close=df["Close"],

        window=20

    )

    df["SMA50"] = ta.trend.sma_indicator(

        close=df["Close"],

        window=50

    )

    df["EMA20"] = ta.trend.ema_indicator(

        close=df["Close"],

        window=20

    )

    # ---------------------------------------
    # RSI
    # ---------------------------------------

    df["RSI"] = ta.momentum.rsi(

        close=df["Close"],

        window=14

    )

    # ---------------------------------------
    # MACD
    # ---------------------------------------

    df["MACD"] = ta.trend.macd(

        close=df["Close"]

    )

    df["MACD_SIGNAL"] = ta.trend.macd_signal(

        close=df["Close"]

    )

    # ---------------------------------------
    # ATR
    # ---------------------------------------

    df["ATR"] = ta.volatility.average_true_range(

        high=df["High"],

        low=df["Low"],

        close=df["Close"],

        window=14

    )

    # ---------------------------------------
    # Returns
    # ---------------------------------------

    df["Returns"] = df["Close"].pct_change()

    # ---------------------------------------
    # Momentum
    # ---------------------------------------

    df["Momentum"] = df["Close"] - df["Close"].shift(10)

    # ---------------------------------------
    # Clean
    # ---------------------------------------

    df = df.dropna().reset_index(drop=True)

    return df