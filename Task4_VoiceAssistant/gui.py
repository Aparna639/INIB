
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
import os

from PIL import Image, ImageDraw

# -------------------- APP SETTINGS --------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Aparna AI - Voice Assistant")
app.geometry("1000x720")
app.minsize(850, 620)
app.configure(fg_color="#0B1220")

# -------------------- COLORS --------------------

BG = "#0B1220"
CARD = "#151F32"
BLUE = "#2563EB"
CYAN = "#38BDF8"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
GREEN = "#22C55E"
RED = "#EF4444"
USER_BUBBLE = "#1D4ED8"
AI_BUBBLE = "#1E293B"

# -------------------- VOICE ENGINE --------------------

engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
voice_map = {}

for index, voice in enumerate(voices):
    display_name = f"{index + 1}. {voice.name}"
    voice_map[display_name] = voice.id

voice_options = list(voice_map.keys())

if not voice_options:
    voice_options = ["Default"]

tts_lock = threading.Lock()

# -------------------- ASSISTANT VARIABLES --------------------

message_queue = queue.Queue()
stop_event = threading.Event()
assistant_thread = None

is_listening = False
animation_step = 0

recognizer = sr.Recognizer()

# -------------------- CHAT FUNCTIONS --------------------

def add_message(sender, message):

    is_user = sender == "You"

    bubble_color = USER_BUBBLE if is_user else AI_BUBBLE
    anchor = "e" if is_user else "w"

    message_frame = ctk.CTkFrame(
        chat_frame,
        fg_color="transparent"
    )
    message_frame.pack(
        fill="x",
        padx=12,
        pady=6
    )

    bubble = ctk.CTkFrame(
        message_frame,
        fg_color=bubble_color,
        corner_radius=15
    )
    bubble.pack(
        anchor=anchor,
        padx=5
    )

    sender_label = ctk.CTkLabel(
        bubble,
        text=sender,
        font=("Arial", 11, "bold"),
        text_color=CYAN if not is_user else "#DBEAFE"
    )
    sender_label.pack(
        anchor="w",
        padx=12,
        pady=(8, 2)
    )

    message_label = ctk.CTkLabel(
        bubble,
        text=message,
        font=("Arial", 13),
        text_color=WHITE,
        wraplength=520,
        justify="left"
    )
    message_label.pack(
        anchor="w",
        padx=12,
        pady=(2, 10)
    )

    chat_frame.after(
        100,
        lambda: chat_frame._parent_canvas.yview_moveto(1.0)
    )


def clear_chat():

    for widget in chat_frame.winfo_children():
        widget.destroy()

    add_message(
        "Aparna AI",
        "Conversation cleared. How can I help you?"
    )


# -------------------- SPEAK FUNCTION --------------------

def speak(text):

    message_queue.put(
        ("message", "Aparna AI", text)
    )

    try:
        with tts_lock:
            engine.say(text)
            engine.runAndWait()

    except Exception as error:
        print("Speech error:", error)


# -------------------- WEATHER FUNCTION --------------------

def get_weather(city):

    try:
        url = f"https://wttr.in/{city}?format=j1"

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        current = data["current_condition"][0]

        temperature = current["temp_C"]
        description = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]

        return (
            f"The weather in {city} is {description}. "
            f"Temperature is {temperature} degrees Celsius. "
            f"Humidity is {humidity} percent."
        )

    except Exception:
        return "Sorry, I could not get the weather information."


# -------------------- COMMAND PROCESSING --------------------

def process_command(command):

    if not command:
        return

    message_queue.put(
        ("message", "You", command)
    )

    print("Command:", command)

    # Greetings
    if any(word in command for word in [
        "hello", "hi", "hey",
        "good morning", "good evening",
        "good afternoon"
    ]):
        speak("Hello! Welcome. How can I help you?")

    elif "how are you" in command:
        speak("I am doing great. Thank you for asking!")

    elif "nice to meet" in command:
        speak("Nice to meet you too!")

    elif "your name" in command or "who are you" in command:
        speak("I am Aparna AI, your personal voice assistant.")

    elif "who created" in command:
        speak("I was created as a Python voice assistant project.")

    elif "thank you" in command or "thanks" in command:
        speak("You are welcome!")

    elif "i am fine" in command or "i am good" in command:
        speak("That is wonderful to hear!")

    # Time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    # Date
    elif "date" in command or "today" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {today}")

    # Weather
    elif "weather" in command:

        city = command.replace("weather", "")
        city = city.replace("in", "")
        city = city.replace("what is the", "")
        city = city.replace("what's the", "")
        city = city.strip()

        if city:
            speak(get_weather(city))
        else:
            speak("Please tell me the city name.")

    # YouTube
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    # Google
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    # Notepad
    elif "open notepad" in command:
        speak("Opening Notepad.")
        subprocess.Popen("notepad.exe")

    # Calculator
    elif "open calculator" in command:
        speak("Opening Calculator.")
        subprocess.Popen("calc.exe")

    # Jokes
    elif "joke" in command:
        speak(pyjokes.get_joke())

    # Wikipedia
    elif "who is" in command or "what is" in command:

        try:
            topic = command.replace("who is", "")
            topic = topic.replace("what is", "")
            topic = topic.strip()

            if topic:
                result = wikipedia.summary(
                    topic,
                    sentences=2
                )
                speak(result)
            else:
                speak("Please tell me what you want to know.")

        except Exception:
            speak("Sorry, I could not find information about that topic.")

    # Google search
    elif "search" in command:

        query = command.replace("search", "").strip()

        if query:
            speak(f"Searching Google for {query}")
            pywhatkit.search(query)
        else:
            speak("Please tell me what you want to search.")

    # Exit
    elif any(word in command for word in [
        "stop assistant", "exit", "quit", "goodbye", "bye"
    ]):
        speak("Goodbye! Have a wonderful day.")
        stop_event.set()

    else:
        speak("Sorry, I do not know that command yet.")


# -------------------- ASSISTANT THREAD --------------------

def assistant_worker():

    try:
        with sr.Microphone() as source:

            message_queue.put(
                ("status", "Adjusting microphone...")
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            message_queue.put(
                ("status", "Listening...")
            )

            while not stop_event.is_set():

                try:
                    audio = recognizer.listen(
                        source,
                        timeout=1,
                        phrase_time_limit=7
                    )

                    message_queue.put(
                        ("status", "Processing...")
                    )

                    command = recognizer.recognize_google(
                        audio
                    ).lower().strip()

                    process_command(command)

                except sr.WaitTimeoutError:
                    continue

                except sr.UnknownValueError:
                    message_queue.put(
                        ("status", "Listening...")
                    )

                except sr.RequestError:
                    speak(
                        "Speech recognition service is unavailable. "
                        "Please check your internet connection."
                    )

                except Exception as error:
                    print("Assistant error:", error)
                    message_queue.put(
                        ("status", "Listening...")
                    )

    except OSError:
        message_queue.put(
            ("message", "Aparna AI", "Please connect a working microphone.")
        )

    finally:
        message_queue.put(
            ("status", "Assistant stopped")
        )


# -------------------- START AND STOP --------------------

def start_assistant():

    global assistant_thread, is_listening

    if assistant_thread and assistant_thread.is_alive():
        return

    stop_event.clear()
    is_listening = True

    status_label.configure(
        text="Starting assistant...",
        text_color=GREEN
    )

    start_button.configure(
        state="disabled",
        text="Assistant Running"
    )

    stop_button.configure(
        state="normal"
    )

    assistant_thread = threading.Thread(
        target=assistant_worker,
        daemon=True
    )

    assistant_thread.start()

    animate_microphone()


def stop_assistant():

    global is_listening

    stop_event.set()
    is_listening = False

    status_label.configure(
        text="Stopping assistant...",
        text_color=RED
    )

    start_button.configure(
        state="normal",
        text="Start Assistant"
    )

    stop_button.configure(
        state="disabled"
    )

    mic_button.configure(
        fg_color=BLUE,
        text="🎙"
    )


# -------------------- MICROPHONE ANIMATION --------------------

def animate_microphone():

    global animation_step

    if not is_listening or stop_event.is_set():
        return

    animation_step += 1

    colors = [
        BLUE,
        "#1D4ED8",
        "#2563EB",
        "#0EA5E9",
        "#0284C7"
    ]

    current_color = colors[
        animation_step % len(colors)
    ]

    mic_button.configure(
        fg_color=current_color,
        text="🎙"
    )

    app.after(
        350,
        animate_microphone
    )


# -------------------- VOICE SELECTION --------------------

def change_voice(selected_voice):

    if selected_voice not in voice_map:
        return

    try:
        with tts_lock:
            engine.setProperty(
                "voice",
                voice_map[selected_voice]
            )

        status_label.configure(
            text="Voice changed successfully",
            text_color=GREEN
        )

    except Exception as error:
        print("Voice selection error:", error)


# -------------------- GUI QUEUE UPDATER --------------------

def update_gui():

    try:
        while True:

            item = message_queue.get_nowait()
            event_type = item[0]

            if event_type == "message":

                sender = item[1]
                message = item[2]

                add_message(sender, message)

            elif event_type == "status":

                status = item[1]

                status_label.configure(
                    text=status
                )

                if status == "Assistant stopped":

                    global is_listening
                    is_listening = False

                    status_label.configure(
                        text_color=RED
                    )

                    start_button.configure(
                        state="normal",
                        text="Start Assistant"
                    )

                    stop_button.configure(
                        state="disabled"
                    )

                    mic_button.configure(
                        fg_color=BLUE
                    )

                elif status == "Listening...":
                    status_label.configure(
                        text_color=GREEN
                    )

                elif status == "Processing...":
                    status_label.configure(
                        text_color=CYAN
                    )

    except queue.Empty:
        pass

    if app.winfo_exists():
        app.after(100, update_gui)


# -------------------- MAIN GUI --------------------

main_frame = ctk.CTkFrame(
    app,
    fg_color=BG,
    corner_radius=0
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

# Header
header = ctk.CTkFrame(
    main_frame,
    fg_color=CARD,
    corner_radius=18,
    height=90
)

header.pack(
    fill="x",
    pady=(0, 15)
)

header.pack_propagate(False)

header_title = ctk.CTkLabel(
    header,
    text="✦ APARNA AI",
    font=("Arial", 27, "bold"),
    text_color=CYAN
)

header_title.pack(
    side="left",
    padx=25,
    pady=20
)

header_subtitle = ctk.CTkLabel(
    header,
    text="YOUR PERSONAL VOICE ASSISTANT",
    font=("Arial", 11, "bold"),
    text_color=MUTED
)

header_subtitle.pack(
    side="right",
    padx=25
)

# Main content
content_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)

content_frame.pack(
    fill="both",
    expand=True
)

# Left panel
left_panel = ctk.CTkFrame(
    content_frame,
    fg_color=CARD,
    corner_radius=18,
    width=280
)

left_panel.pack(
    side="left",
    fill="y",
    padx=(0, 15)
)

left_panel.pack_propagate(False)

# Assistant icon
assistant_icon = ctk.CTkLabel(
    left_panel,
    text="🤖",
    font=("Arial", 48)
)

assistant_icon.pack(pady=(12, 2))

assistant_name = ctk.CTkLabel(
    left_panel,
    text="Aparna AI",
    font=("Arial", 21, "bold"),
    text_color=WHITE
)

assistant_name.pack(pady=2)

assistant_description = ctk.CTkLabel(
    left_panel,
    text="Smart Voice Assistant",
    font=("Arial", 12),
    text_color=MUTED
)

assistant_description.pack(pady=(0, 8))

# Microphone button
mic_button = ctk.CTkButton(
    left_panel,
    text="🎙",
    width=100,
    height=100,
    corner_radius=100,
    font=("Arial", 38),
    fg_color=BLUE,
    hover_color=CYAN,
    command=start_assistant
)

mic_button.pack(pady=8)

# Status
status_label = ctk.CTkLabel(
    left_panel,
    text="Assistant is ready",
    font=("Arial", 12, "bold"),
    text_color=GREEN
)

status_label.pack(pady=5)

# Start button
start_button = ctk.CTkButton(
    left_panel,
    text="Start Assistant",
    width=200,
    height=36,
    corner_radius=10,
    fg_color=BLUE,
    hover_color="#1D4ED8",
    font=("Arial", 12, "bold"),
    command=start_assistant
)

start_button.pack(pady=5)

# Stop button
stop_button = ctk.CTkButton(
    left_panel,
    text="Stop Assistant",
    width=200,
    height=36,
    corner_radius=10,
    fg_color="#991B1B",
    hover_color=RED,
    font=("Arial", 12, "bold"),
    command=stop_assistant,
    state="disabled"
)

stop_button.pack(pady=5)

# Voice selection
voice_label = ctk.CTkLabel(
    left_panel,
    text="Select Assistant Voice",
    font=("Arial", 12, "bold"),
    text_color=WHITE
)

voice_label.pack(pady=(12, 5))

voice_dropdown = ctk.CTkOptionMenu(
    left_panel,
    values=voice_options,
    width=200,
    fg_color="#26364F",
    button_color=BLUE,
    button_hover_color="#1D4ED8",
    dropdown_fg_color=CARD,
    command=change_voice
)

voice_dropdown.pack(pady=5)

# Clear conversation
clear_button = ctk.CTkButton(
    left_panel,
    text="Clear Conversation",
    width=200,
    height=32,
    fg_color="#334155",
    hover_color="#475569",
    command=clear_chat
)

clear_button.pack(pady=(8, 15))

# Right panel
right_panel = ctk.CTkFrame(
    content_frame,
    fg_color=CARD,
    corner_radius=18
)

right_panel.pack(
    side="right",
    fill="both",
    expand=True
)

# Chat heading
chat_heading = ctk.CTkLabel(
    right_panel,
    text="Conversation",
    font=("Arial", 21, "bold"),
    text_color=WHITE
)

chat_heading.pack(
    anchor="w",
    padx=20,
    pady=(20, 5)
)

chat_subheading = ctk.CTkLabel(
    right_panel,
    text="Talk to Aparna AI using your microphone",
    font=("Arial", 12),
    text_color=MUTED
)

chat_subheading.pack(
    anchor="w",
    padx=20,
    pady=(0, 10)
)

# Chat area
chat_frame = ctk.CTkScrollableFrame(
    right_panel,
    fg_color="#0F172A",
    corner_radius=12
)

chat_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(5, 15)
)

# Welcome message
add_message(
    "Aparna AI",
    "Hello! I am Aparna AI. Click Start Assistant or the microphone to begin."
)

# Footer
footer = ctk.CTkLabel(
    main_frame,
    text="Developed with Python | Speech Recognition | CustomTkinter",
    font=("Arial", 11),
    text_color=MUTED
)

footer.pack(pady=(12, 0))


# -------------------- APPLICATION ICON --------------------

try:

    icon_image = Image.new(
        "RGBA",
        (256, 256),
        "#0B1220"
    )

    draw = ImageDraw.Draw(icon_image)

    draw.ellipse(
        (20, 20, 236, 236),
        fill="#2563EB"
    )

    draw.ellipse(
        (70, 45, 186, 165),
        fill="#38BDF8"
    )

    draw.rounded_rectangle(
        (105, 130, 151, 205),
        radius=22,
        fill="white"
    )

    draw.arc(
        (80, 100, 176, 200),
        start=0,
        end=180,
        fill="white",
        width=10
    )

    draw.line(
        (128, 200, 128, 220),
        fill="white",
        width=10
    )

    draw.line(
        (105, 220, 151, 220),
        fill="white",
        width=10
    )

    icon_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "aparna_ai.ico"
    )

    icon_image.save(
        icon_path,
        format="ICO",
        sizes=[(256, 256), (64, 64), (32, 32)]
    )

    app.iconbitmap(icon_path)

except Exception as error:
    print("Application icon could not be created:", error)


# -------------------- CLOSE APPLICATION --------------------

def close_application():

    stop_event.set()

    try:
        app.destroy()
    except Exception:
        pass


app.protocol(
    "WM_DELETE_WINDOW",
    close_application
)

# Start queue updater
app.after(
    100,
    update_gui
)

# Run application
app.mainloop()
