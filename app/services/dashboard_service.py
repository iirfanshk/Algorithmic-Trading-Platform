from app.dashboard.dashboard_utils import load_data
import plotly.express as px


def get_dashboard_data():

    signals, backtest = load_data()

    portfolio_value = float(backtest["Portfolio_Value"].iloc[-1])

    initial_capital = 100000

    total_return = (
        (portfolio_value - initial_capital)
        / initial_capital
    ) * 100

    sharpe_ratio = 0.75

    total_trades = int(
        (signals["Signal"] != "HOLD").sum()
    )

    # -----------------------------
    # Portfolio Growth Chart
    # -----------------------------

    portfolio_chart = px.line(
        backtest,
        x="Date",
        y="Portfolio_Value",
        title="Portfolio Growth"
    )

    portfolio_chart.update_layout(
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    portfolio_chart = portfolio_chart.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    # -----------------------------
    # Signal Distribution
    # -----------------------------

    signal_counts = signals["Signal"].value_counts()

    signal_chart = px.pie(
        names=signal_counts.index,
        values=signal_counts.values,
        hole=0.45
    )

    signal_chart.update_layout(
        template="plotly_dark",
        height=420
    )

    signal_chart = signal_chart.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    return {

        "portfolio_value": round(portfolio_value, 2),

        "total_return": round(total_return, 2),

        "sharpe_ratio": sharpe_ratio,

        "total_trades": total_trades,

        "portfolio_chart": portfolio_chart,

        "signal_chart": signal_chart

    }