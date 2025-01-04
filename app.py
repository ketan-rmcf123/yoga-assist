import streamlit as st
import shutil
import time
import os

# Yoga session data
from configs.sn_config import yoga_sessions


model_dir = "./mediapipe"
os.makedirs(model_dir, exist_ok=True)

os.environ["XDG_CACHE_HOME"] = model_dir


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
    st.page_link("app.py", label="Dashboard", icon="🏠")
    st.page_link("pages/find_your_flow.py", label="Learn Yoga", icon="🧘")
    #st.page_link("pages/daily_check.py", label="Daily Practice", icon="🧘")
    st.page_link("pages/daily_practise.py", label="Test Daily Practice", icon="🧘")
    st.page_link("pages/profile.py", label="Profile", icon="👤")
    st.page_link("pages/blank.py", label="Help Centre", icon="❓")
    


# Header
st.page_link("app.py", label="Back to Yogasana", icon=":material/arrow_back:")

st.markdown("# Yoga Practise")
st.markdown("Welcome to your personalized yoga dashboard!\nWe're excited to support you on your path to wellness and inner peace.")

st.markdown("###")
# Main content
cols = st.columns(3, gap = "large", border=True)
for idx, session in enumerate(yoga_sessions):
    with cols[idx]:
        st.markdown(f"### {yoga_sessions[idx]['title']}")
        st.write(yoga_sessions[idx]["summary"],)
        st.image(yoga_sessions[idx]["image"], caption=None, use_container_width =True)
        
        st.markdown(f"- **Streak**: {yoga_sessions[idx]['streak']}\n- **Level**: {yoga_sessions[idx]['level']}")
        
        st.page_link("pages/daily_practise.py", label="Start", icon="🧘")

mp_pose, pose,mp_drawing = load_model()