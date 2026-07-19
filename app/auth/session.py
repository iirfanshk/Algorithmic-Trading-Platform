import streamlit as st


class Session:

    @staticmethod
    def login(user):

        st.session_state["logged_in"] = True
        st.session_state["user"] = user

    @staticmethod
    def logout():

        st.session_state["logged_in"] = False
        st.session_state["user"] = None

    @staticmethod
    def is_logged_in():

        return st.session_state.get("logged_in", False)

    @staticmethod
    def current_user():

        return st.session_state.get("user", None)