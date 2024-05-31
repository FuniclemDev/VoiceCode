# VoiceCode

VoiceCode est un programme qui vous permet de générer du code en langage C à partir de commandes vocales. Il utilise la reconnaissance vocale pour interpréter les commandes que vous prononcez et les traduit en code C.

## Fonctionnalités

- Génération de code C à partir de commandes vocales.
- Prise en charge de plusieurs types de données, opérateurs et structures de contrôle.
- Interface utilisateur simple utilisant la bibliothèque Pygame pour l'affichage.

## Prérequis

Avant d'exécuter VoiceCode, assurez-vous d'avoir les éléments suivants installés sur votre système :

- Python 3.x
- Pygame
- SpeechRecognition
- Une connexion Internet pour utiliser la reconnaissance vocale avec Google

## Installation

1. Clonez ce dépôt sur votre machine :

git clone https://github.com/FuniclemDev/VoiceCode.git

2. Installez les dépendances requises en exécutant la commande suivante :

./install_requirements.sh


## Utilisation

1. Lancez le programme en exécutant le fichier `VoiceCode.py` :

./VoiceCode.py


2. Parlez dans le microphone pour donner des commandes vocales. VoiceCode les traduira en code C et les affichera à l'écran.

3. Utilisez les touches du clavier pour ajouter des commandes supplémentaires ou modifier le code généré.

4. Pour arrêter le programme, prononcez "stop".

## Remarques

Il est possible que le programme ne détecte aucune entrée audio de votre microphone. C'est pour cela que vous avez à votre disposition ./debug.sh, cela peut résoudre le problème mais certaine fonctionnalités de votre pc peuvent disparaître jusqu'au prochain redémarrage. Je décline toute responsabilité en cas de dommage sur un pc exécutant les programmes présents dans le projet. 
