# Aparna AI – Voice Assistant

## Project Overview
Aparna AI is a Python-based voice assistant that listens to voice commands, processes them, and responds through speech. It provides a graphical user interface built using CustomTkinter.

## Features
- Voice recognition using SpeechRecognition.
- Text-to-speech responses using pyttsx3.
- Modern graphical interface using CustomTkinter.
- Animated microphone button.
- Separate chat bubbles for user and assistant.
- Voice selection option.
- Current date and time.
- Weather information.
- Google search.
- Wikipedia information.
- Open YouTube and Google.
- Launch Notepad and Calculator.
- Random jokes.
- Clear conversation option.

## Technologies Used
- Python
- CustomTkinter
- SpeechRecognition
- PyAudio
- pyttsx3
- PyWhatKit
- Wikipedia
- Requests
- PyJokes
- Pillow

## Project Structure

```text
Task4_VoiceAssistant/
│
├── gui.py
├── main.py
├── README.md
└── aparna_ai.ico
```

The application icon is generated automatically when the GUI starts.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Aparna639/INIB.git
```

2. Navigate to the project folder:

```bash
cd INIB/Task4_VoiceAssistant
```

3. Install the required packages:

```bash
pip install customtkinter SpeechRecognition PyAudio pyttsx3 pywhatkit wikipedia pyjokes requests pillow
```

## Run the Application

```bash
python gui.py
```

## How to Use
1. Start the application.
2. Select your preferred assistant voice.
3. Click Start Assistant.
4. Speak a command through your microphone.
5. Listen to the assistant's response.
6. Click Stop Assistant when finished.

## Example Voice Commands

| Voice Command | Action |
|---|---|
| Hello | Assistant greets you |
| What is the time? | Announces current time |
| What is the date? | Announces current date |
| Open YouTube | Opens YouTube |
| Open Google | Opens Google |
| Tell me a joke | Tells a joke |
| Who is Albert Einstein? | Provides Wikipedia information |
| Weather in Hyderabad | Provides weather information |
| Open Notepad | Opens Notepad |
| Open Calculator | Opens Calculator |
| Goodbye | Stops the assistant |

## Requirements
- Python installed on your computer.
- Working microphone.
- Internet connection for online speech recognition and web-based features.

## Internship Project
**Organization:** InfoByte  
**Project:** Task 4 – Voice Assistant  
**Developer:** Aparna

---

Developed using Python.
