import json
import logging
import whisper
from scipy.io.wavfile import write
from pydub import AudioSegment
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
import magic
import requests
import base64
import numpy as np
from pydub import AudioSegment
import soundfile as sf


def ogg2wav(ofn):
    wfn = ofn.replace('.ogg','.wav')
    x = AudioSegment.from_file(ofn)
    x.export(wfn, format='wav') 
logger = logging.getLogger(__name__)

import speech_recognition as sr
import os

URL = "https://e97f-146-19-88-218.ngrok-free.app"

def prebuilt_speech_to_text_from_audio(audio_path: str) -> str:

    """
    Converts speech to text from an audio file using Google's Web Speech API.

    This function takes the path to an audio file, processes it using the `SpeechRecognition` library,
    and returns the recognized text in Bulgarian (language code: "bg-BG"). If the file does not exist 
    or if there is an issue with the API, appropriate messages will be printed.

    Parameters:
        audio_path (str): The path to the audio file .

    Returns:
        str: The recognized text from the audio file.
             Returns `None` if the audio cannot be processed or recognized.
    """
    if not os.path.exists(audio_path):
        print("File not found. Check the audio path!")
        return
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as s:
        audio = recognizer.record(s)
    try:
        text = recognizer.recognize_google(audio, language="bg-BG")

    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"API request error: {e}")

    return text



class AudioConsumer(AsyncWebsocketConsumer):

    
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connected.")

    async def disconnect(self, close_code):
        logger.info("WebSocket disconnected.")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            logger.info("Received audio chunk.")
            transcript = await self.transcribe_audio(bytes_data)
            await self.send(text_data=json.dumps({"transcript": transcript}))

    async def transcribe_audio(self, audio_data):
        """ Convert received WebM audio bytes to WAV and transcribe with Whisper """

        

        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(audio_data)
        
        if(file_type == "audio/x-wav"):
            with open("output.wav", "wb") as ogg_file:
                ogg_file.write(audio_data)
            

            text = prebuilt_speech_to_text_from_audio('./output.wav')

            
            model_output = requests.post(url=URL, json= {"prompt": text})

            tts = requests.post(f'{URL}/tts', json={'text': model_output.json()['message']}).json()
           
            tts_audio = tts['audio_data']
            tts_sampling_rate = tts['sampling_rate']

            sf.write("tts_output.wav", tts_audio, tts_sampling_rate)


            with open("tts_output.wav", "rb") as audio_file:
                audio_d = audio_file.read()

            enc = base64.b64encode(audio_d).decode('utf-8')
            
            return {
                'audio': enc,
                'sampling_rate': tts_sampling_rate
            }
        
        

        print(f"Detected MIME Type: {file_type}")


