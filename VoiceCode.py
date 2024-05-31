#!/usr/bin/env python3

import pygame
import speech_recognition as sr
import time

no_comm = False

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
all_commands = ["   "]
paused = False  # Variable pour vérifier si la saisie est en pause
paused_string = ""  # Chaîne de caractères tapés pendant la pause
includes = ["#include <stdio.h>\n#include <unistd.h>\n"]

def draw_text(text: str, command_text):
    global includes
    include_text = ""
    for str in includes:
        include_text += str

    screen.fill(background_color)
    y = 10

    command_surface = font.render(command_text, True, text_color)
    screen.blit(command_surface, (10, y))
    y += 30

    # Dessiner une ligne noire
    pygame.draw.line(screen, line_color, (10, y), (790, y), 2)
    y += 10
    for line in include_text.split('\n'):
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (10, y))
        y += 30
    for line in text.split('\n'):
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (10, y))
        y += 30
    pygame.display.flip()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Ajuster le bruit ambiant
        try:
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
            command = recognizer.recognize_google(audio, language='fr-FR')
            print(f"Vous avez dit: {command}")
            return command.lower().split(), command  # Retourner la commande en mots et en texte
        except sr.WaitTimeoutError:
            print("Temps d'attente dépassé, aucune commande détectée")
            return [], "- Vous pouvez dicter..."
        except sr.UnknownValueError:
            print("Je n'ai pas compris ce que vous avez dit")
            return [], "- Je n'ai pas compris ce que vous avez dit"
        except sr.RequestError:
            print("Erreur de service")
            return [], "/!\\ Erreur de service"

def generate_c_code(commands):
    c_code = ""
    tab = 1
    global last_command_text
    global no_comm
    i = 0
    while i < len(commands):
        if "Guy" in commands[i] and commands[i + 1]:
            if "ouvert" in commands[i+1]:
                c_code += '\"'
                no_comm = True
            if "fermé" in commands[i+1]:
                c_code += '\"'
                no_comm = False
            i += 1
            if (i >= len(commands)):
                break
        if no_comm:
            c_code += f'{commands[i]}'
            if i < len(commands) - 1:
                c_code += " "
        elif "parenthèse" in commands[i] and i+1 < len(commands):
            if "ouvert" in commands[i+1]:
                c_code += '('
            if "fermé" in commands[i+1]:
                c_code += ')'
            i += 1
            if (i >= len(commands)):
                break
        elif "entier" in commands[i]:
            c_code += "int "
        elif "décimal" in commands[i]:
            c_code += "float "
        elif "booléen" in commands[i]:
            c_code += "bool "
        elif "étoile" in commands[i]:
            c_code += "*"
        elif "espace" in commands[i]:
            c_code += " "
        elif ("égal" or "=") in commands[i]:
            if i+1 < len(commands) and ("égal" or "=") in commands[i + 1]:
                c_code += "== "
                i += 1
            else:
                c_code += "= "
        elif "supérieur" in commands[i]:
            if i+1 < len(commands) and ("égal" or "=") in commands[i + 1]:
                c_code += ">= "
                i += 1
            else:
                c_code += "> "
        elif "inférieur" in commands[i]:
            if i+1 < len(commands) and ("égal" or "=") in commands[i + 1]:
                c_code += "<= "
                i += 1
            else:
                c_code += "< "
        elif "différent" in commands[i]:
            c_code += "!= "
        elif "retour" in commands[i]:
            c_code += ";\n"
            if tab > 0 and i+1 < len(commands) and ("ferme" or "fermé") in commands[i + 1]:
                tab -= 1
                c_code += (" " * (tab) * 4) + "}\n" + (" " * tab * 4)
                i += 1
            else:
                c_code += (" " * tab * 4)
            if (i >= len(commands)):
                break
        elif "condition" in commands[i]:
            c_code += "if ("
        elif "boucle" in commands[i]:
            c_code += "while ("
        elif "ouvre" in commands[i]:
            c_code += " {\n"
            tab += 1
            c_code += (" " * tab * 4)
        elif ("ferme" or "fermé") in commands[i]:
            c_code += "}\n" + (" " * tab * 4)
            tab -= 1
        else:
            c_code += f'{commands[i]}'
            if i < len(commands) - 1 and commands[i + 1] != "retour":
                c_code += " "
        i += 1
    return c_code

def add_includes():
    global includes
    global paused_string
    global paused
    include_name = ""
    while True:
        draw_text("#include <" + include_name + "_.h>", last_command_text)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                if key_name == 'escape':
                    paused = False
                    return
                elif key_name == 'return':
                    paused = False
                    includes.append("#include <" + include_name + ".h>" + "\n")
                    paused_string = ""
                    return
                elif key_name == 'backspace':
                    include_name = include_name[:-1]
                elif key_name.isprintable() and len(key_name) == 1:
                    include_name += key_name

if __name__ == "__main__":
    c_code = ""
    running = True
    last_command_text = "Chargement..."
    while True and running:
        draw_text("\nint main()\n{\n" + c_code + "    return 0;\n}\n", last_command_text)
        if not paused:
            words, last_command_text = listen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(all_commands) > 0:
                    all_commands.pop(-1)
                    c_code = generate_c_code(all_commands)
                elif event.key == pygame.K_TAB:
                    paused = not paused  # Toggle pause state
                    if not paused:  # If resuming, add the paused string to commands
                        all_commands.append(paused_string)
                        c_code = generate_c_code(all_commands)
                        paused_string = ""
                elif event.key == pygame.K_i and not paused:
                    paused = True
                    add_includes()
                else:
                    key_name = pygame.key.name(event.key)
                    if key_name == 'space':
                        key_name = ' '
                    if key_name == 'return':
                        key_name = '\n'
                    if (key_name == 'escape'):
                        running = False
                    if (key_name.isprintable() and len(key_name) == 1) or key_name == '\n':
                        if paused:
                            paused_string += key_name
                        else:
                            all_commands.append(key_name)
                            c_code = generate_c_code(all_commands)
        if not words or not running:
            continue  # Ignorer les phrases vides
        for i in words:
            if i == "efface" and len(all_commands) > 0:
                all_commands.pop(-1)
                break
        else:
            all_commands.extend(words)  # Ajouter les mots à la liste complète des commandes
        if "stop" in words or "stoppe" in words:
            break

        c_code = generate_c_code(all_commands)
    draw_text("\nint main()\n{\n" + c_code + "return 0;\n}\n", last_command_text)
    print(all_commands)
    with open("generated_code.c", "w") as file:
        for str in includes:
            file.write(str)
        file.write("\nint main()\n{\n")
        file.write(c_code)
        file.write("return 0;\n}\n")
    print("Code C généré avec succès")

    # Garder la fenêtre Pygame ouverte après avoir terminé l'écoute
    while running:
        time.sleep(0.4)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
