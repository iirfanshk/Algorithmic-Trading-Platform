import pandas as pd
from pathlib import Path


def preprocess_data(symbol: str):
    """
    Clean and preprocess market data for any asset.
    """

    input_file = Path(f"data/raw/{symbol}/raw.csv")

    output_dir = Path(f"data/processed/{symbol}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "clean.csv"

    # Check file exists
    if not input_file.exists():
        print(f"\n{symbol}: Raw data not found.")
        return

    # Load data
    df = pd.read_csv(input_file)

    # ----------------------------
    # Flatten columns if necessary
    # ----------------------------
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # ----------------------------
    # Remove duplicate rows
    # ----------------------------
    df.drop_duplicates(inplace=True)

    # ----------------------------
    # Remove missing values
    # ----------------------------
    df.dropna(inplace=True)

    # ----------------------------
    # Convert Date
    # ----------------------------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # ----------------------------
    # Reset index
    # ----------------------------
    df.reset_index(drop=True, inplace=True)

    # ----------------------------
    # Save cleaned dataset
    # ----------------------------
    df.to_csv(output_file, index=False)

    print("=" * 60)
    print(f"{symbol} PREPROCESSED")
    print("=" * 60)
    print(f"Rows: {len(df)}")
    print(f"Saved: {output_file}")


if __name__ == "__main__":

    assets = [
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

    for asset in assets:
        preprocess_data(asset)