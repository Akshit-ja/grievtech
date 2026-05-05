import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Drift Monitoring", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Drift Monitoring")

st.write("### Feature Distribution Drift")

data = pd.DataFrame(np.random.randn(50,2),columns=["Baseline","Live"])

st.line_chart(data)

st.warning("No significant drift detected.")