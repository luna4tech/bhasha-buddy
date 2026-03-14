import streamlit as st
from reading_component import reading_component
from gtts import gTTS
import whisper_timestamped as whisper
from io import BytesIO
from mutagen.mp3 import MP3
import json
import base64
import re

@st.cache_resource
def load_model():
    return whisper.load_model("base")

story_files = {
    "en-IN": 'stories.json',
    "te": 'stories_telugu.json'
}

@st.cache_data
def generate_audio(text, language):
    tts = gTTS(text=text, lang=language)
    tts.save('story.mp3')

    audio = MP3('story.mp3')
    duration = audio.info.length
    with open('story.mp3', 'rb') as fp:
        audio_bytes = fp.read()

    return audio_bytes, duration

@st.cache_data
def generate_audio_bk(text, language):
    tts = gTTS(text=text, lang=language)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Get duration using mutagen
    audio = MP3(fp)
    duration = audio.info.length
    fp.seek(0)

    return fp.read(), duration

def get_words_from_audio(audio_bytes, language):
    audio = whisper.load_audio('story.mp3')
    model = load_model()
    data = whisper.transcribe(model, audio, language="en")
    return [word for segment in data['segments'] for word in segment['words']]

def get_lines_from_audio(audio_bytes, language):
    audio = whisper.load_audio('story.mp3')
    model = load_model()
    data = whisper.transcribe(model, audio, language="en")
    return data['segments']

def get_audio_src(audio_bytes):
    audio_base64 = base64.b64encode(audio_bytes).decode()
    return f"data:audio/mp3;base64,{audio_base64}"

def get_words_split(text, duration):
    words = text.split()
    time_per_word = duration/len(words)
    words_split = []
    for i in range(len(words)):
        words_split.append({
            'text': words[i],
            'start': i*time_per_word,
            'end': (i+1)*time_per_word
        })
    return words_split

def get_words_audio(text):
    words = set(text.split())
    words_audio = {}
    for word in words:
        tts = gTTS(text=word, lang='en')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        words_audio[word] = fp.read()
    return words_audio 

def main():
    language = st.selectbox('Select Language', story_files.keys())
    if(language):
        with open(story_files[language], 'r') as f:
            stories_list = json.load(f)
            story_title = st.selectbox('Select option', stories_list.keys())
            if(st.button("Generate Story")):
                with st.spinner("Generating your story..."):
                    story_text = stories_list[story_title]

                    audio_bytes, duration = generate_audio(story_text, language)
                    audio_src = get_audio_src(audio_bytes)
                    words_split1 = get_words_from_audio(audio_bytes, language)
                    words_split = get_words_split(story_text, duration)
                    words_audio = get_words_audio(story_text)
                    reading_component(
                        audio_src,
                        words_split1,
                        words_audio,
                        story_title,
                        language
                    )

main()


