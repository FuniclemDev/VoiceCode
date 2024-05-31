#!/usr/bin/env python3

import pygame
import speech_recognition as sr
from libc_fct import libc_functions  # Assurez-vous que libc_fct.py contient une liste de fonctions libc
from lib_functions import lib_functions_types  # Assurez-vous que libc_fct.py contient une liste de fonctions libc
import time

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Code Généré')
font = pygame.font.Font(None, 28)
background_color = (255, 255, 255)
text_color = (0, 0, 0)
screen.fill(background_color)
pygame.display.flip()

def draw_text(text):
    screen.fill(background_color)
    y = 10
    for line in text.split('\n'):
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (10, y))
        y += 30
    pygame.display.flip()

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
    for i in range(len(commands)):
        if "déclarer" in commands[i]:
            try:
                if commands[i + 1] in lib_functions_types and commands[i + 2]:
                    c_code += f'    {commands[i + 1]} {commands[i + 2]}'
            except:
                print('Déclaration incomplète ou non valide')
            i += 3
        if (i >= len(commands)):
            break
        elif commands[i] in libc_functions:
            c_code += f'{commands[i]}\n'
        elif commands[i] in lib_functions_types:
            c_code += f'{commands[i]}\n'
        elif "parenthèse" in commands[i] and commands[i + 1]:
            if commands[i + 1] == "ouverte":
                c_code += '('
            if commands[i + 1] == "fermée":
                c_code += ')'
            i += 1
        if (i >= len(commands)):
            break
        elif "espace" in commands[i]:
            c_code += " "
        if "égal" in commands[i]:
            c_code += " = "
        if "point" in commands[i]:
            c_code += ";\n"
        # Ajouter d'autres commandes ici
    return c_code

if __name__ == "__main__":
    all_commands = []
    c_code = ""
    running = True
    while True and running:
        draw_text("#include <stdio.h>\n#include <unistd.h>\n\nint main() {\n" + c_code + "    return 0;\n}\n")
        words = listen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not words:
            continue  # Ignorer les phrases vides
        all_commands.extend(words)  # Ajouter les mots à la liste complète des commandes
        if "stop" in words or "stoppe" in words:
            break

        c_code = generate_c_code(all_commands)

    print(all_commands)
    with open("generated_code.c", "w") as file:
        file.write("#include <stdio.h>\n\nint main() {\n")
        file.write(c_code)
        file.write("    return 0;\n}\n")
    print("Code C généré avec succès")

    # Garder la fenêtre Pygame ouverte après avoir terminé l'écoute
    while running:
        time.sleep(0.4)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
