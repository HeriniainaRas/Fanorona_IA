import itertools
import json
import csv

# Fonction qui vérifie si un joueur gagne
def check_win(board, player):
    # Vérification des lignes, colonnes et diagonales
    for i in range(3):
        # Lignes
        if all([board[i][j] == player for j in range(3)]):
            return True
        # Colonnes
        if all([board[j][i] == player for j in range(3)]):
            return True
    # Diagonales
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Fonction pour générer toutes les configurations possibles
def generate_boards():
    configurations = []
    seen_configurations = set()  # Pour suivre les configurations déjà rencontrées
    # Génération de toutes les configurations possibles (3^9)
    for configuration in itertools.product([0, 1], repeat=9):
        board = [list(configuration[i:i+3]) for i in range(0, 9, 3)]
        
        # Vérifier si joueur 1 gagne et si joueur 0 perd
        if check_win(board, 1) and not check_win(board, 0):
            board_json = json.dumps(board)
            if board_json not in seen_configurations:
                configurations.append((1, board_json))
                seen_configurations.add(board_json)
        # Vérifier si joueur 0 gagne et si joueur 1 perd
        elif check_win(board, 0) and not check_win(board, 1):
            board_json = json.dumps(board)
            if board_json not in seen_configurations:
                configurations.append((0, board_json))
                seen_configurations.add(board_json)

    return configurations

# Fonction pour enregistrer les données dans un fichier CSV
def save_to_csv(filename, boards):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Joueur", "Configuration"])
        for board in boards:
            writer.writerow([board[0], board[1]])

# Générer les configurations gagnantes et perdantes possibles
boards = generate_boards()

# Sauvegarder les données dans un fichier CSV
save_to_csv('dataset_cleaned.csv', boards)

