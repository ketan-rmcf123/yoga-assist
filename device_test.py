"""A sample to configure MediaStreamConstraints object"""

import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

import logging
import os

import streamlit as st
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)


def get_ice_servers():
    """Use Twilio's TURN server because Streamlit Community Cloud has changed
    its infrastructure and WebRTC connection cannot be established without TURN server now.  # noqa: E501
    We considered Open Relay Project (https://www.metered.ca/tools/openrelay/) too,
    but it is not stable and hardly works as some people reported like https://github.com/aiortc/aiortc/issues/832#issuecomment-1482420656  # noqa: E501
    See https://github.com/whitphx/streamlit-webrtc/issues/1213
    """

    # Ref: https://www.twilio.com/docs/stun-turn/api
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    try:
        token = client.tokens.create()
    except TwilioRestException as e:
        st.warning(
            f"Error occurred while accessing Twilio API. Fallback to a free STUN server from Google. ({e})"  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    return token.ice_servers


frame_rate = 5
webrtc_streamer(
    key="media-constraints",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={"iceServers": get_ice_servers()},
    media_stream_constraints={
        "video": {"frameRate": {"ideal": frame_rate}},
    },
    video_html_attrs={
        "style": {"width": "50%", "margin": "0 auto", "border": "5px yellow solid"},
        "controls": False,
        "autoPlay": True,
    },
)
st.write(f"The frame rate is set as {frame_rate}. Video style is changed.")