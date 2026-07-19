import streamlit as st

from app.auth.session import Session


# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="Algorithmic Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ----------------------------------------
# Show Login or Dashboard
# ----------------------------------------

if not Session.is_logged_in():

    from app.dashboard.login_page import show_login_page

    show_login_page()

else:

    from app.dashboard.main_dashboard import show_dashboard_page

    show_dashboard_page()