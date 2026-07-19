import streamlit as st
import plotly.express as px


def equity_curve(portfolio_history):

    if portfolio_history.empty:

        st.info("No portfolio history available.")

        return

    fig = px.line(

        portfolio_history,

        x="Date",

        y="Portfolio_Value",

        title="Portfolio Equity Curve"

    )

    fig.update_layout(

        template="plotly_dark",

        height=450,

        margin=dict(l=10, r=10, t=50, b=10),

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font=dict(color="white")

    )

    st.plotly_chart(

        fig,

        width="stretch"

    )


def asset_allocation(trades):

    if trades.empty:

        st.info("No trades available.")

        return

    holdings = (

        trades.groupby("Asset")["Shares"]

        .sum()

        .reset_index()

    )

    fig = px.pie(

        holdings,

        names="Asset",

        values="Shares",

        hole=0.45,

        title="Asset Allocation"

    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font=dict(color="white")

    )

    st.plotly_chart(

        fig,

        width="stretch"

    )