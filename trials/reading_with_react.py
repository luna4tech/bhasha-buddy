import streamlit as st
from gtts import gTTS
import base64
import re
from mutagen.mp3 import MP3
from io import BytesIO
import streamlit.components.v1 as components

_reading_component = components.declare_component(
    "reading_component",
    url="http://localhost:3001"
)

def reading_component(audio_src, words, key=None):
    return _reading_component(audio_src=audio_src, words=words, key=key)


def generate_story():
    return "Slow and steady wins the race", """
        A hare and tortoise lived in a distant jungle. But the hare always mocked the tortoise.

        “You are so slow, do you ever make it on time?”

        Offended by the rude tone, the tortoise replied in a humble tone.

        “Don’t be so arrogant, let’s compete in a race, and see who’s faster!”

        The hare burst into laughter and declared the other side of the hill as the final point.

        Both the animals started off, and the hare ran faster to reach the finish line in no time!

        Soon the hare felt exhausted and stopped for a quick nap. 

        As the overconfident hare dozed off, the tortoise quietly surpassed him. By the time the hare woke up and ran to the finish point, the tortoise had already won the race!
    """

@st.cache_data
def generate_audio(text):
    tts = gTTS(text=text, lang='en-IN')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Get duration using mutagen
    audio = MP3(fp)
    duration = audio.info.length
    fp.seek(0)
    
    return fp.read(), duration

def main():
    with st.spinner("Generating your story..."):
        story_title, story_text = generate_story()
        audio_bytes, duration = generate_audio(story_text)
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_src = f"data:audio/mp3;base64,{audio_base64}"
    words = story_text.split()
    reading_component(
        audio_src,
        words
    )


main()


