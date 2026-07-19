import yfinance as yf
from pathlib import Path

from config.assets import ASSETS
from config.settings import START_DATE, END_DATE


def fetch_market_data(symbol: str):
    """
    Download historical market data for a given asset
    and save it under:

    data/raw/<ASSET>/raw.csv
    """

    output_dir = Path(f"data/raw/{symbol}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print(f"Downloading {symbol}...")
    print("=" * 70)

    try:

        df = yf.download(
            symbol,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            print(f"No data found for {symbol}")
            return

        # Flatten MultiIndex columns if necessary
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        output_file = output_dir / "raw.csv"
        df.to_csv(output_file)

        print("DOWNLOAD COMPLETED")
        print("-" * 50)
        print(f"Asset : {symbol}")
        print(f"Rows  : {len(df)}")
        print(f"Saved : {output_file}")
        print(df.tail(3))

    except Exception as e:

        print(f"Error downloading {symbol}")
        print(e)


def main():

    print("\n")
    print("=" * 80)
    print("FETCHING MARKET DATA")
    print("=" * 80)

    for asset in ASSETS:
        fetch_market_data(asset)

    print("\n")
    print("=" * 80)
    print("ALL DOWNLOADS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()