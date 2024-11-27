import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp
from configs.sn_config import stages as suryanamaskar_stages, EXPECTED_ANGLES as angles_config
from utils.match_function import mp_pose, pose, mp_drawing, draw_keypoints

# Helper function to initialize session state variables
def initialize_session_state():
    if "pg_bar" not in st.session_state:
        st.session_state.pg_bar = st.progress(0)
    if "current_stage" not in st.session_state:
        st.session_state.current_stage = 0
    if "asana_validation_button_clicked" not in st.session_state:
        st.session_state.asana_validation_button_clicked = False

initialize_session_state()  # Call this at the start of the script to ensure all variables are initialized

# List of asanas
asanas = [x[1] for x in list(suryanamaskar_stages.values())]

def get_current_stage():
    # Explicit check for session state initialization
    if "current_stage" in st.session_state:
        return st.session_state.current_stage
    else:
        initialize_session_state()
        return st.session_state.current_stage

def update_stage():
    # Explicit check and update
    if "current_stage" in st.session_state:
        st.session_state.current_stage += 1
        print("Current stage:", st.session_state.current_stage)

def update_progress_bar():
    # Ensure the progress bar is updated based on the current stage
    if "current_stage" in st.session_state and "pg_bar" in st.session_state:
        progress = (st.session_state.current_stage + 1) / len(asanas)
        st.session_state.pg_bar.progress(progress)

class KeypointDetector(VideoTransformerBase):
    def __init__(self, get_stage_callback, progress_callback):
        self.get_stage_callback = get_stage_callback
        self.progress_callback = progress_callback
        self.current_stage = self.get_stage_callback()
        self.asana = suryanamaskar_stages[self.current_stage][1]
        print("Initialized KeypointDetector with asana:", self.asana)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)
            
            if results.pose_landmarks:
                # Draw landmarks and check if the pose matches
                
                current_angles, match = draw_keypoints(img, angles_config[self.asana]["Angles"])
                
                if match:
                    # Trigger the session state update outside of `transform`
                    st.session_state.asana_validation_button_clicked = True
                    print("Asana validation completed:", match)

                    # Update stage and progress outside of WebRTC component
                    update_stage()
                    self.progress_callback()

                    # Refresh the current asana after stage update
                    self.current_stage = self.get_stage_callback()
                    self.asana = suryanamaskar_stages[self.current_stage][1]
                    print("Next Asana:", self.asana)

        except Exception as e:
            print("Error in transform:", e)

        return img

def video_transformer_factory():
    # Pass callbacks to access and modify session state from outside
    return KeypointDetector(get_stage_callback=get_current_stage, progress_callback=update_progress_bar)

# WebRTC streamer setup with video transformer factory
ctx = webrtc_streamer(key="asana_validator", video_transformer_factory=video_transformer_factory)
