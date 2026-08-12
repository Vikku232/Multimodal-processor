# pyrefly: ignore [missing-import]
import streamlit as st
import db
import os
import json
import requests
import urllib.parse

# Load Google OAuth client config from `st.secrets` or `google_client.json` if present.
client_config = None
try:
    if "google_oauth" in st.secrets:
        client_config = dict(st.secrets["google_oauth"])
except FileNotFoundError:
    pass

if not client_config:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    _client_file = os.path.join(current_dir, "google_client.json")
    if os.path.exists(_client_file):
        try:
            with open(_client_file, "r", encoding="utf-8") as _f:
                client_config = json.load(_f)
        except Exception:
            client_config = None

@st.dialog("🔑 Account Authentication")
def render_auth_dialog():
    if st.session_state.get("google_login_flow", False):
        st.markdown("### 🌐 Sign in with Google")
        st.caption("Choose an account to continue to Multimodal Processor UI")
        
        google_email = st.text_input("Gmail Address", value="vikas.kumar.pandey@gmail.com")
        google_name = st.text_input("Name", value="Vikas Kumar Pandey")
        
        st.caption("Simulated Profile Picture:")
        initials = "+".join(google_name.split())
        avatar_url = f"https://ui-avatars.com/api/?name={initials}&background=0D8ABC&color=fff&size=128"
        st.image(avatar_url, width=64)
        
        col_google_confirm, col_google_back = st.columns(2)
        with col_google_confirm:
            if st.button("Confirm Google Login", key="btn_confirm_google", use_container_width=True):
                if not google_email.endswith("@gmail.com"):
                    st.error("Please enter a valid Gmail address.")
                elif not google_name.strip():
                    st.error("Please enter your name.")
                else:
                    user = db.register_or_login_google(google_email, google_name, avatar_url)
                    if user:
                        st.session_state.user = user
                        st.session_state.authenticated = True
                        st.session_state.show_auth = False
                        st.session_state.google_login_flow = False
                        db.record_login_in_db(google_email, "google")
                        st.success(f"Successfully logged in via Google as {google_name}!")
                        st.rerun()
                    else:
                        st.error("Google Auth connection failed.")
                        
        with col_google_back:
            if st.button("Back", key="btn_back_google", use_container_width=True):
                st.session_state.google_login_flow = False
                st.rerun()
                
    else:
        tab_login, tab_signup = st.tabs(["🔐 Sign In", "📝 Sign Up"])
        
        with tab_login:
            login_email = st.text_input("Email Address", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_pass")
            
            col_login, col_google = st.columns(2)
            with col_login:
                if st.button("Log In", key="btn_login_submit", use_container_width=True):
                    user = db.authenticate_user(login_email, login_password)
                    if user:
                        st.session_state.user = user
                        st.session_state.authenticated = True
                        st.session_state.show_auth = False
                        st.session_state.google_login_flow = False
                        db.record_login_in_db(login_email, "local")
                        st.success(f"Welcome back, {user['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
            
            with col_google:
                if st.button("Continue with Google", key="btn_google_login", use_container_width=True):
                    # If client config is available, start real Google OAuth flow by redirecting
                    if client_config and client_config.get("client_id") and client_config.get("redirect_uri"):
                        auth_base = "https://accounts.google.com/o/oauth2/v2/auth"
                        params = {
                            "client_id": client_config.get("client_id"),
                            "redirect_uri": client_config.get("redirect_uri"),
                            "response_type": "code",
                            "scope": "openid email profile",
                            "access_type": "offline",
                            "prompt": "select_account"
                        }
                        auth_url = auth_base + "?" + urllib.parse.urlencode(params)
                        st.markdown(f"<script>window.parent.location.href=\"{auth_url}\";</script>", unsafe_allow_html=True)
                    else:
                        st.session_state.google_login_flow = True
                        st.rerun()
                    
        with tab_signup:
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_pass")
            
            if st.button("Create Account", key="btn_signup_submit", use_container_width=True):
                if not reg_name.strip() or not reg_email.strip() or not reg_password.strip():
                    st.error("Please fill in all fields.")
                else:
                    success, msg = db.register_user(reg_email, reg_password, reg_name, "local")
                    if success:
                        st.success(msg)
                        user = db.authenticate_user(reg_email, reg_password)
                        st.session_state.user = user
                        st.session_state.authenticated = True
                        st.session_state.show_auth = False
                        st.session_state.google_login_flow = False
                        db.record_login_in_db(reg_email, "local")
                        st.rerun()
                    else:
                        st.error(msg)


def exchange_code_for_user(code: str):
    """Exchange OAuth2 code for tokens, fetch userinfo and register/login the user.

    Returns a user dict on success or None on failure.
    """
    if not client_config:
        return None
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": client_config.get("client_id"),
        "client_secret": client_config.get("client_secret"),
        "redirect_uri": client_config.get("redirect_uri"),
        "grant_type": "authorization_code",
    }
    try:
        r = requests.post(token_url, data=payload, timeout=10)
        r.raise_for_status()
        tokens = r.json()
        access_token = tokens.get("access_token")
        if not access_token:
            return None
        # Fetch userinfo from OpenID Connect endpoint
        ui = requests.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        ui.raise_for_status()
        info = ui.json()
        email = info.get("email")
        name = info.get("name") or info.get("given_name") or email
        picture = info.get("picture")
        if not email:
            return None
        user = db.register_or_login_google(email, name, picture)
        if user:
            db.record_login_in_db(email, "google")
        return user
    except Exception:
        return None


def get_google_auth_url():
    """Return the Google OAuth2 authorization URL if client_config is present, else None."""
    if not client_config:
        return None
    auth_base = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": client_config.get("client_id"),
        "redirect_uri": client_config.get("redirect_uri"),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }
    return auth_base + "?" + urllib.parse.urlencode(params)
