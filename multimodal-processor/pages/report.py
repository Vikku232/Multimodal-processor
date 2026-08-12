import streamlit as st
import datetime

def render_report_page():
    st.markdown('<div class="main-title">📈 Analytical Report Compiler</div>', unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.warning("⚠️ No logs available to compile. Execute algorithms in the **OpenCV** page first!")
    else:
        st.write("Configure and download a summary report of your multimodal operations.")
        
        report_title = st.text_input("Report Title", value="Multimodal Processing Analytics Report")
        include_logs = st.checkbox("Include detailed history log", value=True)
        
        if st.button("📄 Generate Report Summary"):
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.write(f"### {report_title}")
            st.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**Total Executions:** {len(st.session_state.history)}")
            
            text_runs = len([x for x in st.session_state.history if x["mode"] == "Text"])
            img_runs = len([x for x in st.session_state.history if x["mode"] == "Image"])
            st.write(f"- Text NLP Operations: {text_runs}")
            st.write(f"- OpenCV Image Operations: {img_runs}")
            
            if include_logs:
                st.write("---")
                st.write("**Execution Logs:**")
                for i, run in enumerate(st.session_state.history):
                    st.write(f"{i+1}. [{run['timestamp']}] ({run['mode']}) **{run['action']}**")
                    st.write(f"   *Input:* `{run['input']}`")
                    st.write(f"   *Output:* `{run['output']}`")
            st.markdown('</div>', unsafe_allow_html=True)
