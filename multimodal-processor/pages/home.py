import streamlit as st

def render_home_page():
    st.markdown('<div class="main-title">✨ Welcome to Multimodal Processor ✨</div>', unsafe_allow_html=True)
    
    st.write(
        "A highly-polished Streamlit dashboard designed to showcase natural language processing (NLP) and computer vision (CV) algorithms. "
        "Select **OpenCV** from the sidebar to test real-time image processing and textual semantic extraction."
    )
    
    st.markdown("### 📊 Engine Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Active Algorithms</div>
            <div class="metric-value">8 Engines</div>
            <div class="metric-trend trend-up">▲ CV & NLP operational</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">NLP Framework</div>
            <div class="metric-value">SpaCy 3.7</div>
            <div class="metric-trend trend-neutral">■ model: en_core_web_sm</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Computer Vision</div>
            <div class="metric-value">OpenCV 4.10</div>
            <div class="metric-trend trend-up">▲ Headless optimization active</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🛠&nbsp; Core Capabilities")
    
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    with col_feat1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">
                <span class="feature-icon">🧠</span>
                <span class="feature-title">NLP Pipeline</span>
            </div>
            <div class="feature-desc">Extract named entities (organizations, locations), tags parts-of-speech (nouns, verbs, adjectives), segment noun chunks, and perform word tokenization.</div>
            <span class="feature-tag">SpaCy + NLTK</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_feat2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">
                <span class="feature-icon">👁️</span>
                <span class="feature-title">Image Processing</span>
            </div>
            <div class="feature-desc">Perform grayscale conversion, extract fine edges with Canny edge detection, apply Gaussian filters to reduce noise, and invert channel pixel values.</div>
            <span class="feature-tag">OpenCV</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_feat3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-header">
                <span class="feature-icon">📁</span>
                <span class="feature-title">History Logging</span>
            </div>
            <div class="feature-desc">Automatically tracks all ran algorithms, parameter settings, input states, and outputs in an active history view for easy comparison and exports.</div>
            <span class="feature-tag">Session State</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Open Workspace / OpenCV Mode", use_container_width=True):
        st.session_state.page = "opencv"
        st.rerun()
