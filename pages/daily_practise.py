import streamlit as st

st.set_page_config(
    page_title="Yoga Pose Validator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp
import time
from configs.sn_config import stages as suryanamaskar_stages, EXPECTED_ANGLES as angles_config
from utils.match_function import mp_pose, pose, mp_drawing, draw_keypoints
from utils.db_utils import write_to_db,fetch_data,clear_table
import random
from datetime import datetime 
from uuid import uuid4

if "uid" not  in st.session_state:
    st.session_state.uid = str(uuid4)[:10]

frame_rate = 10
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

class KeypointDetector(VideoTransformerBase):
    def __init__(self,asana,write_callback):
        self.asana = asana
        self.write_callback = write_callback
        write_to_db(self.write_callback.uid, self.asana, "Asana started")
        print("Initialized KeypointDetector with asana:", self.asana)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)
            
            if results.pose_landmarks:
                # Draw landmarks and check if the pose matches
                current_angles, match = draw_keypoints(img, angles_config[self.asana]["Angles"])
                if match:
                    write_to_db(self.write_callback.uid, self.asana, "Match Found")
                    self.write_callback.write("Match found {self.asana}")
                    print("Match found")
                    if ctx not in globals or ctx not in locals:
                        ctx.stop()
                        #st.experimental_update()  # Forces rerun to refresh UI
                        print("Stopping webrtc streamer")
                else:
                    write_to_db(self.write_callback.uid, self.asana, "Match Not Found")
        except Exception as e:
            print("Error in transform:", e)

        return img


class Consolewrite():
    def __init__(self):
        self.logs = []
        self.uid = str(uuid4())[:10]

    def write(self,text):
        current_time = datetime.now()

        # Format the time as a string
        time_str = current_time.strftime("%H:%M:%S") 
        self.logs+= time_str+" : " + self.uid +" : "+text

wr = Consolewrite()

# Initialize session state
if "asana_index" not in st.session_state:
    st.session_state.asana_index = 0

st.page_link("pages/blank.py", label="Back to Yogasana", icon=":material/arrow_back:")
st.markdown(
    f"""
    <div class="full-height">
    <h4>Try Step by Step</h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="full-height">
    <h12>Give it a try yourself.Your motion guide will be there to help you and suggest any necessary adjustments.Once you master a pose, you will be smoothly guided to the next step.Enjoy your practice!</h12>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr style='border: 1px solid #f0f2f6;'>", unsafe_allow_html=True)

# Navigation Buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("Previous", disabled=st.session_state.asana_index == 0):
        st.session_state.asana_index -= 1
        st.rerun()

with col3:
    if st.button("Next", disabled=st.session_state.asana_index == len(suryanamaskar_stages) - 1):
        st.session_state.asana_index += 1
        st.rerun()

# Progress bar
st.title("Suryanamaskar Progress Tracker")
progress = (st.session_state.asana_index + 1) / len(suryanamaskar_stages)
progress_bar = st.progress(progress)


# Layout with two columns
col1, col2 = st.columns(2)

# Asana Display and Navigation
with col1:
    st.markdown(
        f"""
        <div class="full-height">
        <h6>Motion guide</h6>
        </div>
        """,
        unsafe_allow_html=True
    )
    asana_placeholder = st.empty()
    asana_placeholder.markdown(f"### {st.session_state.asana_index} {suryanamaskar_stages[st.session_state.asana_index][1]}")
        
    def video_transformer_factory(asana=suryanamaskar_stages[st.session_state.asana_index][1],write_callback = wr):
        return KeypointDetector(asana,write_callback)
    
    ctx = webrtc_streamer(key="asana_validator", 
                          video_transformer_factory=video_transformer_factory,
                          media_stream_constraints={
                                "video": {"frameRate": {"ideal": frame_rate}}}
                        )
                        
    
@st.fragment(run_every=10)
def write_notes():
    print(wr.logs)
    # Streamlit app
    st.write("Database Records Viewer")
    fcol1,fcol2 = st.columns(2)  
    # Display database records
    with fcol1:
        lt_button = st.button("Load Table")
        if lt_button:
            data = fetch_data()
            if not data.empty:
                df = st.dataframe(data)  # Display data as a table with interactive features
            else:
                st.write("No records found.")
        else:
            data = fetch_data()
            if not data.empty:
                df = st.dataframe(data)  # Display data as a table with interactive features
            else:
                st.write("No records found.")
    with fcol2:
        if st.button("Refresh Table"):
            clear_table()

# Notes Textbox
with col2:
    st.header("Notes")
    #notes = st.text_area("Enter your notes here", height=200)
    write_notes()

