import streamlit as st


def metric_cards(metrics):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Portfolio Value",
            f"${metrics.get('Final Value', 0):,.2f}"
        )

    with col2:
        st.metric(
            "📈 Total Return",
            f"{metrics.get('Total Return (%)', 0)} %"
        )

    with col3:
        st.metric(
            "⚡ Sharpe Ratio",
            metrics.get("Sharpe Ratio", 0)
        )

    with col4:
        st.metric(
            "📉 Max Drawdown",
            f"{metrics.get('Maximum Drawdown (%)', 0)} %"
        )