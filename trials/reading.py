import streamlit as st
from gtts import gTTS
from io import BytesIO
import pyttsx3
import time

story = """
I'm reading a story now. 
"""

def read_text_gtts(text):
    tts = gTTS(text=text, lang='en')

    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)  
    
    st.audio(audio_buffer.read(), format="audio/mp3")

st.write(story)
if st.button('Read'):
    read_text_gtts(story)