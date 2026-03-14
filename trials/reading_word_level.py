import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
import pyttsx3
import time

text = """
A hare and tortoise lived in a distant jungle. But the hare always mocked the tortoise.

“You are so slow, do you ever make it on time?”

Offended by the rude tone, the tortoise replied in a humble tone.

“Don’t be so arrogant, let’s compete in a race, and see who’s faster!”

The hare burst into laughter and declared the other side of the hill as the final point.

Both the animals started off, and the hare ran faster to reach the finish line in no time!

Soon the hare felt exhausted and stopped for a quick nap. 

As the overconfident hare dozed off, the tortoise quietly surpassed him. By the time the hare woke up and ran to the finish point, the tortoise had already won the race!
"""
words = text.split()

def read_text_gtts(text):
    tts = gTTS(text=text, lang='en')

    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    audio_bytes = audio_buffer.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
  

    audio_html = f"""
        <audio id="audio" controls>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
        </audio>
        """
    text_html = "<div id='textContainer' style='font-size: 1.2em; line-height: 2em;'>"
    for i, word in enumerate(words):
        text_html += f"<span id='word{i}'>{word} </span>"
    text_html += "</div>"

    script = f"""
        <script>
        const audio = document.getElementById('audio');
        const words = document.querySelectorAll('#textContainer span');
        const totalWords = words.length;

        // Once metadata is loaded, we can compute duration per word
        audio.addEventListener('loadedmetadata', () => {{
            const durationPerWord = audio.duration / totalWords;
            audio.addEventListener('timeupdate', () => {{
                const currentTime = audio.currentTime;
                const currentWordIndex = Math.floor(currentTime / durationPerWord);
                words.forEach((w, index) => {{
                    if (index === currentWordIndex) {{
                        w.style.backgroundColor = 'yellow';
                    }} else {{
                        w.style.backgroundColor = 'transparent';
                    }}
                }});
            }});
        }});
        </script>
    """

    # Combine the HTML parts
    full_html = audio_html + text_html + script

    # Render the custom component in Streamlit
    st.components.v1.html(full_html, height=300)



st.write(text)
if st.button('Read'):
    read_text_gtts(text)