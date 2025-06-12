import os
import datetime
import speech_recognition as sr
import wikipedia
import pyjokes
import webbrowser
from googletrans import Translator
from transformers import pipeline
from TTS.api import TTS  # Coqui TTS for human-like voice

# === SETTINGS ===
TARGET_LANGUAGE = "hi"  # e.g. "en" = English, "hi" = Hindi, "fr" = French

# === SETUP ===
listener = sr.Recognizer()
tts_model = TTS(model_name="tts_models/en/vctk/vits")
translator = Translator()
qa_pipeline = pipeline("question-answering")  # Load Hugging Face QA model once

# === TALK (Human-like voice) ===
def talk(text):
    print("Assistant:", text)
    try:
        translated = translator.translate(text, dest=TARGET_LANGUAGE).text
    except Exception:
        translated = text  # fallback
    print("Translated:", translated)
    tts_model.tts_to_file(text=translated, file_path="output.wav")
    os.system("aplay output.wav" if os.name != "nt" else "start output.wav")

# === VOICE TO TEXT ===
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice).lower()
            print(f"You said: {command}")
            if 'arya' in command:
                command = command.replace('arya', '').strip()
            return command
    except sr.WaitTimeoutError:
        talk("No input detected.")
    except sr.UnknownValueError:
        talk("Sorry, I did not catch that.")
    except sr.RequestError:
        talk("Could not connect to the recognition service.")
    return ""

# === NLP QUESTION HANDLER ===
def answer_from_nlp(question):
    context = (
        "India is a country in South Asia. Its capital is New Delhi. "
        "It is known for its diverse culture, languages, and traditions. "
        "The Prime Minister of India is Narendra Modi."
    )
    try:
        result = qa_pipeline(question=question, context=context)
        return result["answer"]
    except Exception:
        return "Sorry, I couldn't answer that."

# === COMMAND LOGIC ===
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
            if answer:
                talk(answer)
            else:
                talk("I couldn't find that, searching online.")
                webbrowser.open(f"https://www.google.com/search?q={command}")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)

    elif 'search' in command:
        query = command.replace('search', '').strip()
        talk(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    else:
        answer = answer_from_nlp(command)
        if answer:
            talk(answer)
        else:
            talk("Let me search that for you.")
            webbrowser.open(f"https://www.google.com/search?q={command}")

# === MAIN LOOP ===
if __name__ == "__main__":
    while True:
        run_arya()
        if 'exit' in take_command():
            talk("Goodbye!")
            break
