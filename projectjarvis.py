import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import subprocess
import platform
import webbrowser

# Initialize the voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0=male, 1=female

def talk(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening for 'Jarvis'...")
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
        command = ""
        try:
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"🗣️ You said: {command}")
        except sr.UnknownValueError:
            print("❌ Sorry, I didn’t catch that.")
        except sr.RequestError:
            print("⚠️ Couldn’t connect to speech service.")
    return command

# Open apps based on system
def open_app(app_name):
    system_name = platform.system()
    try:
        if app_name == "chrome":
            if system_name == "Darwin":
                subprocess.run(["open", "-a", "Google Chrome"])
            elif system_name == "Windows":
                os.startfile("chrome")
            elif system_name == "Linux":
                subprocess.run(["google-chrome"])
        elif app_name == "spotify":
            if system_name == "Darwin":
                subprocess.run(["open", "-a", "Spotify"])
            elif system_name == "Windows":
                os.startfile("spotify")
            elif system_name == "Linux":
                subprocess.run(["spotify"])
        elif app_name == "vscode":
            if system_name == "Darwin":
                subprocess.run(["open", "-a", "Visual Studio Code"])
            elif system_name == "Windows":
                os.startfile("Code")  # VS Code executable on Windows
            elif system_name == "Linux":
                subprocess.run(["code"])
        elif app_name == "brave":
            if system_name == "Darwin":
                subprocess.run(["open", "-a", "Brave Browser"])
            elif system_name == "Windows":
                os.startfile("brave")
            elif system_name == "Linux":
                subprocess.run(["brave-browser"])
        elif app_name == "github":
            webbrowser.open("https://github.com")
        elif app_name == "facetime":
            if system_name == "Darwin":
                subprocess.run(["open", "-a", "FaceTime"])
            else:
                talk("FaceTime is only available on macOS.")
                return
        talk(f"Opening {app_name}")
    except Exception as e:
        talk(f"Sorry, I could not open {app_name}. Error: {e}")

def run_jarvis():
    command = take_command()

    if 'jarvis' in command:
        command = command.replace("jarvis", "").strip()
        if not command:
            talk("Yes sir? What should I do?")
            return

        print(f"✨ Command detected: {command}")

        # Play on YouTube
        if 'play' in command:
            song = command.replace('play', '').strip()
            if song:
                talk(f'Playing {song}')
                pywhatkit.playonyt(song)
            else:
                talk("Please tell me the song name after 'play'.")

        # Time
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f'Current time is {time}')

        # Date
        elif 'date' in command:
            date = datetime.datetime.now().strftime('%A, %B %d, %Y')
            talk(f'Today is {date}')

        # Wikipedia search
        elif 'who is' in command:
            person = command.replace('who is', '').strip()
            try:
                info = wikipedia.summary(person, 1)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk(f"Multiple results found for {person}, please be more specific.")
            except wikipedia.exceptions.PageError:
                talk(f"Sorry, I could not find any information about {person}.")

        # Joke
        elif 'joke' in command:
            talk(pyjokes.get_joke())

        # Open apps
        elif 'open chrome' in command or 'launch chrome' in command:
            open_app("chrome")
        elif 'open spotify' in command or 'launch spotify' in command:
            open_app("spotify")
        elif 'open vs code' in command or 'launch vscode' in command or 'open visual studio' in command:
            open_app("vscode")
        elif 'open github' in command or 'launch github' in command:
            open_app("github")
        elif 'open brave' in command or 'launch brave' in command:
            open_app("brave")
        elif 'open facetime' in command or 'launch facetime' in command:
            open_app("facetime")

        # Stop / exit
        elif 'stop' in command or 'bye' in command:d
            exit()

        else:
            talk("Sorry, I didn’t understand that. Can you repeat?")
    else:
        print("⏸️ No wake word detected. Say something with 'Jarvis' to give a command.")

# Run Jarvis continuously
while True:
    run_jarvis()
