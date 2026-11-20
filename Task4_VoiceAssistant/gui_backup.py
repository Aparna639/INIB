
import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import webbrowser
import subprocess
import pyjokes
import requests
import threading
import queue


# ---------------- THEME ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BACKGROUND = "#0B1220"
CARD = "#151F32"
BLUE = "#2563EB"
CYAN = "#38BDF8"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
GREEN = "#22C55E"
RED = "#DC2626"


# ---------------- MAIN WINDOW ----------------

app = ctk.CTk()
app.title("Aparna AI - Voice Assistant")
app.geometry("950x750")
app.minsize(800, 650)
app.configure(fg_color=BACKGROUND)


# ---------------- GLOBAL VARIABLES ----------------

message_queue = queue.Queue()
stop_event = threading.Event()
assistant_thread = None

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


# ---------------- SPEAK FUNCTION ----------------

def speak(text):
    message_queue.put(("assistant", text))

    engine.say(text)
    engine.runAndWait()


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


# ---------------- LISTEN FUNCTION ----------------

def listen(recognizer, source):
    try:
        audio = recognizer.listen(
            source,
            timeout=1,
            phrase_time_limit=7
        )

        command = recognizer.recognize_google(audio)

        print("You:", command)

        return command.lower()

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

    except OSError:
        speak("Microphone error.")
        return ""


# ---------------- COMMAND PROCESSING ----------------

def process_command(command):

    if not command:
        return

    message_queue.put(("user", command))

    # Greetings
    if any(word in command for word in [
        "hello", "hi", "good morning", "good evening"
    ]):
        speak("Hello! Nice to meet you. How can I help you?")

    # Conversation
    elif "how are you" in command:
        speak("I am doing great! Thank you for asking.")

    elif "nice to meet" in command:
        speak("It is nice to meet you too!")

    elif "your name" in command:
        speak("I am Aparna AI, your personal voice assistant.")

    elif "thank you" in command or "thanks" in command:
        speak("You are most welcome!")

    elif "who created" in command:
        speak("I was created by Aparna using Python.")

    elif "i am fine" in command or "i am good" in command:
        speak("That's wonderful! How can I help you today?")

    # Time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    # Date
    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak("Today's date is " + today)

    # Weather
    elif "weather in" in command:
        city = command.split("weather in", 1)[1].strip()

        if city:
            get_weather(city)
        else:
            speak("Please tell me the city name.")

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

    # Jokes
    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    # Google search
    elif "search" in command:
        query = command.replace("search", "", 1).strip()

        if query:
            speak("Searching for " + query)
            pywhatkit.search(query)
        else:
            speak("Please tell me what to search for.")

    # Wikipedia
    elif "who is" in command or "what is" in command:
        try:
            topic = (
                command.replace("who is", "")
                .replace("what is", "")
                .strip()
            )

            result = wikipedia.summary(topic, sentences=2)
            speak(result)

        except Exception:
            speak("Sorry, I could not find that information.")

    # Exit
    elif any(word in command for word in [
        "stop assistant", "exit assistant", "goodbye", "quit assistant"
    ]):
        speak("Goodbye! Have a nice day.")
        stop_event.set()
        message_queue.put(("status", "STOPPED"))

    else:
        speak("Sorry, I cannot perform that task yet.")


# ---------------- ASSISTANT THREAD ----------------

def assistant_worker():

    message_queue.put(("status", "LISTENING"))
    speak("Hello! I am Aparna AI.")
    speak("How can I help you?")

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            message_queue.put(("status", "CALIBRATING"))
            recognizer.adjust_for_ambient_noise(source, duration=1)

            message_queue.put(("status", "LISTENING"))

            while not stop_event.is_set():

                command = listen(recognizer, source)

                if stop_event.is_set():
                    break

                if command:
                    message_queue.put(("status", "PROCESSING"))
                    process_command(command)

                    if not stop_event.is_set():
                        message_queue.put(("status", "LISTENING"))

    except OSError:
        speak("Microphone is not available.")
        message_queue.put(("status", "ERROR"))

    except Exception as error:
        print("Error:", error)
        message_queue.put(("status", "ERROR"))

    message_queue.put(("status", "STOPPED"))


# ---------------- GUI FUNCTIONS ----------------

def add_message(sender, message):

    chat_box.configure(state="normal")

    if sender == "user":
        chat_box.insert("end", f"\nYou: {message}\n")

    elif sender == "assistant":
        chat_box.insert("end", f"\nAparna AI: {message}\n")

    chat_box.see("end")
    chat_box.configure(state="disabled")


def start_assistant():

    global assistant_thread

    if assistant_thread and assistant_thread.is_alive():
        return

    stop_event.clear()

    status_label.configure(
        text="● STARTING ASSISTANT",
        text_color=CYAN
    )

    instruction.configure(
        text="Preparing microphone..."
    )

    start_button.configure(state="disabled")

    assistant_thread = threading.Thread(
        target=assistant_worker,
        daemon=True
    )

    assistant_thread.start()


def stop_assistant():

    stop_event.set()

    status_label.configure(
        text="● STOPPING",
        text_color=RED
    )

    instruction.configure(
        text="Stopping assistant..."
    )

    start_button.configure(state="normal")


def update_gui():

    try:
        while True:

            event, value = message_queue.get_nowait()

            if event == "user" or event == "assistant":
                add_message(event, value)

            elif event == "status":

                status_label.configure(
                    text="● " + value,
                    text_color=(
                        GREEN if value == "LISTENING"
                        else RED if value in ["STOPPED", "ERROR"]
                        else CYAN
                    )
                )

                instruction.configure(
                    text={
                        "LISTENING": "Speak your command now...",
                        "PROCESSING": "Processing your command...",
                        "CALIBRATING": "Adjusting microphone...",
                        "STOPPED": "Assistant is stopped.",
                        "ERROR": "Please check your microphone."
                    }.get(value, value)
                )

                if value in ["STOPPED", "ERROR"]:
                    start_button.configure(state="normal")

    except queue.Empty:
        pass

    app.after(100, update_gui)


# ---------------- HEADER ----------------

header = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=15
)

header.pack(fill="x", padx=25, pady=(20, 10))

title = ctk.CTkLabel(
    header,
    text="APARNA AI",
    font=("Arial", 30, "bold"),
    text_color=CYAN
)

title.pack(pady=(15, 3))

subtitle = ctk.CTkLabel(
    header,
    text="YOUR PERSONAL VOICE ASSISTANT",
    font=("Arial", 12),
    text_color=MUTED
)

subtitle.pack(pady=(0, 15))


# ---------------- STATUS ----------------

status_label = ctk.CTkLabel(
    app,
    text="● SYSTEM READY",
    font=("Arial", 16, "bold"),
    text_color=GREEN
)

status_label.pack(pady=12)


# ---------------- MICROPHONE BUTTON ----------------

mic_button = ctk.CTkButton(
    app,
    text="🎙",
    width=125,
    height=125,
    corner_radius=65,
    fg_color=BLUE,
    hover_color="#1D4ED8",
    font=("Arial", 45),
    command=start_assistant
)

mic_button.pack(pady=15)


instruction = ctk.CTkLabel(
    app,
    text="Click START ASSISTANT to begin",
    font=("Arial", 14),
    text_color=MUTED
)

instruction.pack(pady=5)


# ---------------- CONVERSATION PANEL ----------------

chat_frame = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=15
)

chat_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)

chat_title = ctk.CTkLabel(
    chat_frame,
    text="CONVERSATION",
    font=("Arial", 18, "bold"),
    text_color=CYAN
)

chat_title.pack(anchor="w", padx=20, pady=(15, 5))


chat_box = ctk.CTkTextbox(
    chat_frame,
    fg_color=BACKGROUND,
    text_color=WHITE,
    font=("Arial", 14),
    corner_radius=10
)

chat_box.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

chat_box.insert(
    "end",
    "Aparna AI: Hello! Welcome to Aparna AI.\n"
    "Aparna AI: Click Start Assistant to begin.\n"
)

chat_box.configure(state="disabled")


# ---------------- CONTROL BUTTONS ----------------

button_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

button_frame.pack(pady=(0, 20))


start_button = ctk.CTkButton(
    button_frame,
    text="START ASSISTANT",
    width=180,
    height=45,
    fg_color=BLUE,
    hover_color="#1D4ED8",
    command=start_assistant
)

start_button.pack(side="left", padx=10)


stop_button = ctk.CTkButton(
    button_frame,
    text="STOP ASSISTANT",
    width=180,
    height=45,
    fg_color=RED,
    hover_color="#991B1B",
    command=stop_assistant
)

stop_button.pack(side="left", padx=10)


# ---------------- WINDOW CLOSE ----------------

def close_application():
    stop_event.set()
    app.destroy()


app.protocol("WM_DELETE_WINDOW", close_application)


# ---------------- START GUI ----------------

app.after(100, update_gui)
app.mainloop()
