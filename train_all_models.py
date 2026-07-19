from app.ml.train_model import train_model

assets = [

    # =====================
    # Stocks
    # =====================

    "AAPL",
    "AMZN",
    "GOOGL",
    "META",
    "MSFT",
    "NVDA",
    "TSLA",

    # =====================
    # Crypto
    # =====================

    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "BNB-USD",
    "XRP-USD",

    # =====================
    # Forex
    # =====================

    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "USDINR=X",

    # =====================
    # Indices
    # =====================

    "^GSPC",
    "^IXIC",
    "^DJI",
    "^NSEI",
    "^NSEBANK",

    # =====================
    # Commodities
    # =====================

    "GC=F",
    "SI=F",
    "CL=F",
    "NG=F"

]

for asset in assets:

    print(f"\nTraining {asset}...")

    try:
        train_model(asset)
        print(f"✅ {asset} completed")

    except Exception as e:
        print(f"❌ {asset}: {e}")

print("\n🎉 All models trained successfully.")