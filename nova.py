import speech_recognition as sr
import requests
import subprocess
import sqlite3

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

recognizer = sr.Recognizer()


def speak(text):
    subprocess.run(["espeak-ng", "-s", "170", text])


conversation = []


def ask_nova(text):
    conversation.append(f"User: {text}")

    history = "\n".join(conversation)
    memories = get_memories()

    prompt = f"""
You are Nova, a personal AI voice assistant.
Your name is Nova.
Be helpful, natural, and concise.

Saved memories:
{memories}

Current conversation:
{history}

Nova:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    answer = response.json()["response"].strip()

    conversation.append(f"Nova: {answer}")

    return answer




db = sqlite3.connect("nova_memory.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    information TEXT
)
""")

db.commit()


def save_memory(text):
    cursor.execute(
        "INSERT INTO memories (information) VALUES (?)",
        (text,)
    )
    db.commit()


def get_memories():
    cursor.execute("SELECT information FROM memories")
    memories = cursor.fetchall()

    return "\n".join(memory[0] for memory in memories)





while True:

    with sr.Microphone(device_index=0) as source:
        print("\nNova: Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)

        if "nova" not in text.lower():
            continue

        command = text.lower().replace("nova", "", 1).strip()

        if not command:
            speak("Yes, how can I help?")
            continue

        if command in ["exit", "quit", "goodbye", "bye"]:
            speak("Goodbye.")
            break

        print("Nova: Thinking...")
        answer = ask_nova(command)

        print("Nova:", answer)
        speak(answer)

    except sr.UnknownValueError:
        print("Nova: I couldn't understand you.")

    except sr.RequestError as e:
        print("Speech recognition error:", e)

    except Exception as e:
        print("Nova error:", e)

        if text.lower() in ["exit", "quit", "goodbye", "bye nova"]:
            speak("Goodbye.")
            break

        print("Nova: Thinking...")

        answer = ask_nova(text)

        print("Nova:", answer)
        speak(answer)

    except sr.UnknownValueError:
        print("Nova: I couldn't understand you.")

    except sr.RequestError as e:
        print("Speech recognition error:", e)

    except Exception as e:
        print("Nova error:", e)