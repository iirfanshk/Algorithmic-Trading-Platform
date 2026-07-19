import pandas as pd
from pathlib import Path

from config.assets import ASSETS


def generate_signals(asset: str):

    input_file = Path(f"data/processed/{asset}/features.csv")

    if not input_file.exists():
        print(f"{asset}: features.csv not found.")
        return

    df = pd.read_csv(input_file)

    scores = []
    confidences = []
    signals = []

    for _, row in df.iterrows():

        score = 0

        # ======================================
        # Trend
        # ======================================

        if row["SMA_20"] > row["SMA_50"]:
            score += 2
        else:
            score -= 2

        if row["EMA_20"] > row["EMA_50"]:
            score += 2
        else:
            score -= 2

        # ======================================
        # Momentum
        # ======================================

        if row["MACD"] > row["Signal_Line"]:
            score += 2
        else:
            score -= 2

        if row["MACD_Histogram"] > 0:
            score += 1
        else:
            score -= 1

        # ======================================
        # RSI
        # ======================================

        rsi = row["RSI_14"]

        if rsi < 30:
            score += 2
        elif rsi < 40:
            score += 1
        elif rsi > 70:
            score -= 2
        elif rsi > 60:
            score -= 1

        # ======================================
        # Bollinger Bands
        # ======================================

        if row["Close"] < row["BB_Lower"]:
            score += 1

        elif row["Close"] > row["BB_Upper"]:
            score -= 1

        # ======================================
        # Volatility Filter
        # ======================================

        if pd.notna(row["Volatility_20"]):

            if row["Volatility_20"] < 0.03:
                score += 1
            else:
                score -= 1

        # ======================================
        # Daily Return Confirmation
        # ======================================

        if pd.notna(row["Daily_Return"]):

            if row["Daily_Return"] > 0:
                score += 1
            else:
                score -= 1

        # ======================================
        # Final Signal
        # ======================================

        if score >= 8:
            signal = "STRONG BUY"

        elif score >= 5:
            signal = "BUY"

        elif score <= -8:
            signal = "STRONG SELL"

        elif score <= -5:
            signal = "SELL"

        else:
            signal = "HOLD"

        confidence = min(round(abs(score) / 12 * 100, 2), 100)

        scores.append(score)
        confidences.append(confidence)
        signals.append(signal)

    df["Score"] = scores
    df["Confidence"] = confidences
    df["Signal"] = signals

    output_file = Path(f"data/processed/{asset}/signals.csv")

    df.to_csv(output_file, index=False)

    print("\n" + "=" * 70)
    print(f"{asset} SIGNALS GENERATED")
    print("=" * 70)

    print(
        df[
            [
                "Date",
                "Close",
                "Score",
                "Confidence",
                "Signal"
            ]
        ].tail(5)
    )

    print(f"\nSaved : {output_file}")


def main():

    print("\n")
    print("=" * 80)
    print("GENERATING TRADING SIGNALS")
    print("=" * 80)

    for asset in ASSETS:
        generate_signals(asset)

    print("\n")
    print("=" * 80)
    print("SIGNAL GENERATION COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()