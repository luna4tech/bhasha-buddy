import streamlit as st
from gtts import gTTS
import whisper_timestamped as whisper
import os
import re
import json
import string
import shutil
from constants import *

MODEL = whisper.load_model(WHISPER_MODEL)

def contains_invalid_chars(filename):
    return bool(re.search(INVALID_CHARS_PATTERN, filename))

def create_dir(lang, title):
    directory_path = os.path.join(RESOURCES_DIR, lang, title)
    os.makedirs(directory_path, exist_ok=True)
    return directory_path

def save_text(title, text, lang, directory_path):
    # Save the story in a text file with the title as the filename
    filepath = os.path.join(directory_path, STORY_FILE_NAME)
    if os.path.exists(filepath):
        return False, f"A story with the title '{title}' already exists in {lang}. Please choose a different title."
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        return True, f"Story '{title}' added successfully in {lang}!"

def save_audio(title, text, lang_code, directory_path):
    print("Text: ", text)
    filepath = os.path.join(directory_path, AUDIO_FILE_NAME)
    tts = gTTS(text=text, lang=lang_code)
    tts.save(filepath)
    return filepath

def save_words_audio(text, lang_code, lang_directory_path):
    words_dir_path = os.path.join(RESOURCES_DIR, lang, VOCAB_DIRECTORY)
    os.makedirs(words_dir_path, exist_ok=True)

    for word in GET_UNIQUE_WORDS(text):
        filepath = os.path.join(words_dir_path, f"{word}.mp3")
        tts = gTTS(text=word, lang=lang_code)
        tts.save(filepath)

def get_data_from_whisper(directory_path, lang_code):
    audio_filepath = os.path.join(directory_path, AUDIO_FILE_NAME)
    audio = whisper.load_audio(audio_filepath)
    return whisper.transcribe(MODEL, audio, language=lang_code[0:2])

# save list of words from the audio to json file
# word format: {'start': 0.0, 'end': 0.3, 'text': 'The'}
def save_words_metadata(directory_path, detected_data, story_text, title, lang_code):
    detected_words = [word for segment in detected_data['segments'] for word in segment['words']]
    print(detected_words)
    # replace with corresponding word from story text as whisper detected words might not be accurate
    story_words = story_text.split()
    if len(story_words) == len(detected_words):
        for i in range(len(detected_words)):
            detected_words[i]["text"] = story_words[i]
    else:
        print("Speech detection of whisper did not give correct number of words")

    json_filepath = os.path.join(directory_path, WORDS_METADATA_FILE_NAME)
    with open(json_filepath, "w") as f:
        json.dump(detected_words, f, indent=4)

# save list of sententces from the audio to json file
# segment format: {'start': 0.0, 'end': 0.3, 'text': 'The quick fox jumps over the lazy dog.'}
def save_lines_metadata(directory_path, detected_data, title, lang_code):
    fields = ['id', 'start', 'end', 'text']
    lines = [{key: segment[key] for key in fields if key in segment} for segment in detected_data['segments']]

    json_filepath = os.path.join(directory_path, LINES_METADATA_FILE_NAME)
    with open(json_filepath, "w") as f:
        json.dump(lines, f, indent=4)

def generate_story_files(lang, title, text):
    directory_path = create_dir(lang, title)
    status, msg = save_text(title, text, lang, directory_path)
    if(status):
        audio_filepath = save_audio(title, text, LANG_MAP[lang], directory_path)
        if(lang in WHISPER_LANGS):
            detected_data = get_data_from_whisper(directory_path, LANG_MAP[lang])
            save_words_metadata(directory_path, detected_data, text, title, LANG_MAP[lang])
            save_lines_metadata(directory_path, detected_data, title, LANG_MAP[lang])
        save_words_audio(text, LANG_MAP[lang], directory_path)
        return True, msg
    else:
        return False, msg

# build the UI
if st.button("Start reading"):
    st.switch_page(page="reading.py")

add_story_tab, add_from_local, del_story_tab = st.tabs(["Add Story", "Generate Story", "Delete Story"])

# Add story tab
with add_story_tab:
    st.title("Add a Story")
    lang = st.selectbox("Select Language", LANG_MAP.keys())
    title = st.text_input("Enter Story Title")
    text = st.text_area("Enter Story content")
    with st.spinner("Adding Story..."):
        if st.button("Add Story"):
            if not title.strip() or not text.strip():
                st.error("Title and Content cannot be empty!")
            elif contains_invalid_chars(title):
                st.error("Title contains invalid characters. Please remove them and try again.")
            else:
                status, msg = generate_story_files(lang, title, content)
                if(status):
                    st.success(msg)
                else:
                    st.error(msg)

# Add existing stories from local folder
with add_from_local:
    pw = st.text_input("Enter password to generate stories")
    if pw == 'password':
        with st.spinner("Generating stories..."):
            for lang in LANG_MAP.keys():
                with open(os.path.join(STORIES_DIR, f"{lang}.json"), 'r') as f:
                    stories_list = json.load(f)
                    for title in stories_list.keys():
                        content = stories_list[title]
                        status, msg = generate_story_files(lang, title, content)
                        if(status):
                            st.success(msg)
                        else:
                            st.error(msg)

# Delete story tab
with del_story_tab:
    pw = st.text_input("Enter password to delete")
    allow_delete = pw == 'password'
    if os.path.exists(RESOURCES_DIR):
        langs = [d for d in os.listdir(RESOURCES_DIR) if os.path.isdir(os.path.join(RESOURCES_DIR, d))]

        if langs:
            for lang in langs:
                st.header(lang)
                lang_path = os.path.join(RESOURCES_DIR, lang)
                stories = [d for d in os.listdir(os.path.join(RESOURCES_DIR, lang)) 
                    if d != VOCAB_DIRECTORY]

                for story in stories:
                    story_path = os.path.join(lang_path, story)
                    if st.button(f"Delete {story}", key=story, disabled=not allow_delete):
                        # Delete the directory and refresh the list
                        try:
                            shutil.rmtree(story_path)
                            st.success(f"Deleted '{story}'")
                            st.rerun()  # Refresh the app to show updated list
                        except Exception as e:
                            st.error(f"Error deleting '{story}': {str(e)}")
