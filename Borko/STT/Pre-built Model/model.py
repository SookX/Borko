import speech_recognition as sr
import os

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