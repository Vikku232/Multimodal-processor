import streamlit as st

def render_source_page():
    st.markdown('<div class="main-title">📁 App Source Code Viewer</div>', unsafe_allow_html=True)
    st.write("Inspect the files powering this dashboard:")
    
    tabs = st.tabs(["🐍 app.py", "💾 db.py", "🔑 auth.py", "🎨 style.css"])
    
    with tabs[0]:
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                content = f.read()
            st.code(content, language="python")
        except Exception as e:
            st.error(f"Could not load app.py: {e}")
            
    with tabs[1]:
        try:
            with open("db.py", "r", encoding="utf-8") as f:
                content = f.read()
            st.code(content, language="python")
        except Exception as e:
            st.error(f"Could not load db.py: {e}")
            
    with tabs[2]:
        try:
            with open("auth.py", "r", encoding="utf-8") as f:
                content = f.read()
            st.code(content, language="python")
        except Exception as e:
            st.error(f"Could not load auth.py: {e}")
            
    with tabs[3]:
        try:
            with open("style.css", "r", encoding="utf-8") as f:
                content = f.read()
            st.code(content, language="css")
        except Exception as e:
            st.error(f"Could not load style.css: {e}")
