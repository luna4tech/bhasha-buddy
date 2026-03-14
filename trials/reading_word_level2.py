import streamlit as st
from gtts import gTTS
import base64
import re
from mutagen.mp3 import MP3
from io import BytesIO

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
# Function to generate audio and get duration
def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Get duration using mutagen
    audio = MP3(fp)
    duration = audio.info.length
    fp.seek(0)
    
    return fp.read(), duration

@st.cache_data
# Function to create HTML component with audio and highlighting
def create_audio_player(audio_bytes, text, duration):
    # Convert audio bytes to base64
    audio_base64 = base64.b64encode(audio_bytes).decode()
    
    # Split text into words (including punctuation attached to words)
    words = re.findall(r'\S+|\n', text)
    words = [word.replace('\n', '<br>') for word in words]
    
    # Create HTML with words as spans
    words_html = []
    for i, word in enumerate(words):
        words_html.append(f'<span class="word" id="word-{i}">{word}</span>')
    words_html = ' '.join(words_html)
    
    # Create HTML component
    html = f"""
    <style>
    .word {{
        transition: background-color 0.3s ease;
        padding: 2px 4px;
        border-radius: 3px;
    }}
    </style>
    <audio id="player" controls>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    <div>
        {words_html}
    </div>
    <script>
        const audio = document.getElementById('player');
        const words = document.getElementsByClassName('word');
        const totalDuration = {duration};
        const wordCount = {len(words)};
        const timePerWord = totalDuration / wordCount;
        
        audio.addEventListener('timeupdate', function() {{
            const currentTime = audio.currentTime;
            let currentIndex = Math.floor(currentTime / timePerWord);
            currentIndex = Math.min(currentIndex, wordCount - 1);
            
            // Remove highlight from all words
            Array.from(words).forEach(word => {{
                word.style.backgroundColor = 'transparent';
            }});
            
            // Highlight current word
            if(words[currentIndex]) {{
                words[currentIndex].style.backgroundColor = '#ffd700';
            }}
        }});
    </script>
    """
    return html

def render_story(story_title, story_text, audio_bytes, duration):
    st.title(story_title)
       
    # Display audio player with highlighting
    st.components.v1.html(
        create_audio_player(audio_bytes, story_text, duration),
        height=400
    )

def main():
    with st.spinner("Generating your story..."):
        story_title, story_text = generate_story()
        audio_bytes, duration = generate_audio(story_text)
    render_story(story_title, story_text, audio_bytes, duration)


main()