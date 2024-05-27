#!/usr/bin/env python3

import speech_recognition as sr
import pyttsx3
from libc_fct import libc_functions

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
            return command.lower().split()  # Séparer la phrase en mots
        except sr.UnknownValueError:
            print("Je n'ai pas compris ce que vous avez dit")
            return []
        except sr.RequestError:
            print("Erreur de service")
            return []

def generate_c_code(commands):
    c_code = ""
    for command in commands:
        if "déclarer" in command:
            c_code += "int variable;\n"
        elif "afficher" in command:
            c_code += 'printf("Message");\n'
        elif "coucou" in command:
            c_code += 'if (/* condition */) {\n    // next instruction\n}\n'
        # Ajouter d'autres commandes ici
    return c_code

if __name__ == "__main__":
    speak("OK")
    all_commands = []
    while True:
        words = listen()
        if not words:
            continue  # Ignorer les phrases vides
        all_commands.extend(words)  # Ajouter les mots à la liste complète des commandes
        if "stop" in words:
            break
    print(all_commands)
    c_code = generate_c_code(all_commands)
    print("--------")
    print(c_code)
    with open("generated_code.c", "w") as file:
        file.write("#include <stdio.h>\n\nint main() {\n")
        file.write(c_code)
        file.write("    return 0;\n}\n")
    print("Code C généré avec succès")
    speak("OK")
