import streamlit as st
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


if "current_stage" not in st.session_state:  
    st.session_state.current_stage = 0

if "asana_validation_button_clicked" not in st.session_state:  
    st.session_state.asana_validation_button_clicked =False



from streamlit_webrtc import webrtc_streamer
from streamlit_webrtc import VideoTransformerBase
import mediapipe as mp
from configs.sn_config import stages as suryanamaskar_stages, EXPECTED_ANGLES as angles_config
from utils.match_function import mp_pose, pose, mp_drawing, draw_keypoints

from random import shuffle
import time
import extra_streamlit_components as stx
from stqdm import stqdm

total_steps = len(suryanamaskar_stages)
asanas = [x[1] for x in list(suryanamaskar_stages.values())]

print("Mediapipe model loaded")

def update_stage():
    st.session_state.current_stage = st.session_state.current_stage + 1
    print("Current stage:",st.session_state.current_stage)
    


class KeypointDetector(VideoTransformerBase):
    def __init__(self, asana):
        self.asana = asana
        print(self.asana)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)
            # Draw pose landmarks on the image
            if results.pose_landmarks:
                # Drawing landmarks
                    current_angles,match = draw_keypoints(img, angles_config[self.asana]["Angles"])
                    if match == True:
                        st.session_state.asana_validation_button_clicked = True
                        print(f"Asana validation completed {match}")
                        progress_bar.progress((st.session_state.current_stage+1)/len(asanas))
                        update_stage()

                    else:
                        pass
        except Exception as e:
            print(e)
        
        return img

def video_transformer_factory():
    if "current_stage" not in st.session_state:  
        st.session_state.current_stage = 0
    current_stage = st.session_state.current_stage
    return KeypointDetector(asana=suryanamaskar_stages[current_stage][1])



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
    <h12>Observe the instructor as they demonstrate each asana then give it a try yourself.Your motion guide will be there to help you and suggest any necessary adjustments.Once you master a pose, you will be smoothly guided to the next step.Enjoy your practice!</h12>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr style='border: 1px solid #f0f2f6;'>", unsafe_allow_html=True)

#def validate_asana():
    

progress_bar = st.progress(0)
col1, col2= st.columns([6, 4])
# Container in the first column

with col1:
    text_placeholder = st.empty()
    video_placeholder = st.empty()
    button_placeholder = st.empty()
    
    for asana_id,asana in enumerate(asanas):
        st.session_state.asana_validation_button_clicked = False
        text_placeholder.markdown(
            f"""
            <div class="full-height">
            <h6>{suryanamaskar_stages[st.session_state.current_stage][1]}</h6>
            </div>
            """,
            unsafe_allow_html=True
        )
        youtube_url = "https://www.youtube.com/watch?app=desktop&v=BgdJzqfavHI"  # New video URL
        video_placeholder.video(f"{youtube_url}?autoplay=1&mute=1",start_time=suryanamaskar_stages[st.session_state.current_stage][0])  # New video URL,start_time=)  
        status = button_placeholder.button(label='Next step', key = f"{asana}-{asana_id}",on_click=update_stage)
        if status:
            print("Status",status)
            progress_bar.progress((st.session_state.current_stage)/len(asanas))


with col2:
    webrtc_streamer(key="yoga", video_transformer_factory=video_transformer_factory)
    st.markdown(
        f"""
        <div class="full-height">
        <h6>Motion guide</h6>
        </div>
        """,
        unsafe_allow_html=True
    )
    