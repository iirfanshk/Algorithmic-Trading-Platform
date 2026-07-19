import joblib
import numpy as np
import pandas as pd
import yfinance as yf
from pathlib import Path

from app.ml.feature_engineering import add_features


def run_backtest(
    asset,
    strategy,
    capital,
    start_date,
    end_date
):

    # ==========================================
    # Download Historical Data
    # ==========================================

    df = yf.download(
        asset,
        start=start_date,
        end=end_date,
        progress=False
    )

    if df.empty:
        return {
            "success": False,
            "message": "No historical data found."
        }

    df.reset_index(inplace=True)

    # ==========================================
    # Feature Engineering
    # ==========================================

    df = add_features(df)

    # ==========================================
    # Load Model
    # ==========================================

    model_path = Path("models") / f"{asset}_xgboost.pkl"

    if not model_path.exists():
        return {
            "success": False,
            "message": f"Model for {asset} not found."
        }

    model = joblib.load(model_path)

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

    # ==========================================
    # Predictions
    # ==========================================

    df["Prediction"] = model.predict(X)
    
    # ==========================================
    # Prediction Probability
    # ==========================================

    probabilities = model.predict_proba(X)

    df["Confidence"] = probabilities.max(axis=1)

    # Shift predictions one day forward
    df["Prediction"] = df["Prediction"].shift(1)

    df = df.dropna().reset_index(drop=True)

    # ==========================================
    # Confidence Filter
    # ==========================================

    BUY_THRESHOLD = 0.75

    signals = []

    for pred, conf in zip(df["Prediction"], df["Confidence"]):

        if pred == 1 and conf >= BUY_THRESHOLD:
            signals.append("BUY")

        elif pred == 0 and conf >= BUY_THRESHOLD:
            signals.append("SELL")

        else:
            signals.append("HOLD")

    df["Signal"] = signals

    print("\nPrediction")
    print(df["Prediction"].value_counts())

    print("\nSignal")
    print(df["Signal"].value_counts())

    # ==========================================
    # Portfolio Variables
    # ==========================================

    initial_capital = float(capital)
    TRANSACTION_COST = 0.001      # 0.10%
    SLIPPAGE = 0.0005             # 0.05%
    
    STOP_LOSS = 0.05      # 5%
    TAKE_PROFIT = 0.10    # 10%

    cash = initial_capital

    shares = 0.0

    in_position = False

    buy_price = 0.0
    
    # ==========================================
    # Trading Costs
    # ==========================================

    COMMISSION = 0.001      # 0.10%
    SLIPPAGE = 0.0005       # 0.05% 
    STOP_LOSS = 0.05
    TAKE_PROFIT = 0.10

    equity_curve = []

    trades = []

    wins = 0

    total_trades = 0

    # ==========================================
    # Portfolio Simulation
    # ==========================================

    for _, row in df.iterrows():

        price = float(row["Close"])

        signal = row["Signal"]

        date = str(row["Date"])[:10]
        
        # ==========================================
        # Stop Loss / Take Profit
        # ==========================================

        if in_position:

            if price <= buy_price * (1 - STOP_LOSS):

                signal = "SELL"

            elif price >= buy_price * (1 + TAKE_PROFIT):

                signal = "SELL"

        # ---------------- BUY ----------------

        if signal == "BUY" and not in_position:

            execution_price = price * (1 + SLIPPAGE)

            cash_after_commission = cash * (1 - COMMISSION)

            shares = cash_after_commission / execution_price

            buy_price = execution_price

            cash = 0

            in_position = True

            trades.append({
                "date": date,
                "signal": "BUY",
                "price": round(execution_price, 2),
                "portfolio": round(shares * execution_price, 2)
            })

        # ---------------- SELL ----------------

        elif signal == "SELL" and in_position:

            execution_price = price * (1 - SLIPPAGE)

            cash = shares * execution_price

            cash *= (1 - COMMISSION)

            shares = 0

            in_position = False

            total_trades += 1

            if execution_price > buy_price:
                wins += 1

            trades.append({
                "date": date,
                "signal": "SELL",
                "price": round(execution_price, 2),
                "portfolio": round(cash, 2)
            })

        # Current Portfolio Value

        if in_position:
            portfolio_value = shares * price
        else:
            portfolio_value = cash

        equity_curve.append(portfolio_value)
        
    # ==========================================
    # Final Portfolio Value
    # ==========================================
    if in_position:

        last_price = float(df["Close"].iloc[-1]) * (1 - SLIPPAGE)

        final_value = shares * last_price

        final_value *= (1 - COMMISSION)

    else:

        final_value = cash

    total_return = (
        (final_value - initial_capital)
        / initial_capital
    ) * 100
    
    # ==========================================
    # Buy & Hold Benchmark
    # ==========================================

    buy_hold_return = (
        (
            float(df["Close"].iloc[-1])
            - float(df["Close"].iloc[0])
        )
        / float(df["Close"].iloc[0])
    ) * 100

    # ==========================================
    # Maximum Drawdown
    # ==========================================

    equity_array = np.array(equity_curve)

    running_max = np.maximum.accumulate(equity_array)

    drawdowns = (
        running_max - equity_array
    ) / running_max

    max_drawdown = drawdowns.max() * 100

    # ==========================================
    # Daily Returns
    # ==========================================

    equity_returns = pd.Series(equity_curve).pct_change().dropna()

    if len(equity_returns) > 1 and equity_returns.std() != 0:

        sharpe = (
            equity_returns.mean()
            / equity_returns.std()
        ) * np.sqrt(252)

    else:

        sharpe = 0

    # ==========================================
    # Win Rate
    # ==========================================

    if total_trades > 0:
        win_rate = (wins / total_trades) * 100
    else:
        win_rate = 0
        
    # ==========================================
    # Debug
    # ==========================================

    print("Initial:", initial_capital)
    print("Final:", final_value)
    print("Trades:", total_trades)
    print("Return:", total_return)

    # ==========================================
    # Return Response
    # ==========================================
    
    buy_hold_shares = initial_capital / float(df["Close"].iloc[0])

    buy_hold_equity = [
        round(buy_hold_shares * float(price), 2)
        for price in df["Close"]
    ]

    return {

        "success": True,

        "total_return": round(total_return, 2),

        "sharpe": round(float(sharpe), 2),

        "drawdown": round(float(max_drawdown), 2),

        "win_rate": round(float(win_rate), 2),

        "equity": [round(x, 2) for x in equity_curve],
        
        "buy_hold_equity": buy_hold_equity,

        "buy_hold_return": round(buy_hold_return, 2),

        "trades": trades

    }