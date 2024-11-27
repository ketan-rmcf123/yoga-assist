import streamlit as st
import time
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.title("YogaAssist")
    st.page_link("pages/blank.py", label="Dashboard", icon="🏠")
    st.page_link("pages/find_your_flow.py", label="Learn Yoga", icon="🧘")
    #st.page_link("pages/daily_check.py", label="Daily Practice", icon="🧘")
    st.page_link("pages/daily_practise.py", label="Test Daily Practice", icon="🧘")
    st.page_link("pages/blank.py", label="Profile", icon="👤")
    st.page_link("pages/blank.py", label="Help Centre", icon="❓")
    
