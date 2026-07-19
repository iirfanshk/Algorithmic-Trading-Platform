import yfinance as yf
import plotly.graph_objects as go

from app.config.assets import ASSETS


def get_market_data(asset_class, ticker):

    stock = yf.Ticker(ticker)

    hist = stock.history(period="6mo")

    if hist.empty:
        return None

    # ============================================
    # Technical Indicators
    # ============================================

    hist["SMA20"] = hist["Close"].rolling(window=20).mean()
    hist["SMA50"] = hist["Close"].rolling(window=50).mean()

    hist["EMA20"] = hist["Close"].ewm(
        span=20,
        adjust=False
    ).mean()

    delta = hist["Close"].diff()

    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()

    rs = gain / loss

    hist["RSI"] = 100 - (100 / (1 + rs))

    ema12 = hist["Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = hist["Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    hist["MACD"] = ema12 - ema26

    hist["Signal"] = hist["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    # ============================================
    # Company Information
    # ============================================

    try:
        info = stock.info
    except Exception:
        info = {}

    current = float(hist["Close"].iloc[-1])
    previous = float(hist["Close"].iloc[-2])

    change = current - previous
    change_percent = (change / previous) * 100

    # ============================================
    # Chart
    # ============================================

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=hist.index,
            open=hist["Open"],
            high=hist["High"],
            low=hist["Low"],
            close=hist["Close"],
            name="Price"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["SMA20"],
            mode="lines",
            name="SMA 20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["SMA50"],
            mode="lines",
            name="SMA 50"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["EMA20"],
            mode="lines",
            name="EMA 20"
        )
    )

    fig.update_layout(

        template="plotly_dark",

        height=700,

        margin=dict(
            l=10,
            r=10,
            t=30,
            b=10
        ),

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font=dict(
            color="white"
        ),

        legend=dict(
            orientation="h",
            y=1.02,
            x=0
        ),

        xaxis=dict(
            showgrid=False,
            rangeslider_visible=False
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="#374151"
        )

    )

    chart = fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    # ============================================
    # Return
    # ============================================

    return {

        "asset_classes": list(ASSETS.keys()),

        "tickers": ASSETS[asset_class],

        "selected_asset_class": asset_class,

        "selected_ticker": ticker,

        "current_price": round(current, 2),

        "change_percent": round(change_percent, 2),

        "volume": int(hist["Volume"].iloc[-1]),

        "company": info.get("longName", ticker),

        "sector": info.get("sector", "N/A"),

        "industry": info.get("industry", "N/A"),

        "summary": info.get(
            "longBusinessSummary",
            "No description available."
        ),

        "chart": chart,

        "rsi": round(hist["RSI"].fillna(0).iloc[-1], 2),

        "macd": round(hist["MACD"].fillna(0).iloc[-1], 2),

        "signal": round(hist["Signal"].fillna(0).iloc[-1], 2),

        "ema20": round(hist["EMA20"].fillna(0).iloc[-1], 2),

        "sma20": round(hist["SMA20"].fillna(0).iloc[-1], 2),

        "sma50": round(hist["SMA50"].fillna(0).iloc[-1], 2)

    }