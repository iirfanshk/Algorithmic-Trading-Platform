import streamlit as st

from app.auth.session import Session


def show_sidebar():

    # ==========================================
    # Initialize
    # ==========================================

    if "page" not in st.session_state:
        st.session_state["page"] = "Dashboard"

    # ==========================================
    # Logo
    # ==========================================

    st.sidebar.title("📈 AlgoTrade")

    st.sidebar.caption(
        "Algorithmic Trading Platform"
    )

    st.sidebar.divider()

    # ==========================================
    # User
    # ==========================================

    st.sidebar.success(
        f"Logged in as\n\n**{Session.current_user()}**"
    )

    st.sidebar.divider()

    # ==========================================
    # Navigation
    # ==========================================

    pages = {

        "🏠 Dashboard": "Dashboard",

        "💼 Portfolio": "Portfolio",

        "📈 Market": "Market",

        "🧪 Backtesting": "Backtesting",

        "🤖 Models": "Models",

        "📜 Trade History": "Trade History",

        "⚙️ Settings": "Settings"

    }

    for label, page in pages.items():

        if st.sidebar.button(

            label,

            width="stretch",

            type="primary"
            if st.session_state["page"] == page
            else "secondary"

        ):

            st.session_state["page"] = page

            st.rerun()

    st.sidebar.divider()

    # ==========================================
    # Platform Info
    # ==========================================

    st.sidebar.caption("Version 1.0")

    st.sidebar.caption("Built with ❤️ using Streamlit")

    st.sidebar.divider()

    # ==========================================
    # Logout
    # ==========================================

    if st.sidebar.button(

        "🚪 Logout",

        width="stretch"

    ):

        Session.logout()

        st.rerun()