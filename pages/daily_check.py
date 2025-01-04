import streamlit as st
import time
import pdb
from datetime import datetime

def log_with_timestamp(*args):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]", *args)


if "webrtc_key" not in st.session_state:
    st.session_state.webrtc_key = "asana_validator"
# Set the page configuration
st.set_page_config(
    page_title="Yoga Pose Validator",
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
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp
from configs.sn_config import stages as suryanamaskar_stages, EXPECTED_ANGLES as angles_config
from utils.match_function import mp_pose, pose, mp_drawing, draw_keypoints,speak_text

# Helper function to initialize session state variables
def initialize_session_state():
    log_with_timestamp( "Current :",st.session_state)
    if "pg_bar" not in st.session_state:
        st.session_state.pg_bar = st.progress(0)
    if "current_stage" not in st.session_state:
        st.session_state.current_stage = 0
    if "asana_validation_button_clicked" not in st.session_state:
        st.session_state.asana_validation_button_clicked = False
    if "asana_validated" not in st.session_state:
        st.session_state.asana_validated = False

        log_with_timestamp( "Initialized :",st.session_state)

initialize_session_state()  # Initialize session state variables

def stop_webstreamer():
    # Invalidate the webrtc key to stop the streamer
    st.session_state.webrtc_key = None
# List of asanas
asanas = [x[1] for x in list(suryanamaskar_stages.values())]

def get_current_stage():
    if "current_stage" in st.session_state:
        print(st.session_state.current_stage)
        return st.session_state.current_stage
    else:
        initialize_session_state()
        return st.session_state.current_stage

def update_stage():
    if "current_stage" in st.session_state:
        st.session_state.current_stage += 1
        st.session_state.asana_validated = True  
        log_with_timestamp("Updated current stage asana_validated : ",st.session_state.current_stage,st.session_state.asana_validated) # Trigger the validation message

def update_progress_bar():
    if "current_stage" in st.session_state and "pg_bar" in st.session_state:
        progress = (st.session_state.current_stage + 1) / len(asanas)
        st.session_state.pg_bar.progress(progress)
        log_with_timestamp("Updated  Progressbar : ",progress)

def show_validation_message():
    if st.session_state.asana_validated:
        # Display validation success message
        st.success(f"Asana validated! Moving to stage {st.session_state.current_stage + 1}")
        # Reset the validation message flag after displaying
        st.session_state.asana_validated = False
        log_with_timestamp("Updated asana_validated : ",st.session_state.asana_validated)

class KeypointDetector(VideoTransformerBase):
    def __init__(self, get_stage_callback, progress_callback):
        self.get_stage_callback = get_stage_callback
        self.progress_callback = progress_callback
        self.current_stage = self.get_stage_callback()
        self.asana = suryanamaskar_stages[self.current_stage][1]
        log_with_timestamp("Initialized KeypointDetector with asana:", self.asana)

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        try:
            results = pose.process(img)
            print(results)
            if results.pose_landmarks:
                # Draw landmarks and check if the pose matches
                #print("Expected angles: ",self.asana, angles_config[self.asana]["Angles"])
                current_angles, match = draw_keypoints(img, angles_config[self.asana]["Angles"])
                
                if match:
                    st.session_state.asana_validation_button_clicked = True
                    print("Asana validation completed:", match)

                    # Update stage and progress, and show validation message
                    update_stage()
                    self.progress_callback()

                    # Refresh the current asana after stage update
                    self.current_stage = self.get_stage_callback()
                    self.asana = suryanamaskar_stages[self.current_stage][1]
                    log_with_timestamp("Next Asana:", self.asana, st.session_state.asana_validated)
                    #st.experimental_update()  # Forces rerun to refresh UI
                    speak_text(f"Next asana after updation: {self.asana}")

        except Exception as e:
            log_with_timestamp("Error in transform:", e)

        return img
    
def video_transformer_factory():
    return KeypointDetector(get_stage_callback=get_current_stage, progress_callback=update_progress_bar)


st.page_link("app.py", label="Back to Yogasana", icon=":material/arrow_back:")
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
    
# Container in the first column
progress_bar = st.session_state.pg_bar
if st.session_state.webrtc_key:
    ctx = webrtc_streamer(key="asana_validator", video_transformer_factory=video_transformer_factory)

rf_state_button= st.button("Refresh state:")
if rf_state_button:
    speak_text("Refreshing state")
    st.session_state.pg_bar = st.progress(0)
    st.session_state.current_stage = 0
    st.session_state.asana_validation_button_clicked = False
    st.session_state.asana_validated = False


# Function to update the column based on validation
def check_and_update_page():
    log_with_timestamp("Status asana_validated",st.session_state.asana_validated, type(st.session_state.asana_validated))
    if st.session_state.asana_validated==True:

        log_with_timestamp("Session state updated : Asana validated : Next Asana {suryanamaskar_stages[st.session_state.current_stage][1]}")
        st.markdown( 
            f"""
            <div class="full-height">
            <h6>Daily Suryanamaskar check</h6>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="full-height">
            <h6>{suryanamaskar_stages[st.session_state.current_stage][1]}</h6>
            </div>
            """,
            unsafe_allow_html=True
        )
        log_with_timestamp("Reloading webrtc streamer")
        if st.session_state.webrtc_key:
            ctx = webrtc_streamer(key="asana_validator", video_transformer_factory=video_transformer_factory)
            
            # Reset validation flag and update progress bar
            st.session_state.asana_validated = False
            progress_bar.progress((st.session_state.current_stage + 1) / len(asanas))
            log_with_timestamp(f"Setting assana_validated to False : {st.session.asana_validated}", {progress_bar})

        # Optionally, add progress bar update or other actions here
    else:
        log_with_timestamp("Sleeping for 5s  ",suryanamaskar_stages[st.session_state.current_stage][1])
        # Sleep for a short duration, then check again
        time.sleep(5)
        check_and_update_page()  

