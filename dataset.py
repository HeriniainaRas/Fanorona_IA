import random
import csv
import json
import numpy as np

def generate_winning_positions():
    """Génère des positions où un joueur aligne trois pièces (victoire)."""
    positions = set()  # Utilisation d'un set pour éviter les doublons
    while len(positions) < 500:
        board = [[0] * 3 for _ in range(3)]
        player = random.choice([1, -1])
        row_or_col = random.choice(['row', 'col', 'diag'])
        index = random.randint(0, 2)

        if row_or_col == 'row':
            for j in range(3):
                board[index][j] = player
        elif row_or_col == 'col':
            for i in range(3):
                board[i][index] = player
        else:  
            if index == 0:
                for i in range(3):
                    board[i][i] = player
            else:
                for i in range(3):
                    board[i][2 - i] = player

        positions.add(json.dumps(board))  # Convertir en JSON pour éviter les duplicatas

    return [json.loads(pos) for pos in positions]


def generate_losing_positions():
    """Génère des positions où un joueur va perdre au prochain tour."""
    positions = set()
    while len(positions) < 500:
        board = [[0] * 3 for _ in range(3)]
        player = random.choice([1, -1])
        row_or_col = random.choice(['row', 'col', 'diag'])
        index = random.randint(0, 2)

        if row_or_col == 'row':
            for j in range(2):
                board[index][j] = player
        elif row_or_col == 'col':
            for i in range(2):
                board[i][index] = player
        else:
            if index == 0:
                for i in range(2):
                    board[i][i] = player
            else:
                for i in range(2):
                    board[i][2 - i] = player

        positions.add(json.dumps(board))

    return [json.loads(pos) for pos in positions]


def generate_neutral_positions():
    """Génère des positions où aucun joueur ne gagne immédiatement."""
    positions = set()
    while len(positions) < 500:
        board = [[random.choice([0, 1, -1]) for _ in range(3)] for _ in range(3)]
        # Vérifier qu'aucun joueur n'a gagné
        if not any(
            all(board[i][j] == board[i][0] and board[i][j] != 0 for j in range(3)) or
            all(board[j][i] == board[0][i] and board[j][i] != 0 for j in range(3)) or
            all(board[j][j] == board[0][0] and board[j][j] != 0 for j in range(3)) or
            all(board[j][2 - j] == board[0][2] and board[j][2 - j] != 0 for j in range(3))
            for i in range(3)
        ):
            positions.add(json.dumps(board))

    return [json.loads(pos) for pos in positions]


# Générer les jeux de données
winners = generate_winning_positions()
losers = generate_losing_positions()
neutrals = generate_neutral_positions()

# Supprimer les doublons globaux
all_positions = list(set(map(json.dumps, winners + losers + neutrals)))  # Suppression des doublons
random.shuffle(all_positions)  # Mélange aléatoire

# Sauvegarde en CSV
file_path = "fanorona_dataset.csv"
with open(file_path, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Type", "Board"])
    for pos in all_positions:
        board = json.loads(pos)
        if board in winners:
            writer.writerow(["1", pos])
        elif board in losers:
            writer.writerow(["0", pos])
        else:
            writer.writerow(["2", pos])  # Label 2 = position neutre

print(f"Dataset final généré ({len(all_positions)} positions uniques).")

