import streamlit as st
from reading_component import reading_component
from mutagen.mp3 import MP3
import json
import base64
import re
import os
import string
from constants import *

if 'key' not in st.session_state:
    st.session_state.key = []
if 'index' not in st.session_state:
    st.session_state.index = -1
if 'is_correct' not in st.session_state:
    st.session_state.is_correct = True

def reset_state():
    st.session_state.key = []
    st.session_state.index = -1
    st.session_state.is_correct = True

def print_session():
    print(st.session_state.key)
    print(st.session_state.index)
    print(st.session_state.is_correct)

def get_audio_src(audio_filepath):
    try:
        audio_bytes = open(audio_filepath, 'rb').read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        return f"data:audio/mp3;base64,{audio_base64}"
    except FileNotFoundError:
        print(f"Error: The file '{audio_filepath}' was not found.")
        return f""

def get_approx_words_split(audio_filepath, text):
    audio = MP3(audio_filepath)
    words = text.split()
    time_per_word = audio.info.length/len(words)
    words_split = []
    for i in range(len(words)):
        words_split.append({
            'text': words[i],
            'start': i*time_per_word,
            'end': (i+1)*time_per_word
        })
    return words_split

# build the UI
print_session()
if st.sidebar.button("Create story"):
    st.switch_page(page="pages/admin.py")

st.sidebar.title("Read your stories")
languages = [d for d in os.listdir(RESOURCES_DIR) 
                if d in LANG_MAP.keys()]
language = st.sidebar.selectbox('Select Language', languages, on_change=reset_state)
if(language):
    stories = [d for d in os.listdir(os.path.join(RESOURCES_DIR, language)) 
                if d != VOCAB_DIRECTORY]
    title = st.sidebar.selectbox('Select story', stories, on_change=reset_state)
    
    if(title):            
        audio_filepath = os.path.join(RESOURCES_DIR, language, title, AUDIO_FILE_NAME)
        story_text = open(os.path.join(RESOURCES_DIR, language, title, STORY_FILE_NAME), 'r', encoding='utf-8').read()
        audio_src = get_audio_src(audio_filepath)

        words_metadata_filepath = os.path.join(RESOURCES_DIR, language, title, WORDS_METADATA_FILE_NAME)
        if(os.path.exists(words_metadata_filepath)):
            with open(words_metadata_filepath, 'r') as f:
                words_metadata = json.load(f)
        else:
            words_metadata = get_approx_words_split(audio_filepath, story_text)
        
        words_audio = {}
        for word in GET_UNIQUE_WORDS(story_text):
            audio = os.path.join(RESOURCES_DIR, language, VOCAB_DIRECTORY, f"{word}.mp3")
            words_audio[word] = get_audio_src(audio)

        story_text_split = story_text.split()

        is_practice = st.toggle("Practice")
        
        if is_practice:
            st.audio_input("Read out loud")
            next_word = st.text_input("Enter next word: ")
            if next_word:
                print("Comparing: ", CLEAN_WORD(next_word), CLEAN_WORD(story_text_split[st.session_state.index+1]))
                if CLEAN_WORD(next_word) == CLEAN_WORD(story_text_split[st.session_state.index+1]): 
                    st.session_state.is_correct = True
                    st.session_state.index = st.session_state.index + 1
                    st.session_state.key.append(next_word) 
                else:
                    st.session_state.is_correct = False
    
        reading_component(
            audio_src,
            story_text_split,
            words_metadata,
            words_audio,
            title,
            st.session_state.index,
            st.session_state.is_correct
        )

