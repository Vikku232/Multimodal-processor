import streamlit as st
import auth
import time

# Simple loading page config
st.set_page_config(page_title="Signing in...", layout="wide")

# Show a loading spinner
with st.spinner("Signing in with Google, please wait..."):
    query_params = st.query_params
    if "code" in query_params:
        code_val = query_params.get("code")
        code = code_val[0] if isinstance(code_val, (list, tuple)) else code_val
        
        user = auth.exchange_code_for_user(code)
        if user:
            st.session_state.user = user
            st.session_state.authenticated = True
            st.session_state.page = "opencv"
            
            # Use javascript to redirect the parent window to the home page (removing code from URL)
            st.markdown(
                '<script>window.parent.location.href = "http://localhost:8501/";</script>',
                unsafe_allow_html=True
            )
            st.success("Successfully logged in!")
            time.sleep(1)
        else:
            st.error("Google authentication failed. Please try again.")
            if st.button("Go back to Sign In"):
                st.markdown(
                    '<script>window.parent.location.href = "http://localhost:8501/?auth=1";</script>',
                    unsafe_allow_html=True
                )
    else:
        st.warning("No authentication code found.")
        if st.button("Go to Home"):
            st.markdown(
                '<script>window.parent.location.href = "http://localhost:8501/";</script>',
                unsafe_allow_html=True
            )
