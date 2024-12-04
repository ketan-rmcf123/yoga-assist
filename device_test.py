import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration

# Configure WebRTC
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},  # Public STUN server
    ]
})

# WebRTC callback (process frames if needed)
def video_frame_callback(frame):
    # Simply echo the frame back
    return frame

st.title("WebRTC Example on Streamlit Cloud")

# Initialize WebRTC streamer
webrtc_streamer(
    key="example",
    mode="SENDRECV",
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    video_frame_callback=video_frame_callback,
)
