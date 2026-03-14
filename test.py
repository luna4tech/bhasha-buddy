from gtts import gTTS
import whisper_timestamped as whisper

audio = whisper.load_audio("/Users/jyellumahanti/projects/bhasha-buddy/resources/Telugu/తెలివైన మేక/audio.mp3")
model = whisper.load_model("base")


data = whisper.transcribe(model, audio, language="te", task='transcribe')
print(data)