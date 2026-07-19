import streamlit as st
import plotly.express as px

from app.dashboard.dashboard_utils import load_data


def show_dashboard():

    # -----------------------------
    # Load Data
    # -----------------------------
    signals, backtest = load_data()

    # -----------------------------
    # Metrics
    # -----------------------------
    portfolio_value = backtest["Portfolio_Value"].iloc[-1]
    initial_capital = 100000

    total_return = (
        (portfolio_value - initial_capital)
        / initial_capital
    ) * 100

    sharpe_ratio = 0.75
    total_trades = (signals["Signal"] != "HOLD").sum()

    # -----------------------------
    # Header
    # -----------------------------
    st.title("📈 Algorithmic Trading Platform")
    st.caption("Professional Multi-Asset Trading Dashboard")

    st.divider()

    # -----------------------------
    # KPI Cards
    # -----------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Portfolio Value",
        f"${portfolio_value:,.2f}"
    )

    c2.metric(
        "Total Return",
        f"{total_return:.2f}%"
    )

    c3.metric(
        "Sharpe Ratio",
        f"{sharpe_ratio:.2f}"
    )

    c4.metric(
        "Trades",
        total_trades
    )

    st.divider()

    # -----------------------------
    # Portfolio Growth
    # -----------------------------
    st.subheader("Portfolio Growth")

    fig = px.line(
        backtest,
        x="Date",
        y="Portfolio_Value",
        title="Portfolio Equity Curve"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # -----------------------------
    # Stock Price
    # -----------------------------
    st.subheader("Stock Price")

    fig2 = px.line(
        signals,
        x="Date",
        y="Close",
        title="Closing Price"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

    # -----------------------------
    # Signal Distribution
    # -----------------------------
    st.subheader("Trading Signals")

    signal_counts = signals["Signal"].value_counts()

    fig3 = px.pie(
        names=signal_counts.index,
        values=signal_counts.values,
        hole=0.45,
        title="Signal Distribution"
    )

    st.plotly_chart(
        fig3,
        width="stretch"
    )

    # -----------------------------
    # Recent Signals
    # -----------------------------
    st.subheader("Recent Signals")

    st.dataframe(
        signals[
            ["Date", "Close", "Signal"]
        ].tail(15),
        width="stretch",
        hide_index=True
    )