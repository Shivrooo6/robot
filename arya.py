import os
import datetime
import speech_recognition as sr
import pyttsx3
import wikipedia
import pyjokes
import webbrowser
from googletrans import Translator

# === SETTINGS ===
TARGET_LANGUAGE = "hi"  # Change to any language code (e.g. 'en', 'es', 'hi', 'fr')

# === SETUP ===
listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
translator = Translator()

# === TALK ===
def talk(text):
    print("Assistant:", text)
    translated = translator.translate(text, dest=TARGET_LANGUAGE).text
    print("Translated:", translated)
    engine.say(translated)
    engine.runAndWait()

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
            talk("I couldn't find detailed information, opening Google for help.")
            webbrowser.open(f"https://www.google.com/search?q={command}")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)

    elif 'search' in command:
        query = command.replace('search', '').strip()
        talk(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    else:
        talk("Let me search that for you.")
        webbrowser.open(f"https://www.google.com/search?q={command}")

# === MAIN LOOP ===
if __name__ == "__main__":
    while True:
        run_arya()
