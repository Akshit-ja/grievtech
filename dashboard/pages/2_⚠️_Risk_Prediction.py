import streamlit as st
import random

st.set_page_config(page_title="Risk Prediction", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Complaint Risk Prediction")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        features = st.multiselect(
            "Category",
            ["Health","Transport","Education","Electricity"]
        )

        urgency = st.selectbox("Urgency", ["Low","Medium","High"])

        prev = st.number_input("Previous Complaints", min_value=0)

        if st.button("Predict Risk", type="primary"):

            # ---- SIMPLE LOGIC ----
            score = prev

            if urgency == "High":
                score += 3
            elif urgency == "Medium":
                score += 2
            else:
                score += 1

            if "Health" in features:
                score += 2

            # ---- CLASSIFICATION ----
            if score >= 6:
                risk = "HIGH"
                color = "#ff4b4b"
                escalate = True
            elif score >= 3:
                risk = "MEDIUM"
                color = "#ffa500"
                escalate = False
            else:
                risk = "LOW"
                color = "#4caf50"
                escalate = False

            prob = round(random.uniform(70,95),2)

            st.session_state.result = (risk, prob, escalate, color)

with col2:

    if "result" in st.session_state:

        risk, prob, escalate, color = st.session_state.result

        st.markdown(f"""
        <div style="background-color:#f0f2f6;padding:30px;border-radius:12px;text-align:center;">
            <h2 style="color:{color};">Risk: {risk}</h2>
            <h3>Confidence: {prob}%</h3>
        </div>
        """, unsafe_allow_html=True)

        if escalate:
            st.error("⚠️ Escalation Required")
        else:
            st.success("No escalation needed")