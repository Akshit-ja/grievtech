import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="GrievTech Pro",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# Custom Styling
# --------------------------------
st.markdown("""
<style>
.main {
    background-color: #f4f7fa;
}
h1, h2, h3 {
    color: #1f2937;
}
.hero-box {
    padding: 40px;
    border-radius: 20px;
    background: linear-gradient(135deg, #2563eb, #1e3a8a);
    color: white;
    text-align: center;
}
.feature-card {
    padding: 25px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# Sidebar
# --------------------------------
st.sidebar.title("📊 GrievTech Pro")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Dashboard Overview", "Explainability", "Drift Monitoring"]
)

# --------------------------------
# Sample Data
# --------------------------------
feature_data = pd.DataFrame({
    "Feature": ["Borough", "Agency", "Month", "Year", "Text Score"],
    "Importance": [0.32, 0.27, 0.18, 0.12, 0.11]
})

drift_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Drift Score": [0.12, 0.18, 0.22, 0.35, 0.41, 0.38]
})

# ============================================
# HOME PAGE
# ============================================
if page == "Home":

    st.markdown("""
    <div class="hero-box">
        <h1>Intelligent Grievance Monitoring System</h1>
        <p>Production-Ready Machine Learning with Explainability & Drift Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚀 System Overview")

    st.write("""
    This system is designed to classify and monitor grievance data using
    machine learning models integrated with explainability and drift detection.
    It follows modern MLOps practices to ensure transparency, reliability,
    and long-term performance stability.
    """)

    st.markdown("## 🔥 Core Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>📊 Multi-Page Dashboard</h3>
        <p>Interactive monitoring interface with real-time metrics and modular design.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>🔍 Explainable AI</h3>
        <p>Feature importance analysis to ensure transparency and decision interpretability.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3>📈 Drift Monitoring</h3>
        <p>Continuous tracking of data distribution shifts to detect model degradation.</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# DASHBOARD OVERVIEW
# ============================================
elif page == "Dashboard Overview":

    st.title("📊 System Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Predictions", "1,248")
    col2.metric("Model Accuracy", "92%")
    col3.metric("Drift Alert", "False")

    st.markdown("---")
    st.write("This dashboard summarizes model performance and operational health.")

# ============================================
# EXPLAINABILITY PAGE
# ============================================
elif page == "Explainability":

    st.title("🔍 Feature Importance Analysis")

    fig, ax = plt.subplots()
    ax.bar(feature_data["Feature"], feature_data["Importance"])
    ax.set_ylabel("Importance Score")
    ax.set_title("Feature Importance")
    plt.xticks(rotation=30)

    st.pyplot(fig)

    st.write("""
    Feature importance highlights which variables most strongly influence
    the model's prediction decisions, improving transparency and trust.
    """)

# ============================================
# DRIFT MONITORING PAGE
# ============================================
elif page == "Drift Monitoring":

    st.title("📈 Drift Score Trend")

    fig, ax = plt.subplots()
    ax.plot(drift_data["Month"], drift_data["Drift Score"], marker='o')
    ax.set_ylabel("Drift Score")
    ax.set_title("Drift Score Over Time")

    st.pyplot(fig)

    st.write("""
    Drift scores measure changes in input data distribution over time.
    Increasing values may indicate model performance degradation,
    enabling proactive system maintenance.
    """)