import streamlit as st
import pandas as pd
import db

def render_results_page():
    st.markdown('<div class="main-title">❓ Execution Results History</div>', unsafe_allow_html=True)
    
    if "user" not in st.session_state or not st.session_state.user:
        st.warning("⚠️ Access Denied: Please Sign In to view your execution history.")
        return
        
    user_email = st.session_state.user.get("email")
    # Load history from DB specifically for this user
    user_history = db.load_history_from_db(user_email)
    
    if not user_history:
        st.info("📜 No operations executed yet. Switch to the **OpenCV** page to process text or images!")
    else:
        st.write(f"Showing execution history for **{user_email}**:")
        
        if st.button("🧹 Clear History"):
            if db.clear_history_db(user_email):
                st.success("History cleared!")
                st.rerun()
            else:
                st.error("Failed to clear database logs.")
            
        hist_df = pd.DataFrame(user_history)
        st.dataframe(hist_df, use_container_width=True)
