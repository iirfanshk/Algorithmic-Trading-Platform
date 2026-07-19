import streamlit as st
import yfinance as yf
import plotly.graph_objects as go


def show_market():

    st.title("📈 Live Market Dashboard")
    st.markdown("Real-time market data powered by Yahoo Finance")
    st.divider()

    # ==========================================
    # Asset Selection
    # ==========================================

    tickers = [
        "AAPL",
        "MSFT",
        "NVDA",
        "GOOGL",
        "META",
        "AMZN",
        "TSLA",
        "BTC-USD",
        "ETH-USD",
        "SOL-USD"
    ]

    ticker = st.selectbox(
        "Select Asset",
        tickers
    )

    stock = yf.Ticker(ticker)

    hist = stock.history(period="6mo")

    if hist.empty:
        st.error("Unable to fetch market data.")
        return

    hist["SMA20"] = hist["Close"].rolling(20).mean()
    hist["SMA50"] = hist["Close"].rolling(50).mean()

    try:
        info = stock.info
    except:
        info = {}

    # ==========================================
    # Price Metrics
    # ==========================================

    current = hist["Close"].iloc[-1]
    previous = hist["Close"].iloc[-2]

    change = current - previous
    change_pct = (change / previous) * 100

    volume = info.get(
        "volume",
        int(hist["Volume"].iloc[-1])
    )

    market_cap = info.get(
        "marketCap",
        None
    )

    high_52 = hist["High"].max()
    low_52 = hist["Low"].min()

    # ==========================================
    # Metrics
    # ==========================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Price",
        f"${current:,.2f}",
        f"{change_pct:.2f}%"
    )

    c2.metric(
        "Previous Close",
        f"${previous:,.2f}"
    )

    c3.metric(
        "Volume",
        f"{volume:,}"
    )

    if market_cap:
        c4.metric(
            "Market Cap",
            f"${market_cap:,.0f}"
        )
    else:
        c4.metric(
            "Market Cap",
            "N/A"
        )

    c5, c6 = st.columns(2)

    c5.metric(
        "52 Week High",
        f"${high_52:,.2f}"
    )

    c6.metric(
        "52 Week Low",
        f"${low_52:,.2f}"
    )

    st.divider()

    # ==========================================
    # Candlestick Chart
    # ==========================================

    st.subheader("Price Chart")

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
            name="SMA20",
            line=dict(width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist["SMA50"],
            mode="lines",
            name="SMA50",
            line=dict(width=2)
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # Company Information
    # ==========================================

    st.subheader("Company Information")

    col1, col2 = st.columns(2)

    col1.write(
        f"**Name:** {info.get('longName', ticker)}"
    )

    col1.write(
        f"**Sector:** {info.get('sector', 'N/A')}"
    )

    col1.write(
        f"**Industry:** {info.get('industry', 'N/A')}"
    )

    col2.write(
        f"**Country:** {info.get('country', 'N/A')}"
    )

    col2.write(
        f"**Website:** {info.get('website', 'N/A')}"
    )

    st.divider()

    # ==========================================
    # Business Summary
    # ==========================================

    st.subheader("Business Summary")

    summary = info.get("longBusinessSummary")

    if not summary:

        if ticker == "BTC-USD":
            summary = (
                "Bitcoin (BTC) is the world's first decentralized cryptocurrency, "
                "designed for peer-to-peer digital payments without a central authority."
            )

        elif ticker == "ETH-USD":
            summary = (
                "Ethereum (ETH) is a decentralized blockchain platform supporting "
                "smart contracts and decentralized applications."
            )

        elif ticker == "SOL-USD":
            summary = (
                "Solana (SOL) is a high-performance blockchain focused on scalable "
                "decentralized applications and fast transactions."
            )

        else:
            summary = "No business summary available."

    st.write(summary)

    st.divider()

    st.success("✅ Live Market Dashboard Loaded Successfully")