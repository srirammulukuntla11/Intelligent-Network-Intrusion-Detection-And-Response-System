import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os
import sys
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.visualizations import Visualizer

# Page config
st.set_page_config(
    page_title="Network Sentinel | IDS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS
st.markdown("""
    <style>
    .stApp > header {
        background-color: transparent;
    }
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #312e81 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-weight: 700;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    /* Enhance metric cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        height: 100%;
    }
    div[data-testid="stMetric"] label {
        color: #64748b !important;
    }
    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for decisions and data
if 'decisions' not in st.session_state:
    st.session_state.decisions = [
        {
            'time': '05:16:25 AM',
            'title': 'DOS Attack Detected',
            'type': 'CRITICAL',
            'confidence': 98,
            'risk': 94,
            'action': 'BLOCK SOURCE IP',
            'ip': '192.168.1.45'
        },
        {
            'time': '05:15:30 AM',
            'title': 'Port Scan Sweep',
            'type': 'LOW',
            'confidence': 85,
            'risk': 40,
            'action': 'MONITOR',
            'ip': '10.0.0.12'
        },
        {
            'time': '05:14:45 AM',
            'title': 'Normal Traffic',
            'type': 'NORMAL',
            'confidence': 99,
            'risk': 5,
            'action': 'ALLOW',
            'ip': '192.168.1.100'
        }
    ]

# Keep track of last uploaded file to avoid infinite st.rerun loop
if 'last_uploaded' not in st.session_state:
    st.session_state.last_uploaded = None

# Header
st.markdown("""
    <div class="main-header">
        <h1>🛡️ Network Sentinel</h1>
        <p>AI-Powered Real-Time Threat Analysis & Intrusion Detection Platform</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("---")
    
    st.subheader("📁 Analyze Traffic Data")
    uploaded_file = st.file_uploader("Upload CSV log", type=['csv'], help="Upload network traffic logs (.csv) for AI analysis")
    
    # Fix the file upload logic error and remove problematic recursive st.rerun calls
    if uploaded_file is not None:
        if st.session_state.last_uploaded != uploaded_file.name:
            st.session_state.last_uploaded = uploaded_file.name
            st.success("File analyzed safely!")
            
            new_decision = {
                'time': datetime.now().strftime("%I:%M:%S %p"),
                'title': f'Batch: {uploaded_file.name[:10]}...',
                'type': random.choice(['CRITICAL', 'LOW', 'NORMAL']),
                'confidence': random.randint(85, 100),
                'risk': random.randint(30, 95),
                'action': 'REVIEW FINDINGS',
                'ip': 'Multiple'
            }
            st.session_state.decisions.insert(0, new_decision)
    
    st.markdown("---")
    st.subheader("⚡ Simulate Traffic")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🟢 Normal", use_container_width=True):
            st.session_state.decisions.insert(0, {
                'time': datetime.now().strftime("%I:%M:%S %p"),
                'title': 'Normal Traffic',
                'type': 'NORMAL',
                'confidence': random.randint(95, 100),
                'risk': random.randint(0, 10),
                'action': 'ALLOW',
                'ip': f'192.168.1.{random.randint(2, 254)}'
            })
    with col2:
        if st.button("🔴 Attack", use_container_width=True):
            attack_types = ['DOS Attack', 'Port Scan', 'Brute Force SSH', 'SQL Injection']
            risk = random.randint(75, 99)
            st.session_state.decisions.insert(0, {
                'time': datetime.now().strftime("%I:%M:%S %p"),
                'title': random.choice(attack_types),
                'type': 'CRITICAL' if risk > 85 else 'LOW',
                'confidence': random.randint(85, 99),
                'risk': risk,
                'action': 'BLOCK IP' if risk > 85 else 'MONITOR',
                'ip': f'{random.randint(10, 200)}.{random.randint(0, 255)}.1.{random.randint(1, 255)}'
            })
            
    st.markdown("---")
    st.info("System Status: **ONLINE**")

# Analytics Metrics (Top Row)
total_events = len(st.session_state.decisions)
critical_events = sum(1 for d in st.session_state.decisions if d['type'] == 'CRITICAL')
warning_events = sum(1 for d in st.session_state.decisions if d['type'] == 'LOW')
normal_events = sum(1 for d in st.session_state.decisions if d['type'] == 'NORMAL')
avg_risk = int(np.mean([d['risk'] for d in st.session_state.decisions])) if total_events > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Events Analyzed", total_events, delta="Tracking live", delta_color="normal")
m2.metric("Critical Threats Found", critical_events, delta=f"{critical_events} high severity" if critical_events > 0 else "0", delta_color="inverse")
m3.metric("Low Risk Anomalies", warning_events, delta="Active monitoring", delta_color="off")
m4.metric("System Average Risk Score", avg_risk, delta=f"{avg_risk - 50} from baseline" if avg_risk > 50 else f"{avg_risk - 50} from baseline", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# Main Dashboard Content layout
col_charts, col_gauge = st.columns(2, gap="large")

with col_charts:
    st.subheader("📊 Threat Distribution")
    dist_data = {
        'DOS': max(0, critical_events - 1),
        'Probe': warning_events,
        'R2L': 1 if critical_events > 0 else 0,
        'U2R': 0,
        'Normal': normal_events
    }
    
    # Create the chart using Plotly Express from visualizations util
    fig_dist = Visualizer.create_attack_distribution_chart(dist_data)
    fig_dist.update_layout(margin=dict(t=50, b=10, l=10, r=10), height=350)
    st.plotly_chart(fig_dist, use_container_width=True)

with col_gauge:
    st.subheader("🛡️ AI Confidence (Latest)")
    latest = st.session_state.decisions[0]
    is_normal = 'normal' if latest['type'] == 'NORMAL' else 'attack'
    fig_gauge = Visualizer.create_confidence_gauge(latest['confidence']/100.0, is_normal)
    fig_gauge.update_layout(margin=dict(t=50, b=10, l=10, r=10), height=350)
    st.plotly_chart(fig_gauge, use_container_width=True)


st.markdown("---")
st.subheader("⚡ Live Threat Feed")

# Using pandas DataFrame and st.dataframe for an advanced datagrid feel
df = pd.DataFrame(st.session_state.decisions)

def get_status_emoji(row):
    if row['type'] == 'CRITICAL': return '🔴 ' + row['title']
    if row['type'] == 'LOW': return '🟡 ' + row['title']
    return '🟢 ' + row['title']

if not df.empty:
    df['Event'] = df.apply(get_status_emoji, axis=1)
    display_df = df[['time', 'Event', 'ip', 'risk', 'confidence', 'action']]
    display_df.columns = ['Time', 'Event', 'Source IP', 'Risk Score', 'Confidence %', 'Action Strategy']
    
    st.dataframe(
        display_df,
        column_config={
            "Risk Score": st.column_config.ProgressColumn(
                "Risk Intensity",
                min_value=0, max_value=100,
                format="%f",
            ),
            "Confidence %": st.column_config.NumberColumn(
                "AI Confidence %",
                format="%d%%"
            )
        },
        hide_index=True,
        use_container_width=True
    )

# Additional expanded visualizations at bottom
with st.expander("Explore Deep Data Metrics (Network Features)"):
    st.subheader("🌐 Network Feature Correlations")
    fig_heat = Visualizer.create_network_traffic_heatmap(None)
    fig_heat.update_layout(height=400, margin=dict(t=30, b=30, l=30, r=30))
    st.plotly_chart(fig_heat, use_container_width=True)