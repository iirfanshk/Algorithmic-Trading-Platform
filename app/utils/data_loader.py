import pandas as pd
from pathlib import Path


class DataLoader:
    """
    Loads all backtesting output files safely.

    Files:
    - summary.csv
    - portfolio_history.csv
    - trade_history.csv
    """

    BASE_PATH = Path("data/backtest")

    @staticmethod
    def load_summary():

        file = DataLoader.BASE_PATH / "summary.csv"

        if file.exists():

            return pd.read_csv(file)

        return pd.DataFrame()

    @staticmethod
    def load_portfolio():

        file = DataLoader.BASE_PATH / "portfolio_history.csv"

        if file.exists():

            return pd.read_csv(file)

        return pd.DataFrame()

    @staticmethod
    def load_trades():

        file = DataLoader.BASE_PATH / "trade_history.csv"

        if file.exists():

            return pd.read_csv(file)

        return pd.DataFrame()

    @staticmethod
    def metrics():

        summary = DataLoader.load_summary()

        if summary.empty:

            return {}

        return dict(

            zip(

                summary["Metric"],

                summary["Value"]

            )

        )