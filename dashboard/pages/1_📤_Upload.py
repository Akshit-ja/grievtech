import streamlit as st
import pandas as pd
import uuid
import os
from datetime import datetime

st.set_page_config(page_title="Upload Complaint", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Upload Complaint")

# ---- INPUTS ----
with st.container(border=True):

    st.subheader("Citizen Name")
    name = st.text_input("Name", label_visibility="collapsed")

    st.subheader("Department")
    dept = st.selectbox("Dept", ["Health","Transport","Education","Electricity"])

    st.subheader("Location / Borough")
    borough = st.selectbox("Borough", ["North","South","East","West","Central"])

    st.subheader("Previous Complaints")
    count = st.number_input("Count", min_value=0, step=1, label_visibility="collapsed")

    st.subheader("Complaint Description")
    keywords = st.text_area("Enter complaint...", label_visibility="collapsed")

    if st.button("Submit Complaint", type="primary"):

        if name == "" or keywords == "":
            st.error("Please fill all fields")
        else:
            complaint_id = "GRV-" + str(uuid.uuid4())[:8].upper()

            # ---- CREATE DATA ----
            data = {
                "id": complaint_id,
                "agency": dept,
                "borough": borough,
                "month": datetime.now().month,
                "year": datetime.now().year,
                "text": keywords,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            df = pd.DataFrame([data])

            # ---- SAVE CSV ----
            os.makedirs("logs", exist_ok=True)

            file_path = "logs/complaints.csv"

            if os.path.exists(file_path):
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(file_path, index=False)

            st.success("Complaint Submitted Successfully ✅")
            st.info(f"Complaint ID: {complaint_id}")