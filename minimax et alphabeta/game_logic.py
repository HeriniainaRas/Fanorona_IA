from Node import Node

class FanoronaTeloLogic:
    def __init__(self):
        self.node = Node()
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.selected_piece = None
        self.game_over = False
        self.placed_pieces = {'X': 0, 'O': 0}
        self.algorithm = 'alphabeta'  # Par défaut

    def set_algorithm(self, algo):
        self.algorithm = algo

    def place_piece(self, row, col):
        position = row * 3 + col
        
        if self.board[row][col] == ' ' and self.placed_pieces[self.current_player] < 3:
            self.node.make_move(position)
            self.board[row][col] = self.current_player
            self.placed_pieces[self.current_player] += 1
            return True
        return False

    def move_piece(self, start_row, start_col, end_row, end_col):
        if self.board[end_row][end_col] != ' ':
            return False

        if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
            return False

        start_pos = start_row * 3 + start_col
        end_pos = end_row * 3 + end_col

        self.node.move_piece(start_pos, end_pos)
        self.board[end_row][end_col] = self.current_player
        self.board[start_row][start_col] = ' '
        return True

    def check_win(self, row, col):
        return self.node.is_winner()

    def get_valid_moves(self, row, col):
        if self.placed_pieces['X'] + self.placed_pieces['O'] < 6:
            return self.node.get_empty_positions()
        else:
            start_pos = row * 3 + col
            valid_moves = self.node._get_valid_piece_movements()
            return [end for start, end in valid_moves if start == start_pos]

    def get_ai_move(self):
        total_pieces = self.placed_pieces['X'] + self.placed_pieces['O']
        
        if total_pieces < 6:  # Phase de placement
            possible_moves = self.get_valid_moves(0, 0)
            best_score = float('-inf')
            best_move = None
            
            if total_pieces == 0:
                return (1, 1)
            
            for pos in possible_moves:
                new_node = self.node.make_move_copy(pos)
                
                if new_node.is_winner():
                    return (pos // 3, pos % 3)
                
                # Utilisation de l'algorithme sélectionné
                if self.algorithm == 'minimax':
                    score = new_node.minimax(4, False)
                else:
                    score = new_node.alphabeta(4, float('-inf'), float('inf'), False)
                
                if pos == 4:
                    score += 30
                elif pos in [0, 2, 6, 8]:
                    score += 20
                
                if score > best_score:
                    best_score = score
                    best_move = pos
            
            if best_move is not None:
                return (best_move // 3, best_move % 3)
                
        else:  # Phase de déplacement
            valid_moves = self.node._get_valid_piece_movements()
            best_score = float('-inf')
            best_move = None
            
            for start_pos, end_pos in valid_moves:
                if self.board[start_pos // 3][start_pos % 3] != self.current_player:
                    continue
                
                new_node = self.node.make_move_copy((start_pos, end_pos))
                
                if new_node.is_winner():
                    return (start_pos // 3, start_pos % 3, end_pos // 3, end_pos % 3)
                
                # Utilisation de l'algorithme sélectionné
                if self.algorithm == 'minimax':
                    score = new_node.minimax(4, False)
                else:
                    score = new_node.alphabeta(4, float('-inf'), float('inf'), False)
                
                if score > best_score:
                    best_score = score
                    best_move = (start_pos, end_pos)
            
            if best_move:
                start_pos, end_pos = best_move
                return (start_pos // 3, start_pos % 3, end_pos // 3, end_pos % 3)
        
        return None

    def _creates_winning_opportunity(self, node, row, col):
        """Vérifie si un coup crée une opportunité de victoire"""
        # Vérifier les lignes
        row_count = sum(1 for c in range(3) if 
                       (node.x_board if node.player == 'X' else node.o_board) & (1 << (row * 3 + c)))
        if row_count == 2:
            return True
        
        # Vérifier les colonnes
        col_count = sum(1 for r in range(3) if 
                       (node.x_board if node.player == 'X' else node.o_board) & (1 << (r * 3 + col)))
        if col_count == 2:
            return True
        
        # Vérifier les diagonales
        if row == col or row + col == 2:  # Position sur une diagonale
            diag1 = sum(1 for i in range(3) if 
                       (node.x_board if node.player == 'X' else node.o_board) & (1 << (i * 3 + i)))
            diag2 = sum(1 for i in range(3) if 
                       (node.x_board if node.player == 'X' else node.o_board) & (1 << (i * 3 + (2 - i))))
            if diag1 == 2 or diag2 == 2:
                return True
        
        return False