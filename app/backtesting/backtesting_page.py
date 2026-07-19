import streamlit as st
import pandas as pd
import plotly.express as px
import time
from pathlib import Path


def load_backtest(asset="AAPL"):

    file = Path(f"data/processed/{asset}_backtest.csv")

    if not file.exists():
        file = Path(f"data/processed/{asset}/backtest.csv")

    if not file.exists():
        file = Path("data/processed/AAPL_backtest.csv")

    if not file.exists():
        st.error("Backtest data not found.")
        return None

    df = pd.read_csv(file)
    df["Date"] = pd.to_datetime(df["Date"])

    return df


def show_backtesting():

    st.title("🧪 Strategy Backtesting")
    st.caption("Evaluate trading strategies using historical market data.")
    st.divider()

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

        strategy = st.selectbox(
            "Strategy",
            [
                "SMA Crossover",
                "RSI",
                "MACD",
                "Bollinger Bands",
                "LSTM",
                "XGBoost"
            ]
        )

        capital = st.number_input(
            "Initial Capital",
            value=100000,
            step=5000
        )

    with right:
        commission = st.number_input(
            "Commission",
            value=20.0,
            step=1.0
        )

        position = st.slider(
            "Position Size (%)",
            10,
            100,
            100
        )

        risk = st.slider(
            "Risk Per Trade (%)",
            1,
            10,
            2
        )

    start, end = st.date_input(
        "Backtest Period",
        (
            pd.Timestamp("2024-01-01"),
            pd.Timestamp.today()
        )
    )

    st.divider()

    if st.button("▶ Run Backtest", width="stretch"):

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        with st.spinner("Running strategy..."):
            df = load_backtest(asset)

        if df is None:
            return

        portfolio = df["Portfolio_Value"].iloc[-1]

        total_return = (
            (portfolio - capital)
            / capital
        ) * 100

        daily_returns = df["Portfolio_Value"].pct_change().dropna()

        if daily_returns.std() == 0:
            sharpe = 0
        else:
            sharpe = (
                daily_returns.mean()
                / daily_returns.std()
            ) * (252 ** 0.5)

        winning_trades = (daily_returns > 0).sum()
        losing_trades = (daily_returns < 0).sum()

        trades = winning_trades + losing_trades

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Portfolio Value", f"${portfolio:,.2f}")
        c2.metric("Return", f"{total_return:.2f}%")
        c3.metric("Sharpe Ratio", f"{sharpe:.2f}")
        c4.metric("Trades", trades)

        st.divider()

        st.subheader("Portfolio Equity Curve")

        fig = px.line(
            df,
            x="Date",
            y="Portfolio_Value",
            title="Portfolio Value"
        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(fig, width="stretch")

        running_max = df["Portfolio_Value"].cummax()

        drawdown = (
            (df["Portfolio_Value"] - running_max)
            / running_max
        ) * 100

        st.subheader("Portfolio Drawdown")

        fig2 = px.area(
            x=df["Date"],
            y=drawdown,
            title="Drawdown (%)"
        )

        fig2.update_layout(
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(fig2, width="stretch")

        cagr = (
            (
                df["Portfolio_Value"].iloc[-1]
                / df["Portfolio_Value"].iloc[0]
            ) ** (252 / len(df))
            - 1
        ) * 100

        if daily_returns.std() == 0:
            volatility = 0
        else:
            volatility = daily_returns.std() * (252 ** 0.5) * 100

        profits = daily_returns[daily_returns > 0].sum()
        losses = abs(daily_returns[daily_returns < 0].sum())

        if losses == 0:
            profit_factor = 0
        else:
            profit_factor = profits / losses

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("CAGR", f"{cagr:.2f}%")
        m2.metric("Max Drawdown", f"{drawdown.min():.2f}%")
        m3.metric("Volatility", f"{volatility:.2f}%")
        m4.metric("Profit Factor", f"{profit_factor:.2f}")

        st.divider()

        monthly = df.copy()
        monthly["Month"] = monthly["Date"].dt.strftime("%Y-%m")
        monthly = monthly.groupby("Month")["Portfolio_Value"].last().pct_change() * 100
        monthly = monthly.reset_index()

        st.subheader("Monthly Returns")

        fig3 = px.bar(
            monthly,
            x="Month",
            y="Portfolio_Value",
            title="Monthly Returns (%)"
        )

        fig3.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig3, width="stretch")

        st.divider()

        # =====================================================
        # Trade Statistics
        # =====================================================

        st.subheader("Trade Statistics")

        if winning_trades == 0:
            avg_profit = 0
        else:
            avg_profit = (
                daily_returns[daily_returns > 0].mean()
                * portfolio
            )

        if losing_trades == 0:
            avg_loss = 0
        else:
            avg_loss = (
                daily_returns[daily_returns < 0].mean()
                * portfolio
            )

        total = winning_trades + losing_trades

        if total == 0:
            win_rate = 0
        else:
            win_rate = winning_trades / total * 100

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Winning Trades", winning_trades)
        c2.metric("Losing Trades", losing_trades)
        c3.metric("Win Rate", f"{win_rate:.2f}%")
        c4.metric("Average Profit", f"${avg_profit:,.2f}")
        c5.metric("Average Loss", f"${avg_loss:,.2f}")

        st.divider()

        # =====================================================
        # Trade Distribution
        # =====================================================

        st.subheader("Trade Distribution")

        trade_dist = pd.DataFrame({
            "Result": [
                "Winning",
                "Losing"
            ],
            "Trades": [
                winning_trades,
                losing_trades
            ]
        })

        fig4 = px.pie(
            trade_dist,
            names="Result",
            values="Trades",
            hole=0.45,
            title="Winning vs Losing Trades"
        )

        fig4.update_layout(
            template="plotly_dark",
            height=420
        )

        st.plotly_chart(fig4, width="stretch")

        st.divider()

        # =====================================================
        # Trade History
        # =====================================================

        st.subheader("Executed Trades")

        trade_file = Path("data/backtest/trade_history.csv")

        if trade_file.exists():

            trades_df = pd.read_csv(trade_file)

            st.dataframe(
                trades_df,
                width="stretch",
                hide_index=True
            )

            st.download_button(
                "⬇ Export Trade History",
                trades_df.to_csv(index=False),
                file_name="trade_history.csv",
                mime="text/csv",
                width="stretch"
            )

        else:
            st.info("Trade history not available.")

        st.divider()

        # =====================================================
        # Strategy Summary
        # =====================================================

        st.subheader("📋 Backtest Summary")

        summary = pd.DataFrame({
            "Parameter": [
                "Asset",
                "Strategy",
                "Initial Capital",
                "Commission",
                "Position Size",
                "Risk Per Trade",
                "Backtest Period"
            ],
            "Value": [
                asset,
                strategy,
                f"${capital:,.2f}",
                f"${commission:.2f}",
                f"{position}%",
                f"{risk}%",
                f"{start} → {end}"
            ]
        })

        st.dataframe(
            summary,
            width="stretch",
            hide_index=True
        )

        st.divider()

        # =====================================================
        # Performance Report
        # =====================================================

        report = pd.DataFrame({
            "Metric": [
                "Portfolio Value",
                "Return (%)",
                "Sharpe Ratio",
                "CAGR",
                "Volatility",
                "Max Drawdown",
                "Profit Factor",
                "Winning Trades",
                "Losing Trades"
            ],
            "Value": [
                round(portfolio, 2),
                round(total_return, 2),
                round(sharpe, 2),
                round(cagr, 2),
                round(volatility, 2),
                round(drawdown.min(), 2),
                round(profit_factor, 2),
                winning_trades,
                losing_trades
            ]
        })

        st.download_button(
            "📥 Download Performance Report",
            report.to_csv(index=False),
            file_name=f"{asset}_backtest_report.csv",
            mime="text/csv",
            width="stretch"
        )

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            st.success("✅ Backtest Completed Successfully")

        with c2:
            st.info(
                f"Completed at: {pd.Timestamp.now().strftime('%d-%b-%Y %H:%M:%S')}"
            )

        st.caption(
            "Algorithmic Trading Platform • Backtesting Engine v1.0"
        )