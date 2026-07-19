import streamlit as st


def show_settings():

    st.title("⚙ Settings")
    st.caption("Manage your trading platform preferences.")

    st.divider()

    # ----------------------------------------
    # Profile
    # ----------------------------------------

    st.subheader("👤 Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Username",
            value="irfan1"
        )

        st.text_input(
            "Email",
            value="irfan@example.com"
        )

    with col2:
        st.selectbox(
            "Default Asset",
            [
                "AAPL",
                "AMZN",
                "META",
                "MSFT",
                "GOOGL",
                "BTC-USD",
                "ETH-USD",
                "SOL-USD"
            ]
        )

        st.selectbox(
            "Default Strategy",
            [
                "SMA",
                "RSI",
                "MACD",
                "LSTM",
                "XGBoost"
            ]
        )

    st.divider()

    # ----------------------------------------
    # Trading Settings
    # ----------------------------------------

    st.subheader("💰 Trading")

    col1, col2 = st.columns(2)

    with col1:

        capital = st.number_input(
            "Initial Capital ($)",
            value=100000,
            step=1000
        )

        risk = st.slider(
            "Risk Per Trade (%)",
            1,
            10,
            2
        )

    with col2:

        commission = st.number_input(
            "Commission Per Trade ($)",
            value=20.0,
            step=1.0
        )

        leverage = st.selectbox(
            "Leverage",
            [
                "1x",
                "2x",
                "5x",
                "10x"
            ]
        )

    st.divider()

    # ----------------------------------------
    # Appearance
    # ----------------------------------------

    st.subheader("🎨 Appearance")

    col1, col2 = st.columns(2)

    with col1:

        st.selectbox(
            "Theme",
            [
                "Dark",
                "Light"
            ]
        )

    with col2:

        st.selectbox(
            "Chart Theme",
            [
                "Plotly Dark",
                "Plotly White"
            ]
        )

    st.divider()

    # ----------------------------------------
    # Notifications
    # ----------------------------------------

    st.subheader("🔔 Notifications")

    email_alerts = st.toggle(
        "Email Notifications",
        value=True
    )

    trade_alerts = st.toggle(
        "Trade Alerts",
        value=True
    )

    news_alerts = st.toggle(
        "Market News Alerts",
        value=False
    )

    st.divider()

    # ----------------------------------------
    # Security
    # ----------------------------------------

    st.subheader("🔐 Security")

    st.text_input(
        "New Password",
        type="password"
    )

    st.text_input(
        "Confirm Password",
        type="password"
    )

    st.divider()

    # ----------------------------------------
    # Buttons
    # ----------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Save Settings",
            width="stretch"
        ):
            st.success("Settings saved successfully!")

    with col2:

        if st.button(
            "🔄 Reset",
            width="stretch"
        ):
            st.warning("Settings reset to default.")