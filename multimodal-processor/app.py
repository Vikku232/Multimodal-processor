import streamlit as st
# ---------- Page Config ----------
st.set_page_config(page_title="Multimodal Processor UI", layout="wide")

import datetime
import db
import auth
import pages

# Ensure NLTK tokenizer models are downloaded
import nltk
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

# Initialize MySQL tables
db.init_db()

# ---------- Session State Initialization ----------
if "page" not in st.session_state:
    st.session_state.page = "opencv"
if "action" not in st.session_state:
    st.session_state.action = None
if "history" not in st.session_state:
    st.session_state.history = db.load_history_from_db()
if "canny_t1" not in st.session_state:
    st.session_state.canny_t1 = 100
if "canny_t2" not in st.session_state:
    st.session_state.canny_t2 = 200
if "blur_k" not in st.session_state:
    st.session_state.blur_k = 15
if "user" not in st.session_state:
    st.session_state.user = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "show_auth" not in st.session_state:
    st.session_state.show_auth = False
if "google_login_flow" not in st.session_state:
    st.session_state.google_login_flow = False

# ---------- Sidebar Component ----------
def render_sidebar():
    # Load stylesheet and inject it
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, "style.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        pass

    # Brand Logo & Title
    st.sidebar.markdown("""
    <div class="sidebar-brand">
        <svg class="brand-logo" width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#3b82f6" />
                    <stop offset="100%" stop-color="#8b5cf6" />
                </linearGradient>
                <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#10b981" />
                    <stop offset="100%" stop-color="#3b82f6" />
                </linearGradient>
                <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="2" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>
            <circle cx="13" cy="13" r="7" fill="url(#grad1)" opacity="0.85" filter="url(#softGlow)" />
            <circle cx="19" cy="13" r="6.5" fill="url(#grad2)" opacity="0.8" filter="url(#softGlow)" />
            <circle cx="15.5" cy="19.5" r="7.5" fill="url(#grad1)" opacity="0.9" filter="url(#softGlow)" />
        </svg>
        <span class="brand-name">multimodal</span>
    </div>
    """, unsafe_allow_html=True)

    # Pages list
    pages_list = [
        {"name": "Home", "icon": "🏠", "id": "home"},
        {"name": "Impacts", "icon": "📊", "id": "impacts"},
        {"name": "Energy", "icon": "📅", "id": "energy"},
        {"name": "OpenCV", "icon": "📄", "id": "opencv"},
        {"name": "Results", "icon": "❓", "id": "results"}
    ]

    for p in pages_list:
        is_active = (st.session_state.page == p["id"])
        active_class = "sidebar-btn-active" if is_active else "sidebar-btn-inactive"
        st.sidebar.markdown(f'<div class="{active_class}"></div>', unsafe_allow_html=True)
        if st.sidebar.button(f"{p['icon']}  {p['name']}", key=f"side_{p['id']}", use_container_width=True):
            st.session_state.page = p["id"]
            st.rerun()

    st.sidebar.markdown('<div class="sidebar-separator"></div>', unsafe_allow_html=True)

    # Dropdowns list
    dropdowns = [
        {"name": "Report", "icon": "📈", "id": "report"},
        {"name": "Source", "icon": "📁", "id": "source"},
        {"name": "Settings", "icon": "💡", "id": "settings_1"},
        {"name": "Settings", "icon": "⚙️", "id": "settings_2"}
    ]

    for d in dropdowns:
        is_active = (st.session_state.page == d["id"])
        active_class = "sidebar-btn-active" if is_active else "sidebar-btn-inactive"
        st.sidebar.markdown(f'<div class="{active_class}"></div>', unsafe_allow_html=True)
        chevron = "‹" if is_active else "▼"
        if st.sidebar.button(f"{d['icon']}  {d['name']} \u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0 {chevron}", key=f"side_{d['id']}", use_container_width=True):
            st.session_state.page = d["id"]
            st.rerun()

    st.sidebar.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-helper"></div>', unsafe_allow_html=True)
    if st.sidebar.button("🤖  Helper", key="side_helper", use_container_width=True):
        st.session_state.page = "helper"
        st.rerun()

# ---------- Core Routing Layout ----------
def main():
    render_sidebar()
    
    # Query parameters check for Sign In / Log Out
    query_params = st.query_params
    # Handle OAuth callback (Google will return a `code` query parameter)
    if "code" in query_params and not st.session_state.get("authenticated", False):
        code_val = query_params.get("code")
        # streamlit stores query params as lists
        code = code_val[0] if isinstance(code_val, (list, tuple)) else code_val
        user = auth.exchange_code_for_user(code)
        st.query_params.clear()
        if user:
            st.session_state.user = user
            st.session_state.authenticated = True
            st.success(f"Successfully signed in as {user.get('name')}")
            st.rerun()
        else:
            st.error("Google sign-in failed. Please try again.")
            st.rerun()

    if "auth" in query_params:
        if not st.session_state.get("authenticated", False):
            st.session_state.show_auth = True
        st.query_params.clear()
        st.rerun()
        
    if "logout" in query_params:
        st.session_state.user = None
        st.session_state.authenticated = False
        st.session_state.show_auth = False
        st.session_state.google_login_flow = False
        st.session_state.history = []
        st.query_params.clear()
        st.success("Logged out successfully!")
        st.rerun()

    if st.session_state.get("user"):
        st.session_state.authenticated = True
    elif st.session_state.get("authenticated", False):
        st.session_state.authenticated = False
        
    if st.session_state.get("show_auth", False) and not st.session_state.get("authenticated", False):
        st.session_state.show_auth = False
        auth.render_auth_dialog()
    
    # Top Header Bar (Dynamic)
    if "user" in st.session_state and st.session_state.user:
        user = st.session_state.user
        header_html = f"""
        <div class="header-bar">
            <div class="header-left">
            </div>
            <div class="header-right">
                <span style="font-size: 0.95rem; font-weight: 600; color: #cbd5e1;">Hi, {user['name'].split()[0]}</span>
                <a href="?logout=1" target="_self" class="btn-signin" style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;">Log Out</a>
                <div class="user-avatar">
                    <img src="{user['profile_pic']}" alt="User">
                </div>
            </div>
        </div>
        """
    else:
        header_html = """
        <div class="header-bar">
            <div class="header-left">
            </div>
            <div class="header-right">
                <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <a href="?auth=1" target="_self" class="btn-signin">Sign In</a>
                <div class="user-avatar">
                    <img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&q=80&w=256" alt="User">
                </div>
            </div>
        </div>
        """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Page Switcher / Router
    if st.session_state.page == "home":
        pages.render_home_page()
    elif st.session_state.page == "impacts":
        pages.render_impacts_page()
    elif st.session_state.page == "energy":
        pages.render_energy_page()
    elif st.session_state.page == "opencv":
        pages.render_opencv_page()
    elif st.session_state.page == "results":
        pages.render_results_page()
    elif st.session_state.page == "report":
        pages.render_report_page()
    elif st.session_state.page == "source":
        pages.render_source_page()
    elif st.session_state.page in ["settings_1", "settings_2"]:
        pages.render_settings_page()
    elif st.session_state.page == "helper":
        pages.render_helper_page()

if __name__ == "__main__":
    main()