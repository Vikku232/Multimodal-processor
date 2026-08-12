import streamlit as st
import pandas as pd
import numpy as np

def render_impacts_page():
    st.markdown('<div class="main-title">📊 Performance & Impacts Metrics</div>', unsafe_allow_html=True)
    st.write("Real-time telemetry measuring pipeline executions, latency patterns, and throughput efficiency.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Average Latency</div>
            <div class="metric-value">12 ms</div>
            <div class="metric-trend trend-up">▲ 1.2ms faster than baseline</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">GPU/CPU Throughput</div>
            <div class="metric-value">99.2%</div>
            <div class="metric-trend trend-up">▲ stable thread allocation</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Operations Logged</div>
            <div class="metric-value">2,841</div>
            <div class="metric-trend trend-neutral">■ live execution tracking</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 📈 Processing Time Comparison (ms)")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3) * [4, 1.5, 6] + [12, 8, 22],
        columns=['OpenCV Transform', 'SpaCy Parsing', 'Tokenization']
    )
    st.area_chart(chart_data)
    
    st.markdown("### 📊 Frequency of Executed Algorithms")
    bar_data = pd.DataFrame(
        {
            "Runs": [92, 120, 65, 140, 78, 110, 85, 45],
            "Algorithm": ["Extract Entities", "POS Tagging", "Noun Chunks", "Tokenize Words", "Grayscale", "Edge Detection", "Gaussian Blur", "Invert Colors"]
        }
    ).set_index("Algorithm")
    st.bar_chart(bar_data)

def render_energy_page():
    st.markdown('<div class="main-title">📅 Energy & System Load Scheduler</div>', unsafe_allow_html=True)
    st.write("Monitor carbon emissions and power drawing metrics across active worker instances.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Power Usage (PUE)</div>
            <div class="metric-value">1.14</div>
            <div class="metric-trend trend-up">▲ Energy-efficient tier A</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Instantaneous Draw</div>
            <div class="metric-value">84 Watts</div>
            <div class="metric-trend trend-down">▼ 8 Watts lower load</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Carbon Offsets</div>
            <div class="metric-value">8.42 kg</div>
            <div class="metric-trend trend-up">▲ 0.42kg CO2 offset</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### 🔋 Server Wattage over 24 Hours")
    energy_data = pd.DataFrame(
        np.random.randint(70, 95, size=(24, 1)),
        columns=['Power draw (Watts)']
    )
    st.line_chart(energy_data)
    
    st.markdown("### 🖥️ Node Scheduler Health")
    sched_df = pd.DataFrame([
        {"Node ID": "node-us-east-1", "Uptime": "99.98%", "Power Source": "Green Solar Grid", "Efficiency Index": "9.4/10"},
        {"Node ID": "node-us-west-2", "Uptime": "99.95%", "Power Source": "Hydroelectric", "Efficiency Index": "9.1/10"},
        {"Node ID": "node-eu-central", "Uptime": "100.00%", "Power Source": "Wind Farms", "Efficiency Index": "9.7/10"}
    ])
    st.table(sched_df)
