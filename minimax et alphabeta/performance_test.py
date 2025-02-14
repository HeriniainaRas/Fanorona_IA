import time
from Node import Node
import random

def test_performance(depth=4, num_tests=10):
    # Ajout de listes pour stocker les résultats individuels
    minimax_times = []
    alphabeta_times = []
    minimax_nodes = []
    alphabeta_nodes = []
    
    total_time_minimax = 0
    total_nodes_minimax = 0
    total_time_alphabeta = 0
    total_nodes_alphabeta = 0

    for i in range(num_tests):
        # Créer une position aléatoire
        x_board = random.randint(0, 0x1FF)
        o_board = random.randint(0, 0x1FF) & (~x_board)  # Éviter les chevauchements
        
        # Test Minimax
        node_minimax = Node(x_board, o_board)
        node_minimax.nodes_explored = 0
        start_time = time.time()
        node_minimax.minimax(depth, True)
        end_time = time.time()
        total_time_minimax += (end_time - start_time)
        total_nodes_minimax += node_minimax.nodes_explored
        
        # Stockage des résultats individuels
        minimax_times.append(end_time - start_time)
        minimax_nodes.append(node_minimax.nodes_explored)

        # Test Alpha-Beta
        node_alphabeta = Node(x_board, o_board)
        node_alphabeta.nodes_explored = 0
        start_time = time.time()
        node_alphabeta.alphabeta(depth, float('-inf'), float('inf'), True)
        end_time = time.time()
        total_time_alphabeta += (end_time - start_time)
        total_nodes_alphabeta += node_alphabeta.nodes_explored

    print(f"Résultats pour {num_tests} tests à profondeur {depth}:")
    print("\nMinimax:")
    print(f"Temps moyen: {total_time_minimax/num_tests:.4f} secondes")
    print(f"Nœuds explorés en moyenne: {total_nodes_minimax/num_tests:.0f}")
    
    print("\nAlpha-Beta:")
    print(f"Temps moyen: {total_time_alphabeta/num_tests:.4f} secondes")
    print(f"Nœuds explorés en moyenne: {total_nodes_alphabeta/num_tests:.0f}")
    
    print("\nGains de performance:")
    if total_time_minimax > 0:
        print(f"Réduction du temps: {((total_time_minimax - total_time_alphabeta)/total_time_minimax)*100:.1f}%")
    else:
        print("Réduction du temps: N/A (temps minimax = 0)")
        
    if total_nodes_minimax > 0:
        print(f"Réduction des nœuds explorés: {((total_nodes_minimax - total_nodes_alphabeta)/total_nodes_minimax)*100:.1f}%")
    else:
        print("Réduction des nœuds explorés: N/A (nœuds minimax = 0)")

if __name__ == "__main__":
    test_performance(depth=4, num_tests=10) 