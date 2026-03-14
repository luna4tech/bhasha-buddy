import streamlit as st
from gtts import gTTS
from io import BytesIO
import pyttsx3
import time

story = """
I'm reading a story now. I'm reading a story now. I'm reading a story now. I'm reading a story now. I'm reading a story now. I'm reading a story now.
"""
filename = 'story.mp3'

def text_to_speech_gtts(text):
    tts = gTTS(text, 'en')
    tts.save(filename)

def text_to_speech_pytts(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

def read_text_pytts(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def read_text_from_file():
    st.audio(filename, format='audio/mp3')

def read_text_gtts(text):
    tts = gTTS(text=text, lang='en')

    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)  
    st.audio(audio_buffer.read(), format="audio/mp3")

st.write(story)
if st.button('Read'):
    st.write("Reading...")
    read_text_gtts(story)
