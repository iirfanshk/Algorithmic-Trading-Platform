import streamlit as st
import pandas as pd


def show_trading():

    st.title("💹 Paper Trading")

    st.caption("Practice trading without risking real money.")

    st.divider()

    # ===========================================
    # Account Summary
    # ===========================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Cash Balance", "$100,000")

    c2.metric("Portfolio Value", "$112,450")

    c3.metric("Today's P/L", "+$1,280")

    c4.metric("Open Positions", "4")

    st.divider()

    # ===========================================
    # Trade Panel
    # ===========================================

    left, right = st.columns(2)

    with left:

        asset = st.selectbox(
            "Asset",
            [
                "AAPL",
                "MSFT",
                "GOOGL",
                "AMZN",
                "META",
                "NVDA",
                "BTC-USD",
                "ETH-USD",
                "SOL-USD"
            ]
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=10
        )

    with right:

        order_type = st.selectbox(
            "Order Type",
            [
                "Market",
                "Limit"
            ]
        )

        price = st.number_input(
            "Price",
            value=100.0
        )

    buy, sell = st.columns(2)

    if buy.button("🟢 BUY", width="stretch"):
        st.success(f"Bought {quantity} shares of {asset}")

    if sell.button("🔴 SELL", width="stretch"):
        st.success(f"Sold {quantity} shares of {asset}")

    st.divider()

    # ===========================================
    # Current Positions
    # ===========================================

    st.subheader("Current Positions")

    positions = pd.DataFrame({

        "Asset": ["AAPL", "NVDA", "BTC-USD"],

        "Quantity": [20, 10, 2],

        "Average Price": [180.25, 950.60, 108000],

        "Current Price": [184.50, 972.80, 109250],

        "P/L": ["+$85", "+$222", "+$2,500"]

    })

    st.dataframe(
        positions,
        width="stretch",
        hide_index=True
    )