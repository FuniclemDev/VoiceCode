#!/usr/bin/env python3

import pygame
import speech_recognition as sr
from libc_fct import libc_functions  # Assurez-vous que libc_fct.py contient une liste de fonctions libc

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
    for command in commands:
        if "déclarer" in command:
            c_code += "int variable;\n"
        elif "afficher" in command:
            c_code += 'printf("Message");\n'
        elif "coucou" in command:
            c_code += 'if (/* condition */) {\n    // next instruction\n}\n'
        elif command in libc_functions:
            c_code += f'{command}(/* arguments */);\n'
        # Ajouter d'autres commandes ici
    return c_code

if __name__ == "__main__":
    all_commands = []
    c_code = ""
    running = True
    while True and running:
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
        draw_text("#include <stdio.h>\n\nint main() {\n" + c_code + "    return 0;\n}\n")

    print(all_commands)
    with open("generated_code.c", "w") as file:
        file.write("#include <stdio.h>\n\nint main() {\n")
        file.write(c_code)
        file.write("    return 0;\n}\n")
    print("Code C généré avec succès")

    # Garder la fenêtre Pygame ouverte après avoir terminé l'écoute
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
