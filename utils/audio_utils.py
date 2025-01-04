import streamlit as st
from gtts import gTTS
from io import BytesIO

def read_text(placeholder=st,text=""):
    tts = gTTS(text)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    # Play audio in Streamlit
    placeholder.audio(audio_buffer, format="audio/mp3",autoplay =True)