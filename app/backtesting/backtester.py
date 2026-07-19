import pandas as pd
from pathlib import Path

print(">>> NEW BACKTESTER LOADED <<<")

from config.assets import ASSETS
from config.settings import INITIAL_CAPITAL

from app.backtesting.execution_engine import ExecutionEngine
from app.backtesting.trade_manager import TradeManager
from app.backtesting.portfolio_tracker import PortfolioTracker
from app.backtesting.performance import Performance
from app.backtesting.portfolio_state import PortfolioState


class Backtester:

    """
    Multi-Asset Backtesting Engine

    Responsibilities
    ----------------
    - Load historical signals
    - Simulate trades
    - Track portfolio
    - Record trades
    - Generate performance report
    """

    def __init__(self):

        self.execution = ExecutionEngine()

        self.trade_manager = TradeManager()

        self.portfolio_tracker = PortfolioTracker()

        self.portfolio = PortfolioState(
            INITIAL_CAPITAL
        )

        self.market_data = {}

        self.all_dates = []

    # -------------------------------------------------
    # LOAD DATA
    # -------------------------------------------------

    def load_data(self):

        print("\nLoading historical signals...\n")

        for asset in ASSETS:

            file = Path(
                f"data/processed/{asset}/signals.csv"
            )

            if not file.exists():

                print(f"{asset} skipped.")
                continue

            df = pd.read_csv(file)

            df["Date"] = pd.to_datetime(df["Date"])

            df = df.sort_values("Date")

            self.market_data[asset] = df

        dates = set()

        for df in self.market_data.values():

            dates.update(df["Date"])

        self.all_dates = sorted(list(dates))

        print(
            f"\nLoaded {len(self.market_data)} assets."
        )

        print(
            f"Trading Days : {len(self.all_dates)}"
        )
        # -------------------------------------------------
    # RUN BACKTEST
    # -------------------------------------------------

    def run(self):

        self.load_data()

        print("\nStarting Backtest...\n")

        for current_date in self.all_dates:

            # Keep last known market price for every asset
            if not hasattr(self, "latest_prices"):
                self.latest_prices = {}

            for asset, df in self.market_data.items():

                row = df[df["Date"] == current_date]

                if not row.empty:
                    self.latest_prices[asset] = row.iloc[0]["Close"]

            prices = self.latest_prices.copy()

            # -----------------------------------------
            # Execute Signals
            # -----------------------------------------

            for asset, df in self.market_data.items():

                row = df[df["Date"] == current_date]

                if row.empty:
                    continue

                row = row.iloc[0]

                signal = row["Signal"]

                price = row["Close"]

                # BUY
                if (
                    signal in ["BUY", "STRONG BUY"]
                    and asset not in self.portfolio.positions
                    and self.portfolio.cash > 0
                ):

                    allocation = self.portfolio.cash * 0.20

                    trade = self.execution.buy(
                        allocation,
                        price
                    )

                    if trade["success"]:

                        self.portfolio.buy(
                            asset,
                            trade["shares"],
                            price
                        )

                        self.trade_manager.record_trade(

                            date=current_date,

                            asset=asset,

                            trade_type="BUY",

                            price=price,

                            shares=trade["shares"],

                            commission=trade["commission"],

                            cash_after_trade=self.portfolio.cash

                        )

                # SELL
                elif (

                    signal in ["SELL", "STRONG SELL"]

                    and asset in self.portfolio.positions

                ):

                    shares = self.portfolio.positions[asset]

                    trade = self.execution.sell(
                        shares,
                        price
                    )

                    if trade["success"]:

                        self.portfolio.sell(
                            asset,
                            price
                        )

                        self.trade_manager.record_trade(

                            date=current_date,

                            asset=asset,

                            trade_type="SELL",

                            price=price,

                            shares=shares,

                            commission=trade["commission"],

                            cash_after_trade=self.portfolio.cash

                        )

            # -----------------------------------------
            # Portfolio Snapshot
            # -----------------------------------------

            holdings = self.portfolio.holdings_value(
                prices
            )

            self.portfolio_tracker.record(

                date=current_date,

                cash=self.portfolio.cash,

                holdings_value=holdings

            )
        # -------------------------------------------------
    # SAVE RESULTS
    # -------------------------------------------------

    def save_results(self):

        self.trade_manager.save()

        self.portfolio_tracker.save()

        history = self.portfolio_tracker.get_history()

        performance = Performance(history)

        performance.save()

        print("\n" + "=" * 70)
        print("BACKTEST COMPLETED")
        print("=" * 70)

        print("\nFinal Portfolio Summary:\n")

        print(self.portfolio.summary())

    # -------------------------------------------------
    # EXECUTE
    # -------------------------------------------------

    def execute(self):

        self.run()

        self.save_results()
if __name__ == "__main__":

    backtester = Backtester()

    backtester.execute()