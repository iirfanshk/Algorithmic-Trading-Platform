import pandas as pd
from pathlib import Path


class TradeManager:
    """
    Stores every executed trade.

    Responsibilities
    ----------------
    - Record BUY trades
    - Record SELL trades
    - Export trade history
    """

    def __init__(self):

        self.trades = []

    # ---------------------------------------------------
    # Record Trade
    # ---------------------------------------------------

    def record_trade(
        self,
        date,
        asset,
        trade_type,
        price,
        shares,
        commission,
        cash_after_trade
    ):

        trade = {

            "Date": date,
            "Asset": asset,
            "Type": trade_type,
            "Price": round(price, 2),
            "Shares": round(shares, 6),
            "Commission": round(commission, 2),
            "Cash": round(cash_after_trade, 2)

        }

        self.trades.append(trade)

    # ---------------------------------------------------
    # Get Trade History
    # ---------------------------------------------------

    def get_trade_history(self):

        if len(self.trades) == 0:
            return pd.DataFrame()

        return pd.DataFrame(self.trades)

    # ---------------------------------------------------
    # Save Trade History
    # ---------------------------------------------------

    def save(self):

        output_dir = Path("data/backtest")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "trade_history.csv"

        history = self.get_trade_history()

        history.to_csv(
            output_file,
            index=False
        )

        print("\n")
        print("=" * 70)
        print("TRADE HISTORY SAVED")
        print("=" * 70)

        print(history)

        print(f"\nSaved : {output_file}")