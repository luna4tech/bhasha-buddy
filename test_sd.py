import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import io
import whisper
import time
from collections import deque

# Parameters
SAMPLE_RATE = 44100  # Sample rate in Hz
FRAME_DURATION = 0.1  # 100ms frame size
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION)  # Samples per frame
PAUSE_DURATION = 1.0  # Pause duration in seconds to stop recording
ENERGY_THRESHOLD = 0.5  # Relative energy drop threshold (adjustable)
WINDOW_SIZE = 10  # Number of frames to track moving energy
TIMEOUT_DURATION = 3  # Timeout in seconds

# Load Whisper model
model = whisper.load_model("base")  # You can use "small", "medium", "large" for better accuracy

def compute_energy(audio_frame):
    """Compute short-term energy of the audio frame."""
    return np.sum(audio_frame ** 2) / len(audio_frame)

def record_audio():
    st.write("Recording... Speak now!")

    audio_data = []
    recording = True
    silence_counter = 0
    energy_window = deque(maxlen=WINDOW_SIZE)  # Store last few energy values
    start_time = time.time()  # Record start time

    def callback(indata, frames, time, status):
        nonlocal recording, silence_counter
        
        # Compute frame energy
        energy = compute_energy(indata)
        energy_window.append(energy)
        
        # Compute moving average of past frames
        avg_energy = np.mean(energy_window) if energy_window else energy

        # Detect silence based on relative energy drop
        if avg_energy > 0 and energy < avg_energy * ENERGY_THRESHOLD:
            silence_counter += 1
        else:
            silence_counter = 0
        
        # Stop recording if pause detected
        if silence_counter >= (PAUSE_DURATION / FRAME_DURATION):
            recording = False
        
        audio_data.append(indata.copy())

    # Start recording stream
    with sd.InputStream(callback=callback, samplerate=SAMPLE_RATE, channels=1):
        while recording:
            # Check for timeout
            if time.time() - start_time > TIMEOUT_DURATION:
                st.write("Timeout reached. Stopping recording.")
                recording = False
            sd.sleep(int(FRAME_DURATION * 1000))  # Sleep for frame duration

    st.write("Recording stopped.")

    # Convert to WAV format
    audio_array = np.concatenate(audio_data, axis=0)
    byte_io = io.BytesIO()
    with wave.open(byte_io, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((audio_array * 32767).astype(np.int16).tobytes())

    return byte_io.getvalue()

def transcribe_audio(audio_bytes):
    """Send the audio data to Whisper for transcription."""
    # Save audio bytes to a temporary file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)

    # Transcribe using Whisper
    result = model.transcribe("temp_audio.wav")
    return result['text']

# Streamlit UI
st.title("Streamlit Audio Input with Timeout and Whisper Transcription")

if st.button("Start Recording"):
    audio_bytes = record_audio()
    st.audio(audio_bytes, format="audio/wav")  # Play back recorded audio

    # Transcribe the audio with Whisper
    transcription = transcribe_audio(audio_bytes)
    st.write("Transcription:")
    st.write(transcription)
