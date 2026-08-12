import streamlit as st

def render_helper_page():
    st.markdown('<div class="main-title">🤖 Dashboard Helper</div>', unsafe_allow_html=True)
    st.write("Learn how to operate the Multimodal Processor UI or configure custom presets.")
    
    st.markdown("""
    ### 💡 Quickstart Guide
    1. **Page Selection**: Use the left sidebar to navigate. The primary work area is **OpenCV**.
    2. **Text Processing**: In the OpenCV workspace, open the `Input Text Mode` tab, type your sentence, and click one of the first row of buttons (e.g. *Extract Entities*).
    3. **Image Processing**: Switch to the `Image (OpenCV)` tab, upload an image or use the default Nikon sample, then click one of the CV actions (e.g. *Edge Detection*).
    4. **Telemetry**: View real-time efficiency charts under the **Impacts** and **Energy** tabs.
    5. **History**: Track and export execution logs under **Results** and **Report**.
    """)
