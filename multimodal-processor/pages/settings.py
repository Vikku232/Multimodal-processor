import streamlit as st

def render_settings_page():
    st.markdown('<div class="main-title">⚙️ Processor Settings</div>', unsafe_allow_html=True)
    st.write("Modify the default algorithm configurations used by OpenCV and SpaCy pipelines.")
    
    st.markdown("### 🖼&nbsp; OpenCV Settings")
    t1 = st.slider("Canny Lower Threshold", min_value=10, max_value=300, value=st.session_state.canny_t1)
    t2 = st.slider("Canny Upper Threshold", min_value=10, max_value=300, value=st.session_state.canny_t2)
    
    blur_k = st.selectbox(
        "Gaussian Blur Kernel Size",
        options=[3, 5, 7, 9, 11, 13, 15, 17, 19, 21],
        index=[3, 5, 7, 9, 11, 13, 15, 17, 19, 21].index(st.session_state.blur_k)
    )
    
    st.markdown("### 🧠 NLP Settings")
    st.text_input("SpaCy Model Path", value="en_core_web_sm (Preloaded)", disabled=True)
    st.text_input("NLTK Tokenizer Module", value="punkt (Preloaded)", disabled=True)
    
    if st.button("💾 Save Settings"):
        st.session_state.canny_t1 = t1
        st.session_state.canny_t2 = t2
        st.session_state.blur_k = blur_k
        st.success("Settings saved successfully!")
