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

st.markdown("# Suryanamaskar")
st.markdown("Embark on a transformative journey with our Surya Namaskar Asana flow designed to elevate your mind, body and spirit. \n \
            Our program is structured into three progressive levels,each unlocking new depth of practice and udnerstanding")

st.markdown("###")
# Main content
cols = st.columns(len(yoga_sessions[0]["subpage"]), gap = "large", border=True)
for idx in range(len(yoga_sessions[0]["subpage"])):
    with cols[idx]:
        st.markdown(f"### {yoga_sessions[0]['subpage'][idx]['title']}")
        st.write(yoga_sessions[0]["subpage"][idx]["summary"],)
        st.image(yoga_sessions[0]["subpage"][idx]["image"], caption=None, use_container_width =True)
                
        st.page_link(yoga_sessions[0]["subpage"][idx]["page_link"], label="Start", icon="🧘")

