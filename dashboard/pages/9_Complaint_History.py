import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Complaint History", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Complaint History")

st.write("### Submitted Complaints")

file_path = "logs/complaints.csv"

if os.path.exists(file_path):

    df = pd.read_csv(file_path)

    if df.empty:
        st.info("No complaints available.")

    else:
        df = df[::-1]

        for _, row in df.iterrows():

            with st.container(border=True):

                st.write(f"**Complaint ID:** {row['id']}")
                st.write(f"**Department:** {row['agency']}")
                st.write(f"**Location:** {row['borough']}")
                st.write(f"**Date:** {row['month']}/{row['year']}")
                st.write(f"**Complaint:** {row['text']}")
                st.write(f"**Submitted At:** {row['timestamp']}")

else:
    st.warning("No complaints found. Submit one first.")