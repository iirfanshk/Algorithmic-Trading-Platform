import pandas as pd
import plotly.express as px

def portfolio_growth_chart():

    try:
        df = pd.read_csv("data/backtest/portfolio_history.csv")
        print(df.head())
        print(df.dtypes)
    except FileNotFoundError:
        return "<h3>No portfolio history available.</h3>"

    df["Date"] = pd.to_datetime(df["Date"])
    df["Portfolio_Value"] = (
        df["Portfolio_Value"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )
    print(df["Portfolio_Value"].tolist())
    fig = px.line(
        df,
        x="Date",
        y="Portfolio_Value",
        title="Portfolio Growth"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )