"""A sample to configure MediaStreamConstraints object"""

import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

import logging
import os

webrtc_streamer(
    key="media-constraints",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={  # Add this config
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)
st.write(f"WIP")