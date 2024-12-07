"""A sample to configure MediaStreamConstraints object"""
import streamlit as st

st.set_page_config(
    page_title="Yoga Pose Validator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from io import BytesIO
from PIL import Image
import streamlit as st
import numpy as np

from typing import List, NamedTuple
from configs.sn_config import stages as suryanamaskar_stages, EXPECTED_ANGLES as angles_config
from utils.match_function import pose, draw_keypoints
from utils.db_utils import MatchResult
from uuid import uuid4
import queue,av


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


if "uid" not  in st.session_state:
    st.session_state.uid = str(uuid4())[:10]
    print("uid",st.session_state.uid)


frame_rate = 10
def processor(uid,asana) -> av.VideoFrame:
    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)
            
            if results.pose_landmarks:
                # Draw landmarks and check if the pose matches
                current_angles, match = draw_keypoints(img, angles_config[asana]["Angles"])
                if match:
                    write_to_queue(uid, asana, "Match Found")
                    #print(result_queue.qsize())
                else:
                    write_to_queue(uid, asana, "Match Not Found")
                    #print(result_queue.qsize())
            
            last_three = list(result_queue.queue)[-3:]
            #print(last_three)
        except Exception as e:
            print("Error in transform:", e)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
    return video_frame_callback

class KeypointDetector(VideoTransformerBase):
    def __init__(self,id,asana):
        self.uid = id
        self.asana = asana
        write_to_queue(self.uid, self.asana, "Asana started")
        print(result_queue.qsize())
        print("Initialized KeypointDetector with asana:", self.asana)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)
            
            if results.pose_landmarks:
                # Draw landmarks and check if the pose matches
                current_angles, match = draw_keypoints(img, angles_config[self.asana]["Angles"])
                if match:
                    write_to_queue(self.uid, self.asana, "Match Found")
                    #print(result_queue.qsize())
                else:
                    write_to_queue(self.uid, self.asana, "Match Not Found")
                    #print(result_queue.qsize())
            
            last_three = list(result_queue.queue)[-3:]
            #print(last_three)
        except Exception as e:
            print("Error in transform:", e)

        return img

# Initialize session state
if "asana_index" not in st.session_state:
    st.session_state.asana_index = 0

st.page_link("pages/blank.py", label="Back to Yogasana", icon=":material/arrow_back:")
st.markdown(
    f"""
    <div class="full-height">
    <h4>Suryanamaskar Pose Tracker : Try Step by Step</h4>
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
progress = (st.session_state.asana_index + 1) / len(suryanamaskar_stages)
progress_bar = st.progress(progress)
playing = st.checkbox("Playing Validator", value=True)

# Layout with two columns
col1, col2 = st.columns(2)


with col1:
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Live Camera feed", disabled=not enable)

    if picture is not None:
        # Read image using Pillow
        image = Image.open(BytesIO(picture.getvalue()))
        np_image = np.asarray(image)
        results = pose.process(np_image)
        if results.pose_landmarks:
            # Draw landmarks and check if the pose matches
            current_angles, match = draw_keypoints(np_image, angles_config[self.asana]["Angles"])
        st.image(image, caption="Captured Image")
        st.write(match)





