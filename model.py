# import whisper
# model = whisper.load_model("medium")
# print("model loaded successfully")
# result = model.transcribe("D:\\Seeta\\backend\\audio.wav", language="en")

# print(result["segments"])

# print(r"C:\newaudio.wav")

import os
import whisper

# Set the path to ffmpeg manually for this script
os.environ["PATH"] += os.pathsep + r"C:\Users\apjmu\Downloads\ffmpeg-7.1-essentials_build\ffmpeg-7.1-essentials_build\bin"

# Load the model
model = whisper.load_model("medium")
print("Model loaded successfully")

# Transcribe the audio
result = model.transcribe(r"C:\newaudio.wav", language="en")
print(result["segments"])
