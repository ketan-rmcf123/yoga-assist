import streamlit as st
import time
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
from utils.match_function import mp_pose, pose, mp_drawing, draw_keypoints

# Helper function to initialize session state variables
def initialize_session_state():
    if "pg_bar" not in st.session_state:
        st.session_state.pg_bar = st.progress(0)
    if "current_stage" not in st.session_state:
        st.session_state.current_stage = 1
    if "asana_validation_button_clicked" not in st.session_state:
        st.session_state.asana_validation_button_clicked = False
    if "asana_validated" not in st.session_state:
        st.session_state.asana_validated = False

initialize_session_state()  # Initialize session state variables


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
        print("Updated current stage asana_validated : ",st.session_state.current_stage,st.session_state.asana_validated) # Trigger the validation message

def update_progress_bar():
    if "current_stage" in st.session_state and "pg_bar" in st.session_state:
        progress = (st.session_state.current_stage + 1) / len(asanas)
        st.session_state.pg_bar.progress(progress)
        print("Updated  Progressbar : ",progress)

def show_validation_message():
    if st.session_state.asana_validated:
        # Display validation success message
        st.success(f"Asana validated! Moving to stage {st.session_state.current_stage + 1}")
        # Reset the validation message flag after displaying
        st.session_state.asana_validated = False
        print("Updated asana_validated : ",st.session_state.asana_validated)

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
                    st.session_state.asana_validation_button_clicked = True
                    print("Asana validation completed:", match)

                    # Update stage and progress, and show validation message
                    update_stage()
                    self.progress_callback()

                    # Refresh the current asana after stage update
                    self.current_stage = self.get_stage_callback()
                    self.asana = suryanamaskar_stages[self.current_stage][1]
                    print("Next Asana:", self.asana)
                    st.rerun()
                    #st.experimental_update()  # Forces rerun to refresh UI
                    print("Rerunning script")
        except Exception as e:
            print("Error in transform:", e)

        return img
    
def video_transformer_factory():
    return KeypointDetector(get_stage_callback=get_current_stage, progress_callback=update_progress_bar)


st.page_link("app.py", label="Back to Yogasana", icon=":material/arrow_back:")
st.markdown(
    f"""
    <div class="full-height">
    <h6>Daily Practice</h6>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="full-height">
    Observe the instructor as they demonstrate each asana then give it a try yourself. \n
    Your motion guide will be there to help you and suggest any necessary adjustments.Once you master a pose, you will be smoothly guided to the next step.Enjoy your practice!</h12>
    </div>
    """,
    unsafe_allow_html=True
)

#st.markdown("<hr style='border: 1px solid #f0f2f6;'>", unsafe_allow_html=True)
# Custom CSS to fit pills in a single row
st.markdown(
    """
    <style>
    .stPills {
        display: flex;
        flex-wrap: nowrap;
        overflow-x: auto;
    }
    .stPills div {
        flex: 0 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2= st.tabs(["Practise on my Own", "With Instructor Video"])
#def validate_asana():
with tab1:
    col1, col2 = st.columns([6, 4],border=True)

    with col1:
        st.markdown(
            f"""
            <div class="full-height">
            <h6>Motion Guide</h6>
            </div>
            """,
            unsafe_allow_html=True
        )
        #ctx = webrtc_streamer(key="asana_validator", video_transformer_factory=video_transformer_factory)
        #st.image("D:\Projects\yoga-assist\\bin\\aish\hasta_uttanasana.png",width =300)
        video_file = open('D:\Projects\yoga-assist\\bin\\aish\\aish5.mp4', 'rb')
        video_bytes = video_file.read()

        st.video(video_bytes)
    with col2:
        on = st.toggle("Voice Guide :loud_sound:")

        if on:
            st.text_area("","Pranamasana completed! \nHasta Uttanasana in progress.. \nStraighten your elbows.. \n ")


with tab2:
    # Container in the first column
    print(f"Progress bar in main script : {st.session_state.pg_bar}")
    progress_bar = st.session_state.pg_bar
    col1, col2 = st.columns([5, 5],border=True)

    with col1:
        text_placeholder = st.empty()
        video_placeholder = st.empty()

        # Initial content for the current asana
        text_placeholder.markdown(
            f"""
            <div class="full-height">
            <h6>{str(st.session_state.current_stage+1) + " : " + suryanamaskar_stages[st.session_state.current_stage][1]}</h6>
            </div>
            """,
            unsafe_allow_html=True
        )
        youtube_url = "https://www.youtube.com/watch?app=desktop&v=BgdJzqfavHI"
        video_placeholder.video(
            f"{youtube_url}?autoplay=1&mute=1",
            start_time=suryanamaskar_stages[st.session_state.current_stage][0],
        )



    with col2:
        st.markdown(
            f"""
            <div class="full-height">
            <h6>Motion Guide</h6>
            </div>
            """,
            unsafe_allow_html=True
        )
        #ctx = webrtc_streamer(key="asana_validator", video_transformer_factory=video_transformer_factory)
        #st.image("D:\Projects\yoga-assist\\bin\\aish\hasta_uttanasana.png",width =300)
        video_file = open('D:\Projects\yoga-assist\\bin\\aish\\aish5.mp4', 'rb')
        video_bytes = video_file.read()

        st.video(video_bytes)

    on = st.toggle("Voice Guide :loud_sound: ")

    if on:
        st.text_area("","11:54:31 : Pranamasana completed! \n11:54:36 : Hasta Uttanasana in progress.. \n11:54:39 : Straighten your elbows.. \n ")

