import streamlit as st
import time
import os
os.environ["MEDIAPIPE_MODEL_COMPLEXITY"] = "0"  # Optional: Adjust model complexity
os.environ["MEDIAPIPE_DATA_DIR"] = "/tmp/mediapipe"


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
from utils.match_function import load_model


with st.sidebar:
    st.title("YogaAssist")
    st.page_link("pages/blank.py", label="Dashboard", icon="🏠")
    st.page_link("pages/find_your_flow.py", label="Learn Yoga", icon="🧘")
    #st.page_link("pages/daily_check.py", label="Daily Practice", icon="🧘")
    st.page_link("pages/daily_practise.py", label="Test Daily Practice", icon="🧘")
    st.page_link("pages/blank.py", label="Profile", icon="👤")
    st.page_link("pages/blank.py", label="Help Centre", icon="❓")
    

with st.spinner("Loadding screen"):
    mp_pose, pose,mp_drawing = load_model()