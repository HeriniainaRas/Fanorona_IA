import csv
import numpy as np
import ast

def load_and_clean_dataset(input_csv, output_csv):
    """Charge, nettoie et enregistre un dataset sans doublons."""
    data_set = set()
    
    with open(input_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Ignorer l'en-tête
        for row in reader:
            label = int(row[0])
            board = ast.literal_eval(row[1])
            # Convertir les tableaux numpy en listes normales
            board = [list(map(int, sublist)) for sublist in board]
            # Ajouter un tuple immuable pour éviter les doublons
            data_set.add((label, str(board)))
    
    # Sauvegarder le dataset nettoyé
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Label", "Board"])
        for label, board in data_set:
            writer.writerow([label, board])

# Utilisation
dataset_path = "fanorona_dataset.csv"
cleaned_dataset_path = "fanorona_cleaned_dataset.csv"
load_and_clean_dataset(dataset_path, cleaned_dataset_path)
