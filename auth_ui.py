"""
auth_ui.py
------------
Streamlit login/signup UI, shared between app.py and any other page that
needs to gate access. Sets st.session_state["user"] = {"id": ..., "email": ...}
once a user is authenticated; every page checks for this before rendering
its real content.
"""

import streamlit as st

from database.db import init_db
from database.auth import register_user, verify_login, AuthError
from styles import (
    render_brand_bar,
    render_hero_two_column,
    render_stats_bar,
    render_feature_cards,
    render_how_it_works,
    render_footer,
)

# Keys in st.session_state that hold data from a specific user's analysis
# session. These must be cleared on every login, signup, and logout -
# otherwise Streamlit's session state (which persists across the whole
# browser tab, not per-account) can leak one user's report to whoever
# logs into that same browser tab next.
_ANALYSIS_STATE_KEYS = ["report_md"]


def _clear_analysis_state() -> None:
    """Remove any leftover analysis results from session state."""
    for key in _ANALYSIS_STATE_KEYS:
        st.session_state.pop(key, None)


def render_auth_gate() -> bool:
    """
    Render a full landing page with a login/signup form if no user is
    logged in.

    Returns:
        True if a user is already authenticated - callers should proceed
        to render their real page content.
        False if the login form was just rendered instead - callers should
        stop rendering anything further this run.
    """
    init_db()

    if "user" in st.session_state:
        return True

    render_brand_bar()
    render_hero_two_column()
    render_stats_bar()
    render_feature_cards()
    render_how_it_works()

    st.markdown('<div class="auth-section-wrap">', unsafe_allow_html=True)
    left, right = st.columns([1, 1.1], gap="large")

    with left:
        st.markdown(
            """
            <div class="auth-value-title">Ready to see where you stand?</div>
            <div class="auth-value-text">
                Create a free account to save your reports, track your progress
                over time, and revisit your personalized roadmap whenever you need it.
            </div>
            <div class="auth-value-point">✅ &nbsp; Unlimited resume analyses</div>
            <div class="auth-value-point">✅ &nbsp; Full report history, always accessible</div>
            <div class="auth-value-point">✅ &nbsp; Your data is never shared with other accounts</div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="auth-card-wrap">', unsafe_allow_html=True)
        login_tab, signup_tab = st.tabs(["Log In", "Sign Up"])

        with login_tab:
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")
                submitted = st.form_submit_button("Log In →", type="primary", use_container_width=True)

                if submitted:
                    user = verify_login(email, password)
                    if user is None:
                        st.error("Incorrect email or password.")
                    else:
                        _clear_analysis_state()
                        st.session_state["user"] = user
                        st.rerun()

        with signup_tab:
            with st.form("signup_form"):
                new_email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
                new_password = st.text_input("Password", type="password", key="signup_password", placeholder="At least 8 characters")
                confirm_password = st.text_input("Confirm password", type="password", key="signup_confirm", placeholder="Re-enter your password")
                submitted = st.form_submit_button("Create Free Account →", type="primary", use_container_width=True)

                if submitted:
                    if new_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        try:
                            user_id = register_user(new_email, new_password)
                            _clear_analysis_state()
                            st.session_state["user"] = {"id": user_id, "email": new_email.strip().lower()}
                            st.success("Account created! Redirecting...")
                            st.rerun()
                        except AuthError as exc:
                            st.error(str(exc))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="trust-line">
            <span>🔒 Bank-grade password hashing</span>
            <span>🚫 No credit card required</span>
            <span>👤 Your data stays private</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()

    return False


def render_user_badge_and_logout() -> None:
    """Render the logged-in user's email and a logout button in the sidebar."""
    user = st.session_state.get("user")
    if not user:
        return
    with st.sidebar:
        st.markdown(f"**Signed in as**  \n{user['email']}")
        if st.button("Log out", use_container_width=True):
            del st.session_state["user"]
            _clear_analysis_state()
            st.rerun()
