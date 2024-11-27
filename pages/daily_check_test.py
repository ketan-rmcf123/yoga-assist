import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import mediapipe as mp
import av
from datetime import datetime
import time

# Custom CSS for the timer
st.markdown("""
    <style>
    .timer-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
    .big-timer {
        font-size: 48px;
        font-weight: bold;
        color: #0f2b46;
        margin: 10px 0;
    }
    .timer-label {
        font-size: 18px;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'current_pose_index' not in st.session_state:
    st.session_state.current_pose_index = 0
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'timer' not in st.session_state:
    st.session_state.timer = 5

# List of yoga poses
YOGA_POSES = [
    "Mountain Pose (Tadasana)",
    "Tree Pose (Vrksasana)",
    "Warrior I (Virabhadrasana I)",
    "Warrior II (Virabhadrasana II)",
    "Downward-Facing Dog (Adho Mukha Svanasana)"
]

# Initialize MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Main app
st.title("🧘‍♀️ Yoga Pose Tracker")

# Progress bar
progress = st.progress(int((st.session_state.current_pose_index / len(asanas)) * 100))

# Current pose and timer display
st.markdown(f"""
    <div class="timer-container">
        <div class="timer-label">Current Pose</div>
        <div style="font-size: 24px; margin-bottom: 20px;">{YOGA_POSES[st.session_state.current_pose_index]}</div>
        <div class="timer-label">Time Remaining</div>
        <div class="big-timer">{max(0, 5 - (time.time() - st.session_state.start_time)):.1f}s</div>
    </div>
""", unsafe_allow_html=True)

# Main container
col1, col2 = st.columns([2, 1])

with col1:
    def video_frame_callback(frame):
        current_time = time.time()
        elapsed_time = current_time - st.session_state.start_time
        
        img = frame.to_ndarray(format="bgr24")
        
        # Process the frame with MediaPipe
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #results = pose.process(image)
        
        # Draw pose landmarks
        #if results.pose_landmarks:
        #    mp.solutions.drawing_utils.draw_landmarks(
        #        img,
        #        results.pose_landmarks,
        #        mp_pose.POSE_CONNECTIONS
        #    )
        
        # Check if 5 seconds have passed
        if elapsed_time >= 50:
            # Log the completion
            current_pose = YOGA_POSES[st.session_state.current_pose_index]
            log_message = f"{datetime.now().strftime('%H:%M:%S')} - Completed: {current_pose}"
            if log_message not in st.session_state.logs:
                st.session_state.logs.append(log_message)
            
            # Move to next pose
            if st.session_state.current_pose_index < len(YOGA_POSES) - 1:
                st.session_state.current_pose_index += 1
            
            # Reset timer
            st.session_state.start_time = current_time
            st.experimental_rerun()  # Force UI update

        # Draw timer on frame
        remaining_time = max(0, 50 - elapsed_time)
        cv2.putText(
            img,
            f"Next pose in: {remaining_time:.1f}s",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    webrtc_streamer(
        key="yoga_pose_detection",
        video_frame_callback=video_frame_callback,
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
        media_stream_constraints={"video": True, "audio": False},
    )

with col2:
    # Logging section
    st.markdown("""
        <div style="background-color: #f0f2f6; border-radius: 10px; padding: 20px; margin-top: 20px;">
            <h3 style="margin-top: 0;">Progress Log</h3>
        </div>
    """, unsafe_allow_html=True)
    for log in st.session_state.logs:
        st.text(log)

# Reset button
if st.button("Reset Session", type="primary"):
    st.session_state.current_pose_index = 0
    st.session_state.logs = []
    st.session_state.start_time = time.time()
    st.rerun()

# Auto-rerun every second to update timer
time.sleep(0.1)  # Small delay to prevent too frequent updates
st.rerun()