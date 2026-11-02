import subprocess

text = "Hello Zulqarnain. I am Nova, your personal AI assistant."

subprocess.run(["espeak-ng", "-s", "170", text])