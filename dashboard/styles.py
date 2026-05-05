import streamlit as st

def apply_styles():

    st.markdown("""
    <style>

    /* page background */
    .stApp{
        background-color:#d8f3dc;
    }

    /* government header */
    .gov-header{
        background:#7b0f2b;
        color:white;
        padding:8px;
        font-size:14px;
        font-weight:500;
    }

    /* page title */
    .page-title{
        color:black;
        font-size:32px;
        font-weight:800;
        margin-top:10px;
        margin-bottom:20px;
    }

    /* card container */
    .card{
        background:white;
        padding:20px;
        border-radius:8px;
        box-shadow:0px 2px 6px rgba(0,0,0,0.1);
        margin-bottom:15px;
    }

    section[data-testid="stSidebar"]{
        background:#ffffff;
        border-right:1px solid #ddd;
    }

    </style>
    """,unsafe_allow_html=True)



def gov_header():

    st.markdown("""
    <div class='gov-header'>
    🇮🇳 Government of India | Ministry of Public Grievances
    </div>
    """,unsafe_allow_html=True)



def page_title(title):

    st.markdown(
        f"<div class='page-title'>{title}</div>",
        unsafe_allow_html=True
    )