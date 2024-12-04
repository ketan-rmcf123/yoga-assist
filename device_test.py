"""A sample to configure MediaStreamConstraints object"""

import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

import logging
import os

# In your streamlit-webrtc component configuration
webrtc_ctx = webrtc_streamer(
    key="your-key",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={
        # Add STUN/TURN servers if needed
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    # Add proper media constraints
    media_stream_constraints={"video": True, "audio": True},
    # Add async cleanup
    async_processing=True
)

# Add proper connection cleanup
if webrtc_ctx.state.playing:
    # Your WebRTC logic here
    pass
else:
    # Clean up resources when not playing
    # Ensure connections are properly closed
    pass
st.write(f"WIP")