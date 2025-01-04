import streamlit as st
from streamlit_webrtc import webrtc_streamer,WebRtcMode

def main():
    st.title("Live Camera Feed")
    st.markdown("Stream your camera feed live using Streamlit and streamlit-webrtc.")

    # Stream the live camera feed
    try:
        playing = st.checkbox("Playing", value=False)

        webrtc_streamer(
            key="programatic_control",
            desired_playing_state=playing
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(e)

if __name__ == "__main__":
    main()