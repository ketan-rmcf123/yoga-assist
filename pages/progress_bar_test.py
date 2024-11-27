import streamlit as st
import time
from datetime import datetime
from configs.sn_config import stages as suryanamaskar_stages, EXPECTED_ANGLES as angles_config
from utils.match_function import mp_pose, pose, mp_drawing, draw_keypoints, speak_text
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# Initialize session state
def initialize_session_state():
    defaults = {
        "current_index": 0,
        "running": True,
        "progress": 0,
        "ctx_running": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def log_with_timestamp(*args):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]", *args)

initialize_session_state()

# Asana list
asanas = [x[1] for x in list(suryanamaskar_stages.values())]

class KeypointDetector(VideoTransformerBase):
    def __init__(self, current_stage):
        self.match_flag = False
        self.asana = suryanamaskar_stages[current_stage][1]
        log_with_timestamp("Initialized KeypointDetector with asana:", self.asana)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)
            
            if results.pose_landmarks:
                # Draw landmarks and check if the pose matches
                current_angles, match = draw_keypoints(img, angles_config[self.asana]["Angles"])
                if match:
                    self.match_flag = self.match_flag or True
                    log_with_timestamp("Next Asana:", self.asana)

        except Exception as e:
            log_with_timestamp("Error in transform:", e)

        return img
def video_transformer_factory():
    # Re-initialize session state variables in case they were not set
    if "current_index" not in st.session_state:
        st.session_state["current_index"] = 0

    # Use current stage from session state
    current_stage = st.session_state.current_index
    return KeypointDetector(current_stage=current_stage)

def main():
    initialize_session_state()

    # Page title and layout
    st.title("Yoga Progress Tracker")

    # Navigation and control columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Previous"):
            st.session_state.current_index = (st.session_state.current_index - 1) % len(asanas)
            st.session_state.progress = max(0, st.session_state.progress - int(100/(len(asanas)-1)))
    
    with col2:
        if st.button("Stop"):
            st.session_state.running = False
    
    with col3:
        if st.button("Play"):
            st.session_state.running = True
    
    with col4:
        if st.button("Next"):
            st.session_state.current_index = (st.session_state.current_index + 1) % len(asanas)
            st.session_state.progress = min(100, st.session_state.progress + int(100/(len(asanas)-1)))
    
    with col5:
        if st.button("Refresh"):
            st.session_state.current_index = 0
            st.session_state.running = True
            st.session_state.progress = 0

    # Display current asana
    current_asana = st.markdown(f"### Current Asana: {asanas[st.session_state.current_index]}")
    
    # Progress bar
    progress_bar = st.progress(st.session_state.progress)

    # WebRTC streamer
    ctx = webrtc_streamer(
        key="asana_validator", 
        video_transformer_factory=video_transformer_factory,
        )
    

    def validate_yoga():
        if ctx.video_transformer:
            return ctx.video_transformer.match_flag
        return False

    # Main tracking logic
    if st.session_state.running:
        match = validate_yoga()
        
        if match:
            st.session_state.progress = min(100, st.session_state.progress + int(100 / (len(asanas)-1)))
            st.session_state.current_index = (st.session_state.current_index + 1) % len(asanas)
            
            # Update UI
            progress_bar.progress(st.session_state.progress)
            current_asana.markdown(f"### Current Asana: {asanas[st.session_state.current_index]}")
            
            # Reset match flag
            if ctx.video_transformer:
                ctx.video_transformer.match_flag = False
            
            # Optional: Add a small delay
            time.sleep(2)

        # Reset if completed full cycle
        if st.session_state.progress >= 100:
            st.session_state.progress = 0
            st.session_state.current_index = 0

if __name__ == "__main__":
    main()