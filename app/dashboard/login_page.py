import streamlit as st
from pathlib import Path


def load_css():
    css = Path("app/static/styles.css")

    if css.exists():
        st.markdown(
            f"<style>{css.read_text()}</style>",
            unsafe_allow_html=True
        )


def show_login_page():

    load_css()

    st.markdown(
        """
<div class="page">

<div class="glass-card">

<h1 class="title">
Welcome back
</h1>

<p class="subtitle">
Sign in to your trading desk
</p>

""",
        unsafe_allow_html=True,
    )

    st.button(
        "🔵 Continue with Google",
        use_container_width=True,
        disabled=True
    )

    st.markdown(
        """
<div class="divider">
<span>OR SIGN IN WITH EMAIL</span>
</div>
        """,
        unsafe_allow_html=True,
    )

    email = st.text_input(
    "Email",
    placeholder="you@quantedge.io",
    key="login_email"
)

col1, col2 = st.columns([3,1])

with col1:
    st.markdown(
        "<label class='password-label'>Password</label>",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        "<p class='forgot'>Forgot password?</p>",
        unsafe_allow_html=True,
    )

password = st.text_input(
    "",
    type="password",
    placeholder="Minimum 8 characters",
    key="login_password",
    label_visibility="collapsed"
)

st.checkbox("Keep me signed in for 30 days")

st.button(
    "Sign in to dashboard",
    use_container_width=True,
    key="login_button"
)

st.markdown(
    """
<div class="bottom-link">
Don't have an account?
<b>Create one</b>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
</div>
</div>
""",
    unsafe_allow_html=True,
)