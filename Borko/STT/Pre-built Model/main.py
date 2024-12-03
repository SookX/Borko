from model import prebuilt_speech_to_text_from_audio
import os

audio_path = os.path.join(os.getcwd(), "Borko", "STT", "dist", "obesvaneto.wav")
text = prebuilt_speech_to_text_from_audio(audio_path)

print(text)