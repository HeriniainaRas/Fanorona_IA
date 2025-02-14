class Node:
    def __init__(self, x_board=0, o_board=0, player='X'):
        self.x_board = x_board  # bitboard pour les pièces X
        self.o_board = o_board  # bitboard pour les pièces O
        self.player = player    # joueur actuel ('X' ou 'O')
        self.nodes_explored = 0  # Compteur pour les nœuds explorés

    def get_empty_squares(self):
        occupied = self.x_board | self.o_board
        return (~occupied) & 0x1FF  # 0x1FF = 111111111 en binaire (9 bits)

    def make_move(self, position):
        move_bit = 1 << position
        if self.player == 'X':
            self.x_board |= move_bit
        else:
            self.o_board |= move_bit

    def move_piece(self, start_pos, end_pos):
        start_bit = 1 << start_pos
        end_bit = 1 << end_pos
        
        if self.player == 'X':
            self.x_board &= ~start_bit  # Retire la pièce de la position initiale
            self.x_board |= end_bit     # Place la pièce à la position finale
        else:
            self.o_board &= ~start_bit
            self.o_board |= end_bit

    def is_winner(self):
        winning_patterns = [
            0b111000000,  # première ligne
            0b000111000,  # deuxième ligne
            0b000000111,  # troisième ligne
            0b100100100,  # première colonne
            0b010010010,  # deuxième colonne
            0b001001001,  # troisième colonne
            0b100010001,  # diagonale principale
            0b001010100   # diagonale secondaire
        ]

        board = self.x_board if self.player == 'X' else self.o_board
        return any(pattern & board == pattern for pattern in winning_patterns)

    def get_empty_positions(self):
        empty = self.get_empty_squares()
        return [i for i in range(9) if empty & (1 << i)]

    def _get_valid_piece_movements(self):
        moves = []
        current_board = self.x_board if self.player == 'X' else self.o_board
        empty = self.get_empty_squares()

        # Définition des mouvements valides le long des lignes visibles
        valid_connections = {
            0: [1, 3, 4],     # Coin supérieur gauche
            1: [0, 2, 4],     # Milieu haut
            2: [1, 4, 5],     # Coin supérieur droit
            3: [0, 4, 6],     # Milieu gauche
            4: [0, 1, 2, 3, 5, 6, 7, 8],  # Centre - connecté à toutes les positions par les lignes
            5: [2, 4, 8],     # Milieu droit
            6: [3, 4, 7],     # Coin inférieur gauche
            7: [4, 6, 8],     # Milieu bas
            8: [4, 5, 7]      # Coin inférieur droit
        }

        for start in range(9):
            if current_board & (1 << start):
                for end in valid_connections[start]:
                    if empty & (1 << end):
                        moves.append((start, end))

        return moves

    def minimax(self, depth, maximizing_player):
        self.nodes_explored += 1
        if depth == 0 or self.is_winner():
            return self.evaluate()

        # Phase de placement ou de déplacement
        is_placement_phase = bin(self.x_board | self.o_board).count('1') < 6
        moves = self.get_empty_positions() if is_placement_phase else self._get_valid_piece_movements()

        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_node = self.make_move_copy(move)
                eval = new_node.minimax(depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                new_node = self.make_move_copy(move)
                eval = new_node.minimax(depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def alphabeta(self, depth, alpha, beta, maximizing_player):
        self.nodes_explored += 1

        # Condition de terminaison
        if depth == 0 or self.is_winner():
            return self.evaluate()

        # Phase de placement ou de déplacement
        is_placement_phase = bin(self.x_board | self.o_board).count('1') < 6

        if maximizing_player:
            max_eval = float('-inf')
            moves = self.get_empty_positions() if is_placement_phase else self._get_valid_piece_movements()
            
            for move in moves:
                new_node = self.make_move_copy(move)
                eval = new_node.alphabeta(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            moves = self.get_empty_positions() if is_placement_phase else self._get_valid_piece_movements()
            
            for move in moves:
                new_node = self.make_move_copy(move)
                eval = new_node.alphabeta(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def make_move_copy(self, move):
        new_node = Node(self.x_board, self.o_board, self.player)
        if isinstance(move, tuple):
            start_pos, end_pos = move
            new_node.move_piece(start_pos, end_pos)
        else:
            new_node.make_move(move)
        new_node.player = 'O' if self.player == 'X' else 'X'
        return new_node

    def evaluate(self):
        if self.is_winner():
            return 1000 if self.player == 'O' else -1000

        # Évaluation des positions
        x_score = self._evaluate_alignments(self.x_board)
        o_score = self._evaluate_alignments(self.o_board)
        
        # L'IA joue avec O, donc on retourne la différence dans sa perspective
        return o_score - x_score

    def _evaluate_alignments(self, board):
        score = 0
        winning_patterns = [
            0b111000000, 0b000111000, 0b000000111,  # lignes
            0b100100100, 0b010010010, 0b001001001,  # colonnes
            0b100010001, 0b001010100                # diagonales
        ]
        
        empty = self.get_empty_squares()
        
        for pattern in winning_patterns:
            bits = bin(board & pattern).count('1')
            empty_in_pattern = bin(empty & pattern).count('1')
            
            if bits == 2 and empty_in_pattern == 1:
                score += 100  # Deux pièces alignées avec possibilité de gagner
            elif bits == 1 and empty_in_pattern == 2:
                score += 10   # Une pièce avec potentiel d'alignement
        
        # Bonus pour le contrôle du centre
        if board & (1 << 4):
            score += 15
            
        return score