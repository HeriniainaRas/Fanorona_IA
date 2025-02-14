import random
import csv

def generate_winning_positions():
    """Génère 500 positions gagnantes où un joueur aligne trois pièces."""
    winning_positions = []
    for _ in range(500):
        board = [[0] * 3 for _ in range(3)]  # Initialiser un plateau vide
        player = random.choice([1, -1])  # Sélectionner un joueur gagnant
        row_or_col = random.choice(['row', 'col', 'diag'])
        index = random.randint(0, 2)
        
        if row_or_col == 'row':
            for j in range(3):
                board[index][j] = player
        elif row_or_col == 'col':
            for i in range(3):
                board[i][index] = player
        else:  # diagonales
            if index == 0:
                for i in range(3):
                    board[i][i] = player
            else:
                for i in range(3):
                    board[i][2 - i] = player
        
        winning_positions.append(board)
    return winning_positions

def generate_losing_positions():
    """Génère 500 positions perdantes où un joueur va perdre au prochain coup."""
    losing_positions = []
    for _ in range(500):
        board = [[0] * 3 for _ in range(3)]
        player = random.choice([1, -1])
        row_or_col = random.choice(['row', 'col', 'diag'])
        index = random.randint(0, 2)
        
        if row_or_col == 'row':
            for j in range(2):
                board[index][j] = -player
        elif row_or_col == 'col':
            for i in range(2):
                board[i][index] = -player
        else:
            if index == 0:
                for i in range(2):
                    board[i][i] = -player
            else:
                for i in range(2):
                    board[i][2 - i] = -player
        
        losing_positions.append(board)
    return losing_positions

# Génération des datasets
winners = generate_winning_positions()
losers = generate_losing_positions()

# Sauvegarde en CSV
with open("fanorona_dataset.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Type", "Board"])
    for board in winners:
        writer.writerow(["1", board])
    for board in losers:
        writer.writerow(["0", board])

print("Dataset généré et sauvegardé en CSV.")

