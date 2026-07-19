import joblib
from pathlib import Path

import yfinance as yf
from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from app.ml.feature_engineering import add_features


def train_model(asset="AAPL"):

    # ==========================================
    # Download Historical Data
    # ==========================================

    df = yf.download(
        asset,
        period="5y",
        interval="1d",
        progress=False
    )

    if df.empty:
        raise ValueError("No market data downloaded.")

    df.reset_index(inplace=True)

    # ==========================================
    # Feature Engineering
    # ==========================================

    df = add_features(df)

    # ==========================================
    # Target
    # 1 = Tomorrow closes higher
    # 0 = Tomorrow closes lower
    # ==========================================

    df["Target"] = (
        df["Close"].shift(-1) > df["Close"]
    ).astype(int)

    df = df.iloc[:-1]

    # ==========================================
    # Features
    # ==========================================

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

    X = df[features]
    y = df["Target"]

    # ==========================================
    # Train Test Split
    # ==========================================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        shuffle=False,
        random_state=42
    )

    # ==========================================
    # Model
    # ==========================================

    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        random_state=42,
        eval_metric="logloss"
    )

    print("Training model...")

    model.fit(X_train, y_train)

    print("Training completed.")

    # ==========================================
    # Evaluation
    # ==========================================

    predictions = model.predict(X_test)

    metrics = {

        "accuracy": accuracy_score(y_test, predictions),

        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0
        ),

        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0
        ),

        "f1": f1_score(
            y_test,
            predictions,
            zero_division=0
        ),

        "confusion_matrix": confusion_matrix(
            y_test,
            predictions
        ),

        "feature_importance": model.feature_importances_,

        "feature_names": features

    }

    # ==========================================
    # Save
    # ==========================================

    Path("models").mkdir(exist_ok=True)

    save_path = Path("models") / f"{asset}_xgboost.pkl"

    joblib.dump(model, save_path)

    print(f"Model saved -> {save_path}")

    return model, metrics