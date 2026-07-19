from app.ml.predict import predict_signal

import yfinance as yf
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot


def get_model_prediction(asset):

    signal, confidence = predict_signal(asset)

    # =========================================
    # Model Not Available
    # =========================================

    if signal == "MODEL_NOT_AVAILABLE":

        return {

            "signal": "N/A",

            "confidence": 0,

            "risk": "N/A",

            "trend": "N/A",

            "recommendation":
                "No trained AI model is available for this asset yet.",

            "reasons": [

                "Model has not been trained.",

                "Train an XGBoost model for this asset.",

                "Currently supported assets are those with trained models."

            ]

        }

    confidence = round(confidence * 100, 2)
    
    # =========================================
    # Live Market Data
    # =========================================

    try:

        data = yf.download(asset, period="3mo", progress=False, auto_adjust=False)

        close = data["Close"]

        if hasattr(close, "columns"):
            close = close.iloc[:, 0]

        current_price = round(float(close.iloc[-1]), 2)

        returns = close.pct_change().dropna()

        volatility = round(float(returns.std() * 100), 2)

        expected_move = round(volatility * 1.5, 2)
        
        print(data.head())
        print(data.columns)
        
        close = data["Close"]
        open_ = data["Open"]
        high = data["High"]
        low = data["Low"]

        if hasattr(close, "columns"):
            close = close.iloc[:, 0]
            open_ = open_.iloc[:, 0]
            high = high.iloc[:, 0]
            low = low.iloc[:, 0]

        fig = go.Figure()

        fig.add_trace(

            go.Candlestick(

                x=data.index.to_list(),

                open=open_.to_list(),

                high=high.to_list(),

                low=low.to_list(),

                close=close.to_list(),

                name="Price"

            )

        )

        fig.update_layout(

            template="plotly_dark",

            height=500,

            margin=dict(l=10, r=10, t=10, b=10),

            xaxis_rangeslider_visible=False

        )

        chart = plot(
            fig,
            output_type="div",
            include_plotlyjs=False
        )

    except Exception as e:

        print("Market Data Error:", e)

        current_price = 0

        volatility = 0

        expected_move = 0

    # =========================================
    # Trend
    # =========================================

    trend = "Bullish" if signal == "BUY" else "Bearish"

    # =========================================
    # Risk
    # =========================================

    if confidence >= 85:
        risk = "Low"

    elif confidence >= 70:
        risk = "Medium"

    else:
        risk = "High"

    # =========================================
    # Recommendation
    # =========================================

    if signal == "BUY":

        recommendation = (
            "Consider buying or accumulating the asset."
        )

        reasons = [

            "Momentum indicators are positive.",

            "Trend is currently bullish.",

            "AI model predicts upward movement.",

            "Technical indicators support buying."

        ]

    else:

        recommendation = (
            "Avoid new positions or consider reducing exposure."
        )

        reasons = [

            "Momentum has weakened.",

            "Trend is currently bearish.",

            "AI model predicts downward movement.",

            "Technical indicators suggest caution."

        ]

    return {

        "signal": signal,

        "confidence": confidence,

        "risk": risk,

        "trend": trend,

        "recommendation": recommendation,

        "reasons": reasons,

        "current_price": current_price,

        "expected_move": expected_move,

        "volatility": volatility,
        
        "chart": chart,

    }