import streamlit as st
from gtts import gTTS
import base64
import re
from mutagen.mp3 import MP3
from io import BytesIO

def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    audio = MP3(fp)
    duration = audio.info.length
    fp.seek(0)
    
    return fp.read(), duration

def create_audio_player(audio_bytes, text, duration):
    audio_base64 = base64.b64encode(audio_bytes).decode()
    
    words = re.findall(r'\S+|\n', text)
    words = [word.replace('\n', '<br>') for word in words]
    
    words_html = []
    for i, word in enumerate(words):
        words_html.append(f'<span class="word" id="word-{i}">{word}</span>')
    words_html = ' '.join(words_html)
    
    html = f"""
    <style>
    .word {{
        transition: background-color 0.3s ease;
        padding: 2px 4px;
        border-radius: 3px;
        margin: 2px;
        display: inline-block;
    }}
    .controls-container {{
        display: flex;
        gap: 20px;
        align-items: center;
        margin-bottom: 20px;
    }}
    #player {{
        flex-grow: 1;
        height: 50px;
    }}
    .speed-selector {{
        padding: 8px 12px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }}
    .text-display {{
        line-height: 2;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background: #f9f9f9;
        margin-top: 20px;
        max-height: 300px;
        overflow-y: auto;
    }}
    </style>

    <div class="controls-container">
        <audio id="player" controls style="width: 100%">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        <select class="speed-selector" id="speedSelect">
            <option value="0.5">0.5x</option>
            <option value="0.75">0.75x</option>
            <option value="1" selected>1x</option>
            <option value="1.5">1.5x</option>
            <option value="2">2x</option>
        </select>
    </div>

    <div class="text-display">
        {words_html}
    </div>

    <script>
        const audio = document.getElementById('player');
        const speedSelect = document.getElementById('speedSelect');
        const words = document.getElementsByClassName('word');
        const totalDuration = {duration};
        const wordCount = {len(words)};
        let timePerWord = totalDuration / wordCount;
        
        // Speed control handler
        speedSelect.addEventListener('change', function() {{
            audio.playbackRate = parseFloat(this.value);
        }});
        
        // Highlighting logic
        audio.addEventListener('timeupdate', function() {{
            const currentTime = audio.currentTime;
            let currentIndex = Math.floor(currentTime / timePerWord);
            currentIndex = Math.min(currentIndex, wordCount - 1);
            
            Array.from(words).forEach(word => {{
                word.style.backgroundColor = 'transparent';
                word.style.color = '#333';
            }});
            
            if(words[currentIndex]) {{
                words[currentIndex].style.backgroundColor = '#4CAF50';
                words[currentIndex].style.color = 'white';
                // Auto-scroll to current word
                words[currentIndex].scrollIntoView({{
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                }});
            }}
        }});
        
        // Initialize playback speed
        audio.playbackRate = 1;
    </script>
    """
    return html

def main():
    st.title("Text to Speech with Word Highlighting")
    
    text = st.text_area("Enter text to convert to speech:", height=200,
                       placeholder="Type or paste your text here...")
    
    if st.button("Generate Speech"):
        if not text.strip():
            st.warning("Please enter some text")
            return
            
        with st.spinner("Generating audio..."):
            audio_bytes, duration = generate_audio(text)
            
        st.components.v1.html(
            create_audio_player(audio_bytes, text, duration),
            height=500,
        )

if __name__ == "__main__":
    main()