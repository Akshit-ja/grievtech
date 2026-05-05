import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

from auth_utils import login, signup
from styles import apply_styles, gov_header, page_title

# -------------------------------------------------
# CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="GrievTech",
    page_icon="🏛️",
    layout="wide"
)

apply_styles()
st.markdown("""
<style>

/* 🌌 Animated Gradient Background */
.stApp {
    background: linear-gradient(135deg, #e6fff5, #ccf5e6, #b3f0d9);
    background-size: 200% 200%;
    animation: gradientBG 10s ease infinite;
    color: #003333;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* 🧊 Glass Cards */
[data-testid="stMetric"], .stAlert, .stDataFrame, .stPlotlyChart {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(10px);
    border-radius: 18px;
    padding: 15px;
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

/* Hover Animation */
[data-testid="stMetric"]:hover,
.stPlotlyChart:hover,
.stAlert:hover {
    transform: scale(1.03);
}

/* ✨ Section Titles Glow */
h1, h2, h3 {
    text-shadow: 0 0 12px rgba(0,255,255,0.7);
    font-weight: 700;
}

/* 📦 Feature Boxes */
.stInfo {
    background: rgba(0, 200, 255, 0.1) !important;
    border-left: 4px solid cyan !important;
    border-radius: 12px;
    transition: 0.3s;
}

.stInfo:hover {
    transform: translateY(-5px);
    background: rgba(0, 200, 255, 0.2) !important;
}

/* 🚨 Alerts */
.stError {
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% {box-shadow: 0 0 0 0 rgba(255,0,0,0.5);}
    70% {box-shadow: 0 0 0 15px rgba(255,0,0,0);}
    100% {box-shadow: 0 0 0 0 rgba(255,0,0,0);}
}

/* 📊 Plot Glow */
.stPlotlyChart {
    border: 1px solid rgba(0,255,255,0.2);
}

/* 🗺️ Map Styling */
iframe {
    border-radius: 15px !important;
    overflow: hidden;
}

/* 🚀 Smooth Fade-In */
section {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

/* 🎯 Buttons (Login Page also enhanced) */
.stButton>button {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #ff512f, #dd2476);
}

/* ✨ Divider Glow */
hr {
    border: 1px solid rgba(0,255,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------------------------
# LOGIN PAGE (UNCHANGED)
# -------------------------------------------------

if not st.session_state.logged_in:

    page_title("GrievTech")

    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display:none;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        "<h3 style='text-align:center;'>AI Powered Public Grievance Intelligence Platform</h3>",
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            if login(email, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_email = st.text_input("Create Email")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Create Account"):
            if signup(new_email, new_pass):
                st.success("Account created successfully")
            else:
                st.error("User already exists")

    st.stop()

# -------------------------------------------------
# HEADER
# -------------------------------------------------

page_title("GrievTech – National AI Grievance Intelligence Portal")

st.caption("AI Powered Public Grievance Intelligence Platform")

st.divider()
st.markdown("""
<div style='text-align:center; padding: 20px;'>
    <h1 style='font-size:50px;'>🧠 AI Governance Dashboard</h1>
    <p style='font-size:18px; color:lightgray;'>
    Real-time Intelligence • Predictive Analytics • National Scale Monitoring
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 🧠 FEATURE OVERVIEW (NEW SECTION)
# -------------------------------------------------

st.title("🚀 GrievTech System Overview")

st.markdown("""
GrievTech is an AI-powered grievance intelligence platform designed to streamline complaint handling, 
predict risk levels, and assist authorities in proactive decision-making.

### 🔹 Core Features:
""")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    📥 **Complaint Upload System**  
    Citizens can submit grievances with structured data and keywords.  
    Each complaint is assigned a unique ID for tracking.
    """)

    st.info("""
    ⚡ **AI Risk Prediction Engine**  
    Uses machine learning to classify complaints into Low, Medium, or High risk.  
    Helps prioritize critical cases instantly.
    """)

    st.info("""
    🚨 **Escalation Detection**  
    Automatically flags high-risk complaints requiring urgent attention.
    """)

with col2:
    st.info("""
    📊 **Performance Monitoring Dashboard**  
    Tracks model accuracy, system metrics, and complaint trends in real time.
    """)

    st.info("""
    📉 **Drift Detection System**  
    Detects changes in incoming data patterns and alerts for retraining.
    """)

    st.info("""
    ⭐ **Citizen Feedback System**  
    Collects user feedback to improve service quality and model performance.
    """)

st.divider()

# -------------------------------------------------
# 📊 DASHBOARD METRICS (UNCHANGED)
# -------------------------------------------------

st.title("📊 National Grievance AI Command Center")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Complaints Today", "126", "+8")
col2.metric("High Risk Cases", "34", "+3")
col3.metric("Model Accuracy", "92%", "+1.1%")
col4.metric("System Status", "Operational")

st.divider()

# -------------------------------------------------
# 🚨 ALERT PANEL (UNCHANGED)
# -------------------------------------------------

st.subheader("🚨 AI System Alerts")

DRIFT_LOG = "logs/drift_log.csv"

if os.path.exists(DRIFT_LOG):

    log = pd.read_csv(DRIFT_LOG)

    if len(log) > 0:

        latest = log.iloc[-1]

        if latest["status"] == "Drift Detected":
            st.error("⚠️ Alert: Data drift detected. Model retraining may be required.")
        else:
            st.success("✅ AI model operating normally")

    else:
        st.info("No drift alerts recorded yet")

else:
    st.info("No drift alerts recorded yet")

st.divider()

# -------------------------------------------------
# 📨 LATEST COMPLAINT (UNCHANGED)
# -------------------------------------------------

st.subheader("📨 Latest Citizen Complaint")

LOG_FILE = "logs/complaints.csv"

if os.path.exists(LOG_FILE):

    df = pd.read_csv(LOG_FILE)

    if len(df) > 0:

        latest = df.iloc[-1]

        st.write("Complaint ID:", latest["id"])
        st.write("Department:", latest["agency"])
        st.write("Location:", latest["borough"])
        st.write("Description:", latest["text"])

    else:
        st.warning("No complaints submitted yet")

else:
    st.warning("Complaint database not found")

st.divider()

# -------------------------------------------------
# 📈 TREND (UNCHANGED)
# -------------------------------------------------

st.subheader("📈 Complaint Trend Monitoring")

dates = pd.date_range(end=pd.Timestamp.today(), periods=30)

trend_df = pd.DataFrame({
    "Date": dates,
    "Complaints": np.random.randint(80, 150, 30)
})

fig = px.line(trend_df, x="Date", y="Complaints", markers=True)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 📊 RISK DISTRIBUTION (UNCHANGED)
# -------------------------------------------------

st.subheader("Complaint Risk Distribution")

risk_data = pd.DataFrame({
    "Risk Level": ["Low", "Medium", "High"],
    "Cases": [120, 60, 25]
})

fig = px.bar(
    risk_data,
    x="Risk Level",
    y="Cases",
    color="Risk Level"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 🧠 ANOMALY DETECTION (UNCHANGED)
# -------------------------------------------------

st.subheader("AI Anomaly Detection")

data = np.random.normal(50, 10, 100)
data[::10] += 40

anomaly_df = pd.DataFrame({
    "Index": range(100),
    "Value": data
})

fig = px.scatter(anomaly_df, x="Index", y="Value")

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# 🗺️ HEATMAP (UNCHANGED)
# -------------------------------------------------

st.subheader("Live Complaint Heatmap")

map_data = pd.DataFrame({
    "lat": np.random.uniform(40.65, 40.85, 200),
    "lon": np.random.uniform(-74.05, -73.75, 200)
})

st.map(map_data)