import streamlit as st

st.set_page_config(page_title="Citizen Feedback", layout="wide")

def draw_header(title):
    st.markdown(f"""
        <div style="background-color:#1e3c72;padding:12px;color:white;text-align:center;font-size:22px;font-weight:600;">
        {title}
        </div><br>
    """, unsafe_allow_html=True)

draw_header("Citizen Feedback")

with st.container(border=True):

    st.subheader("Citizen Name")
    name = st.text_input("Enter Name", label_visibility="collapsed")

    st.subheader("Complaint ID")
    cid = st.text_input("Complaint ID", label_visibility="collapsed")

    st.subheader("⭐ Rate Your Experience")

    rating = st.radio(
        "",
        ["😡 Very Bad", "😕 Bad", "😐 Average", "😊 Good", "😍 Excellent"],
        horizontal=True
    )

    st.subheader("Feedback Comments")

    feedback = st.text_area(
        "Feedback",
        placeholder="Enter feedback here...",
        label_visibility="collapsed"
    )

    if st.button("Submit Feedback", type="primary"):
        st.success("Thank you for your feedback!")