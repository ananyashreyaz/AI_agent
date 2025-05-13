

import pyttsx3


engine = pyttsx3.init()

engine.setProperty("rate", 170)  # Words per minute


voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  

def speak(text: str):
    """Speak the given text out loud."""
    print("🔊 Speaking:", text)
    engine.say(text)
    engine.runAndWait()
