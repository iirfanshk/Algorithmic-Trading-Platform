import pandas as pd
from pathlib import Path


def analyze_performance():

    file_path = Path("data/processed/AAPL_backtest.csv")

    df = pd.read_csv(file_path)

    # Daily Returns
    df["Daily_Return"] = df["Portfolio_Value"].pct_change()

    # Total Return
    total_return = (
        (df["Portfolio_Value"].iloc[-1] - df["Portfolio_Value"].iloc[0])
        / df["Portfolio_Value"].iloc[0]
    ) * 100

    # Maximum Portfolio Value
    rolling_max = df["Portfolio_Value"].cummax()

    # Drawdown
    drawdown = (
        (df["Portfolio_Value"] - rolling_max)
        / rolling_max
    )

    max_drawdown = drawdown.min() * 100

    # Volatility
    volatility = df["Daily_Return"].std() * (252 ** 0.5) * 100

    # Sharpe Ratio
    sharpe_ratio = (
        df["Daily_Return"].mean()
        /
        df["Daily_Return"].std()
    ) * (252 ** 0.5)

    print("=" * 60)
    print("PERFORMANCE REPORT")
    print("=" * 60)

    print(f"Total Return      : {total_return:.2f}%")
    print(f"Maximum Drawdown  : {max_drawdown:.2f}%")
    print(f"Annual Volatility : {volatility:.2f}%")
    print(f"Sharpe Ratio      : {sharpe_ratio:.2f}")


if __name__ == "__main__":
    analyze_performance()