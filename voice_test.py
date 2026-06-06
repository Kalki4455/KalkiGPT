import speech_recognition as sr
import pyttsx3

# Text to Speech Engine
engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

# Select first available voice
voices = engine.getProperty("voices")
if len(voices) > 0:
    engine.setProperty("voice", voices[0].id)

recognizer = sr.Recognizer()

try:
    with sr.Microphone() as source:

        print("🎤 Speak now...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=10
        )

        print("⏳ Processing...")

    text = recognizer.recognize_google(audio)

    print(f"✅ You said: {text}")

    response = f"You said {text}"

    print(f"🤖 {response}")

    engine.say(response)
    engine.runAndWait()

except sr.WaitTimeoutError:
    print("⌛ No speech detected")

except sr.UnknownValueError:
    print("❌ Could not understand audio")

except sr.RequestError as e:
    print(f"❌ Speech Recognition Error: {e}")

except Exception as e:
    print(f"❌ Error: {e}")