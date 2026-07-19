import pandas as pd
from pathlib import Path


class PortfolioTracker:
    """
    Tracks the portfolio value over time.

    Responsibilities
    ----------------
    - Track cash
    - Track holdings
    - Track portfolio value
    - Save portfolio history
    """

    def __init__(self):

        self.history = []

    # ---------------------------------------------------
    # Record Portfolio Snapshot
    # ---------------------------------------------------

    def record(
        self,
        date,
        cash,
        holdings_value
    ):

        total_value = cash + holdings_value

        self.history.append({

            "Date": date,
            "Cash": round(cash, 2),
            "Holdings": round(holdings_value, 2),
            "Portfolio_Value": round(total_value, 2)

        })

    # ---------------------------------------------------
    # Return DataFrame
    # ---------------------------------------------------

    def get_history(self):

        if len(self.history) == 0:
            return pd.DataFrame()

        return pd.DataFrame(self.history)

    # ---------------------------------------------------
    # Save Portfolio History
    # ---------------------------------------------------

    def save(self):

        output_dir = Path("data/backtest")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "portfolio_history.csv"

        history = self.get_history()

        history.to_csv(
            output_file,
            index=False
        )

        print("\n")
        print("=" * 70)
        print("PORTFOLIO HISTORY SAVED")
        print("=" * 70)

        print(history.tail())

        print(f"\nSaved : {output_file}")