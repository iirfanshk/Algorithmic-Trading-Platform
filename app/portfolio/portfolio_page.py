import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


def show_portfolio():

    st.title("💼 Portfolio")

    portfolio_file = Path("data/backtest/portfolio_history.csv")
    trade_file = Path("data/backtest/trade_history.csv")

    # ------------------------------------------
    # Portfolio History
    # ------------------------------------------

    if portfolio_file.exists():

        portfolio = pd.read_csv(portfolio_file)

        latest = portfolio.iloc[-1]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Portfolio Value",
            f"${latest['Portfolio_Value']:,.2f}"
        )

        col2.metric(
            "Cash",
            f"${latest['Cash']:,.2f}"
        )

        col3.metric(
            "Holdings",
            f"${latest['Holdings']:,.2f}"
        )

        st.divider()

        st.subheader("Portfolio Performance")

        fig = px.line(

            portfolio,

            x="Date",

            y="Portfolio_Value",

            title="Portfolio Equity Curve"

        )

        fig.update_layout(

            template="plotly_dark",

            height=450

        )

        st.plotly_chart(

            fig,

            width="stretch"

        )

    else:

        st.warning("Portfolio history not found.")

    # ------------------------------------------
    # Trade History
    # ------------------------------------------

    st.divider()

    st.subheader("Recent Trades")

    if trade_file.exists():

        trades = pd.read_csv(trade_file)

        st.dataframe(

            trades.tail(20),

            width="stretch",

            hide_index=True

        )

        # ------------------------------------------
        # Allocation
        # ------------------------------------------

        st.divider()

        st.subheader("Asset Allocation")

        allocation = (

            trades.groupby("Asset")["Shares"]

            .sum()

            .reset_index()

        )

        pie = px.pie(

            allocation,

            names="Asset",

            values="Shares",

            hole=0.45

        )

        pie.update_layout(

            template="plotly_dark",

            height=500

        )

        st.plotly_chart(

            pie,

            width="stretch"

        )

    else:

        st.info("No trades available.")