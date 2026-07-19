import pandas as pd
from pathlib import Path

from config.assets import ASSETS


def calculate_indicators(symbol: str):
    """
    Generate technical indicators for a given asset and save them as
    data/processed/<ASSET>/features.csv
    """

    input_file = Path(f"data/processed/{symbol}/clean.csv")

    if not input_file.exists():
        print(f"Clean dataset not found for {symbol}")
        return

    output_dir = Path(f"data/processed/{symbol}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "features.csv"

    try:

        df = pd.read_csv(input_file)

        df["Date"] = pd.to_datetime(df["Date"])

        # ======================================================
        # Trend Indicators
        # ======================================================

        df["SMA_20"] = df["Close"].rolling(20).mean()
        df["SMA_50"] = df["Close"].rolling(50).mean()

        df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
        df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()

        # ======================================================
        # RSI (14)
        # ======================================================

        delta = df["Close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        df["RSI_14"] = 100 - (100 / (1 + rs))

        # ======================================================
        # MACD
        # ======================================================

        df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
        df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()

        df["MACD"] = df["EMA_12"] - df["EMA_26"]

        df["Signal_Line"] = (
            df["MACD"]
            .ewm(span=9, adjust=False)
            .mean()
        )

        df["MACD_Histogram"] = (
            df["MACD"] - df["Signal_Line"]
        )

        # ======================================================
        # Bollinger Bands
        # ======================================================

        df["BB_Middle"] = df["Close"].rolling(20).mean()

        rolling_std = df["Close"].rolling(20).std()

        df["BB_Upper"] = df["BB_Middle"] + (2 * rolling_std)
        df["BB_Lower"] = df["BB_Middle"] - (2 * rolling_std)

        # ======================================================
        # Future ML Features (NEW)
        # ======================================================

        df["Daily_Return"] = df["Close"].pct_change()

        df["Volatility_20"] = (
            df["Daily_Return"]
            .rolling(20)
            .std()
        )

        df["Price_Change"] = df["Close"].diff()

        df["High_Low_Spread"] = (
            df["High"] - df["Low"]
        )

        df["Volume_Change"] = (
            df["Volume"].pct_change()
        )

        # ======================================================
        # Save
        # ======================================================

        df.to_csv(output_file, index=False)

        print("\n" + "=" * 70)
        print(f"{symbol} FEATURES GENERATED")
        print("=" * 70)
        print(df.tail(3))
        print(f"\nSaved : {output_file}")

    except Exception as e:

        print(f"\nError processing {symbol}")
        print(e)


def main():

    print("\n")
    print("=" * 80)
    print("GENERATING TECHNICAL INDICATORS")
    print("=" * 80)

    for asset in ASSETS:
        calculate_indicators(asset)

    print("\n")
    print("=" * 80)
    print("FEATURE ENGINEERING COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()