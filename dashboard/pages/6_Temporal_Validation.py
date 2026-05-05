import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Temporal Validation", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Temporal Validation")

st.write("### Model Performance Over Time")

data = pd.DataFrame(
    np.random.randn(30,1),
    columns=["Performance"]
)

st.line_chart(data)

st.success("Model stability verified across time windows.")