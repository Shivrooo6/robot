import os
import datetime
import speech_recognition as sr
import wikipedia
import pyjokes
import webbrowser
from googletrans import Translator
from transformers import pipeline
from TTS.api import TTS
import face_recognition
import cv2
import soundfile as sf
import torch
from speechbrain.pretrained import SpeakerRecognition

# === SETTINGS ===
TARGET_LANGUAGE = "hi"
AUTHORIZED_VOICE_PATH = "ownervoice.wav"
AUTHORIZED_FACE_PATH = "ownerimage.jpg"

# === SETUP ===
listener = sr.Recognizer()
tts_model = TTS(model_name="tts_models/en/vctk/vits")
default_speaker = tts_model.speakers[0]
translator = Translator()
qa_pipeline = pipeline("question-answering")
verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# === FUNCTIONS ===

def talk(text):
    print("Assistant:", text)
    try:
        translated = translator.translate(text, dest=TARGET_LANGUAGE).text
    except:
        translated = text
    tts_model.tts_to_file(text=translated, speaker=default_speaker, file_path="output.wav")
    os.system("aplay output.wav" if os.name != "nt" else "start output.wav")

def verify_face():
    try:
        known_img = face_recognition.load_image_file(AUTHORIZED_FACE_PATH)
        known_encoding = face_recognition.face_encodings(known_img)[0]

        cam = cv2.VideoCapture(0)
        result, frame = cam.read()
        cam.release()
        cv2.destroyAllWindows()

        if not result:
            return False

        unknown_encoding = face_recognition.face_encodings(frame)
        if unknown_encoding and face_recognition.compare_faces([known_encoding], unknown_encoding[0])[0]:
            return True
    except:
        pass
    return False

def verify_voice():
    try:
        with sr.Microphone() as source:
            print("Listening for voice verification...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5)
            with open("temp.wav", "wb") as f:
                f.write(voice.get_wav_data())
        score, _ = verification.verify_files(AUTHORIZED_VOICE_PATH, "temp.wav")
        os.remove("temp.wav")
        return score > 0.75
    except:
        return False

def take_command():
    try:
        with sr.Microphone() as source:
            print("Waiting for hotword 'Arya'...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=10)
            command = listener.recognize_google(voice).lower()
            print(f"You said: {command}")
            if 'arya' in command:
                talk("Yes, how can I help you?")
                voice = listener.listen(source, timeout=5)
                command = listener.recognize_google(voice).lower()
                print(f"Command: {command}")
                return command
    except sr.UnknownValueError:
        talk("Sorry, I didn't understand.")
    except sr.RequestError:
        talk("Could not connect to recognition service.")
    except sr.WaitTimeoutError:
        pass
    return ""

def answer_from_nlp(question):
    context = (
        "India is a country in South Asia. Its capital is New Delhi. "
        "It is known for its diverse culture, languages, and traditions. "
        "The Prime Minister of India is Narendra Modi."
    )
    try:
        result = qa_pipeline(question=question, context=context)
        return result["answer"]
    except:
        return "Sorry, I couldn't answer that."

def run_arya():
    command = take_command()
    if not command:
        return

    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song}")
        os.system(f"xdg-open https://www.youtube.com/results?search_query={song}")

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The time is {current_time}")

    elif 'who is' in command or 'what is' in command or 'define' in command:
        try:
            info = wikipedia.summary(command, sentences=1)
            talk(info)
        except:
            answer = answer_from_nlp(command)
            talk(answer if answer else "I couldn't find that. Let me search it.")
            webbrowser.open(f"https://www.google.com/search?q={command}")

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'search' in command:
        query = command.replace('search', '').strip()
        talk(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'exit' in command or 'quit' in command:
        talk("Goodbye!")
        exit()

    else:
        answer = answer_from_nlp(command)
        if answer:
            talk(answer)
        else:
            talk("Let me search that for you.")
            webbrowser.open(f"https://www.google.com/search?q={command}")

# === MAIN ===
if __name__ == "__main__":
    talk("Starting voice assistant...")
    if verify_face() and verify_voice():
        talk("Welcome back, verified successfully.")
        while True:
            run_arya()
    else:
        talk("Verification failed. Access denied.")
        exit()
# === END OF CODE ===