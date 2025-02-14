import tkinter as tk
from tkinter import messagebox
from game_logic import FanoronaTeloLogic

class FanoronaTeloGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Fanorona Telo')
        self.algorithm = 'alphabeta'  # Par défaut
        
        # Création du frame pour les boutons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5)
        
        # Boutons pour choisir l'algorithme
        self.minimax_btn = tk.Button(self.button_frame, text="Minimax", command=lambda: self.set_algorithm('minimax'))
        self.minimax_btn.pack(side=tk.LEFT, padx=5)
        
        self.alphabeta_btn = tk.Button(self.button_frame, text="Alpha-Beta", command=lambda: self.set_algorithm('alphabeta'))
        self.alphabeta_btn.pack(side=tk.LEFT, padx=5)
        
        self.logic = FanoronaTeloLogic()
        self.is_ai_turn = False
        self.human_player = 'X'  # Ajout : le joueur humain est toujours X (blanc)
        self.ai_player = 'O'     # Ajout : l'IA est toujours O (noir)

        self.canvas = tk.Canvas(master, width=300, height=300)
        self.canvas.pack()

        self.draw_board()
        self.canvas.bind('<Button-1>', self.click)

    def set_algorithm(self, algo):
        self.algorithm = algo
        self.logic.set_algorithm(algo)
        # Mise à jour visuelle des boutons
        if algo == 'minimax':
            self.minimax_btn.config(relief=tk.SUNKEN)
            self.alphabeta_btn.config(relief=tk.RAISED)
        else:
            self.minimax_btn.config(relief=tk.RAISED)
            self.alphabeta_btn.config(relief=tk.SUNKEN)

    def draw_board(self):
        self.canvas.delete('all')
        for i in range(3):
            self.canvas.create_line(50, i * 100 + 50, 250, i * 100 + 50)
            self.canvas.create_line(i * 100 + 50, 50, i * 100 + 50, 250)
        self.canvas.create_line(50, 50, 250, 250)
        self.canvas.create_line(50, 250, 250, 50)
        for i in range(3):
            for j in range(3):
                if self.logic.board[i][j] != ' ':
                    self.draw_piece(i, j, self.logic.board[i][j])

    def draw_piece(self, row, col, player):
        x = col * 100 + 50
        y = row * 100 + 50
        radius = 20
        color = 'white' if player == 'X' else 'black'
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def click(self, event):
        if self.logic.game_over or self.is_ai_turn or self.logic.current_player != self.human_player:
            return

        col = round((event.x - 50) / 100)
        row = round((event.y - 50) / 100)
        
        if not (0 <= row < 3 and 0 <= col < 3):
            return

        total_pieces = self.logic.placed_pieces['X'] + self.logic.placed_pieces['O']
        
        if total_pieces < 6:
            if self.logic.place_piece(row, col):
                self.draw_board()
                if self.check_game_over():
                    return
                self.is_ai_turn = True
                self.master.after(500, self.ai_turn)
        else:
            if self.logic.selected_piece:
                start_row, start_col = self.logic.selected_piece
                if row == start_row and col == start_col:
                    self.logic.selected_piece = None
                    self.draw_board()
                    return
                
                if self.logic.move_piece(start_row, start_col, row, col):
                    self.logic.selected_piece = None
                    self.draw_board()
                    if self.check_game_over():
                        return
                    self.is_ai_turn = True
                    self.master.after(500, self.ai_turn)
            elif self.logic.board[row][col] == self.human_player:
                self.logic.selected_piece = (row, col)
                self.highlight_selected_piece(row, col)

    def highlight_selected_piece(self, row, col):
        x = col * 100 + 50
        y = row * 100 + 50
        radius = 25
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline='yellow', width=3)

    def ai_turn(self):
        if self.logic.game_over:
            return
        
        ai_move = self.logic.get_ai_move()
        if ai_move:
            total_pieces = self.logic.placed_pieces['X'] + self.logic.placed_pieces['O']
            if total_pieces < 6:
                row, col = ai_move
                if self.logic.place_piece(row, col):
                    self.draw_board()
                    self.check_game_over()
            else:
                start_row, start_col, end_row, end_col = ai_move
                if self.logic.move_piece(start_row, start_col, end_row, end_col):
                    self.draw_board()
                    self.check_game_over()
        
        self.is_ai_turn = False

    def check_game_over(self):
        if self.logic.check_win(0, 0):
            self.logic.game_over = True
            winner = "Les Blancs" if self.logic.current_player == 'X' else "Les Noirs"
            messagebox.showinfo("Fin de la partie", f"{winner} gagnent!")
            self.master.quit()
            return True
        else:
            self.logic.node.player = 'O' if self.logic.current_player == 'X' else 'X'
            self.logic.current_player = self.logic.node.player
            return False

