
import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit
import wikipedia
import webbrowser
import subprocess
import pyjokes
import requests


# ---------------- INITIALIZATION ----------------

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


# ---------------- SPEAK FUNCTION ----------------

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# ---------------- LISTEN FUNCTION ----------------

def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source, duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=7
            )

        command = recognizer.recognize_google(audio)

        print("You:", command)

        return command.lower()

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""

    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""

    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

    except OSError:
        speak("Microphone is not available.")
        return ""


# ---------------- WEATHER FUNCTION ----------------

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        description = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]

        speak(
            f"The weather in {city} is {description}. "
            f"The temperature is {temperature} degrees Celsius. "
            f"Humidity is {humidity} percent."
        )

    except Exception:
        speak("Sorry, I could not get the weather information.")


# ---------------- MAIN ASSISTANT ----------------

def run_assistant():

    speak("Hello! I am your voice assistant.")
    speak("How can I help you?")

    while True:

        command = listen()

        if not command:
            continue

        # Greetings
        elif (
            "hello" in command
            or "hi" in command
            or "good morning" in command
            or "good evening" in command
        ):
            speak("Hello! Nice to meet you. How can I help you?")

        # Conversation
        elif "how are you" in command:
            speak(
                "I am doing great! Thank you for asking. "
                "How are you?"
            )

        elif "nice to meet" in command:
            speak("It is nice to meet you too!")

        elif "your name" in command:
            speak("I am your personal voice assistant.")

        elif "thank you" in command or "thanks" in command:
            speak("You are most welcome!")

        elif "who created" in command:
            speak("I was created by Aparna using Python.")

        elif "i am fine" in command or "i am good" in command:
            speak("That's wonderful! How can I help you today?")

        # Current time
        elif "time" in command:
            current_time = datetime.datetime.now().strftime(
                "%I:%M %p"
            )
            speak("The current time is " + current_time)

        # Current date
        elif "date" in command:
            today = datetime.datetime.now().strftime(
                "%d %B %Y"
            )
            speak("Today's date is " + today)

        # Weather information
        elif "weather in" in command:
            city = command.split("weather in", 1)[1].strip()

            if city:
                get_weather(city)
            else:
                speak("Please tell me the city name.")

        # Search Google
        elif "search" in command:
            query = command.replace("search", "", 1).strip()

            if query:
                speak("Searching for " + query)
                pywhatkit.search(query)
            else:
                speak("Please tell me what to search for.")

        # Wikipedia information
        elif "who is" in command or "what is" in command:
            try:
                topic = (
                    command.replace("who is", "")
                    .replace("what is", "")
                    .strip()
                )

                result = wikipedia.summary(
                    topic,
                    sentences=2
                )

                speak(result)

            except Exception:
                speak(
                    "Sorry, I could not find information about that."
                )

        # Open YouTube
        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        # Open Google
        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # Open Notepad
        elif "open notepad" in command:
            speak("Opening Notepad")
            subprocess.Popen("notepad.exe")

        # Open Calculator
        elif "open calculator" in command:
            speak("Opening Calculator")
            subprocess.Popen("calc.exe")

        # Tell a joke
        elif "joke" in command:
            joke = pyjokes.get_joke()
            speak(joke)

        # Exit assistant
        elif (
            "stop" in command
            or "exit" in command
            or "goodbye" in command
        ):
            speak("Goodbye! Have a nice day.")
            break

        # Unknown commands
        else:
            speak("Sorry, I cannot perform that task yet.")


# ---------------- START PROGRAM ----------------

if __name__ == "__main__":
    run_assistant()
