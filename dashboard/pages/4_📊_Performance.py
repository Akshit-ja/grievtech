import streamlit as st

st.set_page_config(page_title="Model Performance", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Model Performance")

c1, c2, c3 = st.columns(3)

c1.metric("Accuracy","92%","+2%")
c2.metric("Precision","89%","+1%")
c3.metric("Recall","90%","+1.5%")

st.progress(0.92)