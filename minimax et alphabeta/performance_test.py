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

    print(f"\nDébut des tests de performance ({num_tests} tests à profondeur {depth})...")
    print("=" * 60)

    for i in range(num_tests):
        print(f"\nTest {i+1}/{num_tests}")
        
        # Créer une position aléatoire plus réaliste
        x_board = random.randint(0, 0x1FF)
        o_board = random.randint(0, 0x1FF) & (~x_board)  # Éviter les chevauchements
        
        # Test Minimax
        print("Exécution de Minimax...", end=" ", flush=True)
        node_minimax = Node(x_board, o_board)
        node_minimax.nodes_explored = 0
        start_time = time.time()
        score_minimax = node_minimax.minimax(depth, True)
        end_time = time.time()
        time_minimax = end_time - start_time
        total_time_minimax += time_minimax
        total_nodes_minimax += node_minimax.nodes_explored
        minimax_times.append(time_minimax)
        minimax_nodes.append(node_minimax.nodes_explored)
        print(f"Terminé en {time_minimax:.3f}s ({node_minimax.nodes_explored} nœuds)")

        # Test Alpha-Beta
        print("Exécution d'Alpha-Beta...", end=" ", flush=True)
        node_alphabeta = Node(x_board, o_board)
        node_alphabeta.nodes_explored = 0
        start_time = time.time()
        score_alphabeta = node_alphabeta.alphabeta(depth, float('-inf'), float('inf'), True)
        end_time = time.time()
        time_alphabeta = end_time - start_time
        total_time_alphabeta += time_alphabeta
        total_nodes_alphabeta += node_alphabeta.nodes_explored
        alphabeta_times.append(time_alphabeta)
        alphabeta_nodes.append(node_alphabeta.nodes_explored)
        print(f"Terminé en {time_alphabeta:.3f}s ({node_alphabeta.nodes_explored} nœuds)")
        
        # Vérification de la cohérence des résultats
        if score_minimax != score_alphabeta:
            print(f"⚠️ Attention: Incohérence des scores - Minimax: {score_minimax}, Alpha-Beta: {score_alphabeta}")

    print(f"Resultats pour {num_tests} tests a profondeur {depth}:")
    print("\nMinimax:")
    print(f"Temps moyen: {total_time_minimax/num_tests:.4f} secondes")
    print(f"Noeuds explores en moyenne: {total_nodes_minimax/num_tests:.0f}")
    
    print("\nAlpha-Beta:")
    print(f"Temps moyen: {total_time_alphabeta/num_tests:.4f} secondes")
    print(f"Noeuds explores en moyenne: {total_nodes_alphabeta/num_tests:.0f}")
    
    print("\nGAINS DE PERFORMANCE")
    print("=" * 60)
    if total_time_minimax > 0:
        print(f"Reduction du temps: {((total_time_minimax - total_time_alphabeta)/total_time_minimax)*100:.1f}%")
    else:
        print("Reduction du temps: N/A (temps minimax = 0)")
        
    if total_nodes_minimax > 0:
        print(f"Reduction des noeuds explores: {((total_nodes_minimax - total_nodes_alphabeta)/total_nodes_minimax)*100:.1f}%")
    else:
        print("Reduction des noeuds explores: N/A (nœuds minimax = 0)")

if __name__ == "__main__":
    # Tests à différentes profondeurs
    for depth in [3, 4, 5]:
        test_performance(depth=depth, num_tests=5) 