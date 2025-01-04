import streamlit as st
import time
import pandas as pd

st.set_page_config(
    page_title="Yoga Pose Daily Practice",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
from typing import List, NamedTuple
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
from configs.sn_config import stages as suryanamaskar_stages, EXPECTED_ANGLES as angles_config
from utils.match_function import pose, draw_keypoints
from utils.db_utils import MatchResult
from utils.audio_utils import read_text
from uuid import uuid4
import queue,av

if "uid" not  in st.session_state:
    st.session_state.uid = str(uuid4())[:10]
    print("uid",st.session_state.uid)


class MatchResult(NamedTuple):
    uid:int
    asana: int
    status: str
    visibility: dict
    current_angles: dict

result_queue: "queue.Queue[List[MatchResult]]" = queue.Queue()

def write_to_queue(uid,asana,status,visibility,current_angles):
    entry =  [ MatchResult(uid=uid,
    asana= asana,
    status=status,
    visibility = visibility,
    current_angles = current_angles
)]  
    result_queue.put(entry)
    return result_queue

frame_rate = 10
def asana_processor(uid,asana) -> av.VideoFrame:
    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)
            
            if results.pose_landmarks:
                # Draw landmarks and check if the pose matches
                current_angles, match, visibility = draw_keypoints(img, angles_config[asana]["Angles"])
                if match:
                    write_to_queue(uid, asana, "Match Found", visibility, current_angles)
                    #print(result_queue.qsize())
                else:
                    write_to_queue(uid, asana, "Match Not Found", visibility, current_angles)
                    #print(result_queue.qsize())
            
            last_three = list(result_queue.queue)[-3:]
            #print(last_three)
        except Exception as e:
            print("Error in transform:", e)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
    return video_frame_callback

def sample_processor(uid,asana) -> av.VideoFrame:
    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)

            print(uid,asana,results)
        except Exception as e:
            print("Error in transform:", e)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
    return video_frame_callback


# Initialize session state
if "asana_index" not in st.session_state:
    st.session_state.asana_index = 0

st.page_link("app.py", label="Back to Yogasana", icon=":material/arrow_back:")
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
        
    processor_callback = sample_processor(st.session_state.uid, suryanamaskar_stages[st.session_state.asana_index][1])
    
    
    ctx = webrtc_streamer(key="asana_validator", 
                          video_frame_callback=processor_callback,
                          mode=WebRtcMode.SENDRECV,
                          desired_playing_state=playing,
#                          async_processing=True,

                        )
with col2:
    if st.checkbox("Show the detected labels outside", value=False):
        labels_placeholder = st.empty()
        audio_placeholder = st.empty()
        status_placeholder = st.empty()
        table_placeholder = st.empty()
        # NOTE: The video transformation with object detection and
        # this loop displaying the result labels are running
        # in different threads asynchronously.
        # Then the rendered video frames and the labels displayed here
        # are not strictly synchronized.
        audio_button = st.checkbox("Play Instructions",value=False)
        if ctx.state.playing:
            while True:
                try:
                    result = result_queue.get()
                    labels_placeholder.table(result)
                    
                    if "Match" in result[0].status:
                        status_placeholder.write(result[0])
                        if audio_button:
                            read_text(audio_placeholder,result[0].status)
                            time.sleep(0.5)
                        print(result[0].current_angles)
                        df = pd.DataFrame.from_dict([result[0].visibility]).T
                        df = df.reset_index(inplace=True)
                        #df["angles"] = df.apply(lambda x: result[0].current_angles.get(x["index"]),axis=0)
                        table_placeholder.table(df)

                except Exception as e:
                    print(str(e))

