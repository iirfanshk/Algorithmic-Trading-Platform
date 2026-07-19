import pandas as pd
import numpy as np
from pathlib import Path


class Performance:
    """
    Calculates portfolio performance metrics.
    """

    def __init__(self, portfolio_history):

        self.history = portfolio_history.copy()

    # --------------------------------------------------
    # Calculate Metrics
    # --------------------------------------------------

    def calculate(self):

        if self.history.empty:
            return {}

        history = self.history.copy()

        history["Daily_Return"] = history["Portfolio_Value"].pct_change()

        daily_returns = history["Daily_Return"].dropna()

        initial_value = history["Portfolio_Value"].iloc[0]
        final_value = history["Portfolio_Value"].iloc[-1]

        total_return = ((final_value - initial_value) / initial_value) * 100

        # Annualized Return (CAGR)
        years = len(history) / 252

        if years > 0:
            cagr = (((final_value / initial_value) ** (1 / years)) - 1) * 100
        else:
            cagr = 0

        # Volatility
        if len(daily_returns) > 1:
            volatility = daily_returns.std() * np.sqrt(252) * 100
        else:
            volatility = 0

        # Sharpe Ratio
        risk_free_rate = 0.02

        if daily_returns.std() != 0:
            sharpe = (
                (daily_returns.mean() - (risk_free_rate / 252))
                / daily_returns.std()
            ) * np.sqrt(252)
        else:
            sharpe = 0

        # Maximum Drawdown
        running_max = history["Portfolio_Value"].cummax()

        drawdown = (
            history["Portfolio_Value"] - running_max
        ) / running_max

        max_drawdown = drawdown.min() * 100

        # Best / Worst Day
        if len(daily_returns):

            best_day = daily_returns.max() * 100

            worst_day = daily_returns.min() * 100

        else:

            best_day = 0

            worst_day = 0

        metrics = {

            "Initial Value": round(initial_value, 2),

            "Final Value": round(final_value, 2),

            "Total Return (%)": round(total_return, 2),

            "Annual Return (%)": round(cagr, 2),

            "Sharpe Ratio": round(sharpe, 2),

            "Volatility (%)": round(volatility, 2),

            "Maximum Drawdown (%)": round(max_drawdown, 2),

            "Best Day (%)": round(best_day, 2),

            "Worst Day (%)": round(worst_day, 2)

        }

        return metrics

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    def save(self):

        metrics = self.calculate()

        output = Path("data/backtest")

        output.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(

            metrics.items(),

            columns=["Metric", "Value"]

        )

        output_file = output / "summary.csv"

        df.to_csv(output_file, index=False)

        print("\n")
        print("=" * 70)
        print("PERFORMANCE SUMMARY")
        print("=" * 70)

        print(df)

        print(f"\nSaved : {output_file}")