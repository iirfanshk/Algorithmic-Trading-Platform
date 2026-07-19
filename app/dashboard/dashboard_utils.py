import pandas as pd
from pathlib import Path


def load_data():

    base_path = Path("data/processed/AAPL")

    signals = pd.read_csv(base_path / "signals.csv")
    backtest = pd.read_csv(base_path / "backtest.csv")

    signals["Date"] = pd.to_datetime(signals["Date"])
    backtest["Date"] = pd.to_datetime(backtest["Date"])

    return signals, backtest