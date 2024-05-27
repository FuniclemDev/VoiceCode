#!/usr/bin/env python3

import speech_recognition as sr
import pyttsx3

# Initialisation du moteur de synthèse vocale
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='fr-FR')
            print(f"Vous avez dit: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Je n'ai pas compris ce que vous avez dit")
            return ""
        except sr.RequestError:
            print("Erreur de service")
            return ""

def generate_c_code(commands):
    c_code = ""
    for command in commands:
        if "déclarer une variable entière" in command:
            c_code += "int variable;\n"
        elif "afficher un message" in command:
            c_code += 'printf("Message");\n'
        # Ajouter d'autres commandes ici
    return c_code

if __name__ == "__main__":
    speak("OK")
    commands = []
    while True:
        command = listen()
        if command == "stop" or command == "stoppe":
            break
        commands.append(command)

    c_code = generate_c_code(commands)
    with open("generated_code.c", "w") as file:
        file.write("#include <stdio.h>\n\nint main() {\n")
        file.write(c_code)
        file.write("    return 0;\n}\n")
    print("Code C généré avec succès")
    speak("OK")
