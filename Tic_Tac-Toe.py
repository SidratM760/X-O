import tkinter as tk
from tkinter import PhotoImage
import time
import threading

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.clear_screen()
        # Load and resize the logo image
        logo_image = PhotoImage(file="logo.png").subsample(2, 2)  # Adjust scaling factor as needed
        logo = tk.Label(self.root, image=logo_image)
        logo.image = logo_image  # Keep a reference to avoid garbage collection
        logo.pack(pady=20)
        title = tk.Label(self.root, text="Tic-Tac-Toe", font=('Arial', 26, 'bold'), fg="#af3b44")  
        title.pack(pady=10)
        start_button = tk.Button(self.root, text="Play", font=('Arial', 18), bg="#14856F", fg="white", command=self.create_board) 
        start_button.pack(pady=20)

    def create_board(self):
        self.clear_screen()
        self.board = [" " for _ in range(9)]
        self.player_turn = True
        self.human_wins = 0
        self.ai_wins = 0

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True)

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.game_frame, text=" ", font=('Arial', 20), width=5, height=2,
                               command=lambda i=i: self.click(i), bg="#f0f0f0")  
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)
        
        self.result_label = tk.Label(self.root, text="", font=('Arial', 30, 'bold'), fg="#14856F")  
        self.result_label.pack(pady=20)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        play_again_button = tk.Button(self.button_frame, text="Reset", font=('Arial', 18), bg="#e88e1b", fg="white", command=self.reset_board)  # Blue button
        play_again_button.pack(pady=5)

        quit_button = tk.Button(self.button_frame, text="Quit", font=('Arial', 18), bg="#af3b44", fg="white", command=self.root.quit)  # Red button
        quit_button.pack(pady=5)

    def click(self, index):
        if self.board[index] == " " and self.player_turn:
            self.board[index] = "X"
            self.buttons[index].config(text="X", bg="#e88e1b") 
            self.player_turn = False
            if not self.check_winner():
                threading.Thread(target=self.delayed_ai_move).start()

    def delayed_ai_move(self):
        time.sleep(0.5)  # AI move delay
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                score = self.minimax(self.board, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i

        self.board[best_move] = "O"
        self.buttons[best_move].config(text="O", bg="#af3b44") 
        self.player_turn = True
        self.check_winner()

    def minimax(self, board, is_maximizing):
        winner, _ = self.check_winner_state(board)
        if winner == "X":
            return -1
        elif winner == "O":
            return 1
        elif " " not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        winner, condition = self.check_winner_state(self.board)
        if winner:
            self.draw_winning_box(condition)
            self.update_score(winner)
            self.show_result(f"{'You won!' if winner == 'X' else 'AI wins!'}")
            return True
        elif " " not in self.board:
            self.show_result("Draw!")
            return True
        return False

    def check_winner_state(self, board):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
                          (0, 4, 8), (2, 4, 6)]  # Diagonal
        for condition in win_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] != " ":
                return board[condition[0]], condition
        return None, None

    def draw_winning_box(self, condition):
        if condition:
            for i in condition:
                self.buttons[i].config(bg="#14856F")  

    def update_score(self, winner):
        if winner == "X":
            self.human_wins += 1
        else:
            self.ai_wins += 1

    def show_result(self, result):
        self.result_label.config(text=result)

    def reset_board(self):
        self.create_board()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
