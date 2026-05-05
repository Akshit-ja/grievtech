import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Explainable AI (SHAP)", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Explainable AI (SHAP)")

st.write("### Select Departments")

st.segmented_control(
    "Depts",
    ["Health","Transport","Education","Electricity"],
    selection_mode="single",
    default="Health",
    label_visibility="collapsed"
)

c1, c2 = st.columns([1.5,1])

with c1:

    st.write("#### SHAP values: How each feature contributes to the prediction")

    chart_data = pd.DataFrame({
        'Feature':['Sentiment Score','Previous Count','Urgency','Keywords'],
        'Contribution':[0.4,0.7,0.2,0.5]
    }).set_index('Feature')

    st.bar_chart(chart_data, horizontal=True)

with c2:

    st.write("#### Risk Metrics")

    m1, m2 = st.columns(2)

    m1.metric("Probability of Risk","7.9%",delta="-1.2%")
    m2.metric("Level","Moderate")

    st.write("#### Sentiment Trend Plot")

    trend_data = pd.DataFrame(np.random.randn(20,1),columns=['Sentiment'])

    st.line_chart(trend_data)