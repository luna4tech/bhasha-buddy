import streamlit as st
import speech_recognition as sr

st.title("Real-Time Audio Transcription with SpeechRecognition API")

# Initialize recognizer
recognizer = sr.Recognizer()

st.write("Click 'Start Transcription' to capture your voice in real-time.")

# Button to start transcription
if st.button("Start Transcription"):
    st.write("Listening... Speak into your microphone.")
    try:
        # Use the microphone for input
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
            st.write("Processing transcription...")
            
            # Transcribe using Google Web Speech API
            transcription = recognizer.recognize_google(audio)
            st.subheader("Transcription Result:")
            st.write(transcription)
    except sr.UnknownValueError:
        st.error("Could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
