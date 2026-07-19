import streamlit as st
import pandas as pd
from pathlib import Path


def show_trade_history():

    st.title("📜 Trade History")

    st.markdown("Review all executed trades.")

    st.divider()

    trade_file = Path("data/backtest/trade_history.csv")

    if not trade_file.exists():

        st.warning("No trade history found.")

        return

    trades = pd.read_csv(trade_file)

    # -----------------------------------
    # Search
    # -----------------------------------

    search = st.text_input(
        "🔍 Search Asset",
        placeholder="Example: AAPL"
    )

    if search:

        trades = trades[
            trades["Asset"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # -----------------------------------
    # Filter
    # -----------------------------------

    if "Trade_Type" in trades.columns:

        trade_filter = st.selectbox(

            "Trade Type",

            ["All", "BUY", "SELL"]

        )

        if trade_filter != "All":

            trades = trades[
                trades["Trade_Type"] == trade_filter
            ]

    # -----------------------------------
    # Metrics
    # -----------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Trades",
        len(trades)
    )

    if "Trade_Type" in trades.columns:

        c2.metric(
            "BUY",
            (trades["Trade_Type"] == "BUY").sum()
        )

        c3.metric(
            "SELL",
            (trades["Trade_Type"] == "SELL").sum()
        )

    st.divider()

    # -----------------------------------
    # Table
    # -----------------------------------

    st.dataframe(

        trades,

        width="stretch",

        hide_index=True

    )

    # -----------------------------------
    # Download
    # -----------------------------------

    st.download_button(

        "⬇ Download CSV",

        trades.to_csv(index=False),

        "trade_history.csv",

        "text/csv",

        width="stretch"

    )