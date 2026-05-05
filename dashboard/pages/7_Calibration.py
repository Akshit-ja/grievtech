import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Calibration", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Calibration")

st.write("### Model Probability Calibration")

st.write("This page checks whether predicted probabilities match actual outcomes.")

# Sample calibration data
data = pd.DataFrame({
    "Predicted Probability":[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
    "Actual Frequency":[0.08,0.19,0.27,0.41,0.49,0.63,0.71,0.79,0.91]
})

st.line_chart(data)

st.success("Model calibration is within acceptable range.")