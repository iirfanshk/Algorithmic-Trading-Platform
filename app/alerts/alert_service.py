import yfinance as yf


def check_price_alert(asset, target_price, condition):

    data = yf.download(asset, period="1d", progress=False)

    close = data["Close"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    current_price = float(close.iloc[-1])

    triggered = False

    if condition == "Above":
        triggered = current_price >= float(target_price)

    elif condition == "Below":
        triggered = current_price <= float(target_price)

    return {

        "asset": asset,

        "current_price": round(current_price, 2),

        "target_price": float(target_price),

        "condition": condition,

        "triggered": triggered

    }