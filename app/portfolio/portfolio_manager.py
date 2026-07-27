import pandas as pd
from pathlib import Path

from config.assets import ASSETS
from config.settings import INITIAL_CAPITAL


def get_priority(signal):

    priorities = {
        "STRONG BUY": 5,
        "BUY": 4,
        "HOLD": 3,
        "SELL": 2,
        "STRONG SELL": 1
    }

    return priorities.get(signal, 0)


def build_portfolio():

    portfolio = []

    for asset in ASSETS:

        signal_file = Path(f"data/processed/{asset}/signals.csv")

        if not signal_file.exists():
            print(f"{asset}: signals.csv not found.")
            continue

        df = pd.read_csv(signal_file)

        latest = df.iloc[-1]

        portfolio.append({

            "Asset": asset,
            "Close": latest["Close"],
            "Signal": latest["Signal"],
            "Score": latest["Score"],
            "Confidence": latest["Confidence"],
            "Priority": get_priority(latest["Signal"]),
            "RSI": round(latest["RSI_14"], 2),
            "MACD": round(latest["MACD"], 4)

        })

    portfolio = pd.DataFrame(portfolio)

    if portfolio.empty:
        print("No assets available.")
        return

    portfolio = portfolio.sort_values(
        by=["Priority", "Score", "Confidence"],
        ascending=False
    ).reset_index(drop=True)

    portfolio["Allocation (%)"] = 0.0
    portfolio["Capital"] = 0.0

    buy_assets = portfolio[
        portfolio["Signal"].isin(
            ["BUY", "STRONG BUY"]
        )
    ].copy()

    if not buy_assets.empty:

        total_confidence = buy_assets["Confidence"].sum()

        for idx in buy_assets.index:

            allocation = (
                buy_assets.loc[idx, "Confidence"]
                / total_confidence
            ) * 100

            portfolio.loc[idx, "Allocation (%)"] = round(allocation, 2)

            portfolio.loc[idx, "Capital"] = round(
                allocation
                / 100
                * INITIAL_CAPITAL,
                2
            )

    output_dir = Path("data/portfolio")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "portfolio.csv"

    portfolio.to_csv(output_file, index=False)

    print("\n")
    print("=" * 100)
    print("TODAY'S PORTFOLIO")
    print("=" * 100)
    print(portfolio)
    print("=" * 100)

    print(f"\nSaved : {output_file}")


def main():

    print("\n")
    print("=" * 80)
    print("BUILDING PORTFOLIO")
    print("=" * 80)

    build_portfolio()

    print("\n")
    print("=" * 80)
    print("PORTFOLIO CREATED")
    print("=" * 80)


if __name__ == "__main__":
    main()