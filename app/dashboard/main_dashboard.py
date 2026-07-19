import streamlit as st

from app.components.sidebar import show_sidebar

from app.dashboard.dashboard import show_dashboard
from app.dashboard.market_page import show_market
from app.dashboard.trade_history_page import show_trade_history
from app.dashboard.settings_page import show_settings

from app.portfolio.portfolio_page import show_portfolio
from app.backtesting.backtesting_page import show_backtesting
from app.models.models_page import show_models


def show_dashboard_page():

    # -----------------------------
    # Sidebar
    # -----------------------------
    show_sidebar()

    page = st.session_state.get(
        "page",
        "Dashboard"
    )

    # -----------------------------
    # Routing
    # -----------------------------
    if page == "Dashboard":

        show_dashboard()

    elif page == "Portfolio":

        show_portfolio()

    elif page == "Market":

        show_market()

    elif page == "Backtesting":

        show_backtesting()

    elif page == "Models":

        show_models()

    elif page == "Trade History":

        show_trade_history()

    elif page == "Settings":

        show_settings()