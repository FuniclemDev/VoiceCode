import os
import re

def extract_function_names(header_file):
    function_names = []
    try:
        with open(header_file, 'rb') as file:  # Ouvrir en mode binaire
            content = file.read().decode('utf-8', errors='ignore')  # Décoder avec gestion des erreurs
            lines = content.splitlines()
            for line in lines:
                # Recherche des lignes contenant des déclarations de fonctions
                match = re.match(r'^\s*(extern\s+)?[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)\s*;', line)
                if match:
                    # Extraction du nom de la fonction
                    function_signature = match.group(0)
                    function_name = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', function_signature)
                    if function_name:
                        function_names.append(function_name[0])
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {header_file}: {e}")
    return function_names

def find_all_functions_in_include():
    include_dirs = ['/usr/include', '/usr/local/include']  # Inclure les deux répertoires communs
    all_functions = []

    for include_dir in include_dirs:
        for root, dirs, files in os.walk(include_dir):
            for file in files:
                if file.endswith('.h'):
                    header_file = os.path.join(root, file)
                    functions = extract_function_names(header_file)
                    all_functions.extend(functions)

    return all_functions

if __name__ == "__main__":
    functions = find_all_functions_in_include()
    unique_functions = list(set(functions))  # Pour éviter les doublons
    unique_functions.sort()

    # Écriture des fonctions dans un fichier pour usage ultérieur
    with open('lib_functions.py', 'w') as file:
        file.write('lib_functions_types = [\n')
        for func in unique_functions:
            file.write(f'    "{func}",\n')
        file.write(']\n')

    print(f"Nombre total de fonctions trouvées: {len(unique_functions)}")
    print("Les fonctions ont été écrites dans libc_functions.py")
