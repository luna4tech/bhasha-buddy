import streamlit as st
import whisper_timestamped as whisper
from scipy.io import wavfile
import tempfile
import os

model = whisper.load_model("base")
audio_bytes = st.audio_input("Record")
if audio_bytes:
    # Save the audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_bytes.getvalue())
        audio_path = temp_audio_file.name

    st.write("Audio file saved successfully!")

    try:
        # Transcribe the audio using Whisper
        st.write("Transcribing audio...")
        result = model.transcribe(audio_path)
        st.subheader("Transcription Result:")
        st.write(result['text'])
    except Exception as e:
        st.error(f"Error during transcription: {e}")
    finally:
        # Clean up the temporary file
        os.remove(audio_path)