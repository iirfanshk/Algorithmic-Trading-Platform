import pandas as pd
import numpy as np
import plotly.express as px



def portfolio_growth_chart():

    try:
        df = pd.read_csv("data/backtest/portfolio_history.csv")
    except FileNotFoundError:
        return "<h3>No portfolio history available.</h3>"

    if df.empty:
        return "<h3>No portfolio history available.</h3>"

    df["Date"] = pd.to_datetime(df["Date"], format="mixed")

    df["Portfolio_Value"] = (
        df["Portfolio_Value"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    fig = px.line(
        df,
        x="Date",
        y="Portfolio_Value",
        title="Portfolio Growth",
        markers=True
    )

    fig.update_traces(
        marker=dict(size=8, color="#8b7cf6"),
        line=dict(width=3, color="#8b7cf6")
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Time",
        yaxis_title="Portfolio Value ($)"
    )

    min_val = df["Portfolio_Value"].min()
    max_val = df["Portfolio_Value"].max()
    value_range = max_val - min_val

    if value_range == 0:
        fig.update_yaxes(
            tickformat="$,.0f",
            separatethousands=True,
            range=[min_val - 100, max_val + 100]
        )
    else:
        padding = max(value_range * 0.2, 20)
        fig.update_yaxes(
            tickformat="$,.0f",
            separatethousands=True,
            range=[min_val - padding, max_val + padding]
        )

    return fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )


def calculate_sharpe_ratio():

    try:
        df = pd.read_csv("data/backtest/portfolio_history.csv")
    except FileNotFoundError:
        return "-"

    if len(df) < 2:
        return "-"

    df["Portfolio_Value"] = (
        df["Portfolio_Value"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    returns = df["Portfolio_Value"].pct_change().dropna()

    if len(returns) == 0 or returns.std() == 0:
        return "-"

    risk_free_rate = 0.0

    sharpe = (returns.mean() - risk_free_rate) / returns.std()

    sharpe_annualized = sharpe * np.sqrt(252)

    return round(sharpe_annualized, 2)