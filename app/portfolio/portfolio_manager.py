import pandas as pd
from pathlib import Path

INITIAL_CAPITAL = 100000

ASSETS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "TSLA",
    "AMZN",
    "GOOGL",
    "META",
    "SPY",
    "QQQ",
    "DIA",
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "GC=F",
    "SI=F",
    "CL=F"
]


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
            print(f"{asset} signals not found.")
            continue

        df = pd.read_csv(signal_file)

        latest = df.iloc[-1]

        signal = latest["Signal"]
        score = latest["Score"]

        priority = get_priority(signal)

        confidence = min(abs(score) / 10 * 100, 100)

        portfolio.append({
            "Asset": asset,
            "Close": latest["Close"],
            "Signal": signal,
            "Score": score,
            "Priority": priority,
            "Confidence (%)": round(confidence, 2),
            "RSI": round(latest["RSI_14"], 2),
            "MACD": round(latest["MACD"], 4)
        })

    portfolio = pd.DataFrame(portfolio)

    portfolio = portfolio.sort_values(
        by=["Priority", "Score"],
        ascending=False
    ).reset_index(drop=True)

    portfolio["Allocation (%)"] = 0.0
    portfolio["Capital Allocation"] = 0.0

    buy_assets = portfolio[
        portfolio["Signal"].isin(
            ["BUY", "STRONG BUY"]
        )
    ]

    if not buy_assets.empty:

        allocation = round(100 / len(buy_assets), 2)

        portfolio.loc[
            portfolio["Signal"].isin(["BUY", "STRONG BUY"]),
            "Allocation (%)"
        ] = allocation

        portfolio.loc[
            portfolio["Signal"].isin(["BUY", "STRONG BUY"]),
            "Capital Allocation"
        ] = (
            INITIAL_CAPITAL
            * allocation
            / 100
        )

    output_dir = Path("data/portfolio")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "portfolio.csv"

    portfolio.to_csv(output_file, index=False)

    print("\n")
    print("=" * 80)
    print("TODAY'S PORTFOLIO")
    print("=" * 80)
    print(portfolio)
    print("=" * 80)

    print(f"\nPortfolio saved to: {output_file}")


if __name__ == "__main__":
    build_portfolio()