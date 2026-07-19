import joblib
import yfinance as yf
from pathlib import Path

from app.ml.feature_engineering import add_features


def predict_signal(asset="AAPL"):

    model_path = Path("models") / f"{asset}_xgboost.pkl"

    # ----------------------------------------
    # Model not trained yet
    # ----------------------------------------

    if not model_path.exists():

        return (
            "MODEL_NOT_AVAILABLE",
            0.0
        )

    model = joblib.load(model_path)

    # ----------------------------------------
    # Download latest market data
    # ----------------------------------------

    df = yf.download(
        asset,
        period="6mo",
        interval="1d",
        progress=False
    )

    if df.empty:

        return (
            "MODEL_NOT_AVAILABLE",
            0.0
        )

    df.reset_index(inplace=True)

    df = add_features(df)

    features = [

        "SMA20",
        "SMA50",
        "EMA20",
        "RSI",
        "MACD",
        "MACD_SIGNAL",
        "ATR",
        "Returns",
        "Momentum"

    ]

    X = df[features].tail(1)

    prediction = model.predict(X)[0]

    probability = float(model.predict_proba(X)[0].max())

    signal = "BUY" if prediction == 1 else "SELL"

    return signal, probability