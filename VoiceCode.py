#!/usr/bin/env python3

import pygame
import speech_recognition as sr
from libc_fct import libc_functions  # Assurez-vous que libc_fct.py contient une liste de fonctions libc
from lib_functions import lib_functions_types  # Assurez-vous que libc_fct.py contient une liste de fonctions libc
import time

tab = 1

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Code Généré')
font = pygame.font.Font(None, 28)
background_color = (255, 255, 255)
text_color = (0, 0, 0)
screen.fill(background_color)
pygame.display.flip()
line_color = (0, 0, 0)
last_command_text = ""  # Variable pour stocker la dernière commande reconnue

def draw_text(text, command_text):
    screen.fill(background_color)
    y = 10

    # Afficher la commande reconnue en haut de la fenêtre
    command_surface = font.render(command_text, True, text_color)
    screen.blit(command_surface, (10, y))
    y += 30  # Ajouter un espace après la commande

    # Dessiner une ligne noire
    pygame.draw.line(screen, line_color, (10, y), (790, y), 2)
    y += 10  # Ajouter un espace après la ligne
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
            return command.lower().split(), command  # Retourner la commande en mots et en texte
        except sr.UnknownValueError:
            print("Je n'ai pas compris ce que vous avez dit")
            return [], ""
        except sr.RequestError:
            print("Erreur de service")
            return [], ""

def generate_c_code(commands):
    c_code = ""
    global tab
    for i in range(len(commands)):
        if (i >= len(commands)):
            break
        if "déclarer" in commands[i]:
            try:
                if commands[i + 1] and commands[i + 2]:
                    c_code += f'    {commands[i + 1]} {commands[i + 2]}'
            except:
                print('Déclaration incomplète ou non valide')
            i += 3
            if (i >= len(commands)):
                break
        elif commands[i] in libc_functions:
            c_code += f'{commands[i]}'
        elif commands[i] in lib_functions_types:
            c_code += f'{commands[i]}'
        elif "parenthèse" in commands[i] and commands[i + 1]:
            if commands[i + 1] == "ouverte":
                c_code += '('
            if commands[i + 1] == "fermée":
                c_code += ')'
            i += 1
            if (i >= len(commands)):
                break
        elif "Guy" in commands[i] and commands[i + 1]:
            if commands[i + 1] == "ouvert":
                c_code += '\"'
            if commands[i + 1] == "fermé":
                c_code += '\"'
            i += 1
            if (i >= len(commands)):
                break
        elif "espace" in commands[i]:
            c_code += " "
        elif "égal" in commands[i]:
            if commands[i + 1] == "égal":
                c_code += " == "
                i += 1
            else:
                c_code += " = "
        elif "supérieur" in commands[i]:
            if commands[i + 1] == "égal":
                c_code += " >= "
                i += 1
            else:
                c_code += " > "
        elif "inférieur" in commands[i]:
            if commands[i + 1] == "égal":
                c_code += " <= "
                i += 1
            else:
                c_code += " < "
        elif "différent" == commands[i]:
            c_code += " != "
        elif "point" in commands[i]:
            c_code += ";\n"
            if tab > 0 and commands[i + 1] == "ferme":
                c_code += (" " * (tab - 1) * 4)
                i += 1
            else:
                c_code += (" " * tab * 4)
            if (i >= len(commands)):
                break
        elif "si" == commands[i]:
            c_code += "if ("
        elif "ouvre" == commands[i]:
            c_code += " {\n"
            tab += 1
        elif "ferme" == commands[i]:
            c_code += "}\n" + (" " * tab * 4)
        elif "efface" == commands[i]:
            while len(c_code) > 0 and c_code[-1] != "\n":
                c_code = c_code[:-1]
        else:
            c_code += f' {commands[i]} '
    return c_code

if __name__ == "__main__":
    all_commands = []
    c_code = ""
    running = True
    while True and running:
        draw_text("#include <stdio.h>\n#include <unistd.h>\n\nint main() {\n" + c_code + "    return 0;\n}\n", last_command_text)
        words, last_command_text = listen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not words:
            last_command_text = "Je n'ai pas compris, veillez répéter."
            continue  # Ignorer les phrases vides
        all_commands.extend(words)  # Ajouter les mots à la liste complète des commandes
        if "stop" in words or "stoppe" in words:
            break

        c_code = generate_c_code(all_commands)
    draw_text("#include <stdio.h>\n#include <unistd.h>\n\nint main() {\n" + c_code + "    return 0;\n}\n", last_command_text)
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
