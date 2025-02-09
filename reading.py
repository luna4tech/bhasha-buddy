import streamlit as st
from reading_component import reading_component
from gtts import gTTS
import base64
import re
from io import BytesIO
import json

language = "en-IN"

with open('stories.json', 'r') as f:
    stories_list = json.load(f)

@st.cache_data
def generate_story(story_title):
    return stories_list[story_title]

@st.cache_data
def generate_audio(text):
    tts = gTTS(text=text, lang=language)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    return fp.read()

def main():
    story_title = st.selectbox('Select option', stories_list.keys())
    if(st.button("Generate Story")):
        with st.spinner("Generating your story..."):
            story_text = generate_story(story_title)
            audio_bytes = generate_audio(story_text)
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_src = f"data:audio/mp3;base64,{audio_base64}"
            words = story_text.split()
            reading_component(
                audio_src,
                words,
                story_title,
                language
            )

main()


