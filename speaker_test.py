import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Speak...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)

    response = f"You said {text}"

    print(response)

    engine.say(response)
    engine.runAndWait()

except Exception as e:
    print("Error:", e)