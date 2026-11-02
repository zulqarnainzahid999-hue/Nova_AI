import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Nova: I'm listening...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = recognizer.listen(source)

print("Nova: Processing...")

try:
    text = recognizer.recognize_google(audio)
    print("You:", text)

except sr.UnknownValueError:
    print("Nova: I couldn't understand you.")

except sr.RequestError as e:
    print("Nova: Speech service error:", e)