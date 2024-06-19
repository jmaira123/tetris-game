import tkinter as tk
import random

# Game configuration
GAME_WIDTH = 300
GAME_HEIGHT = 600
GRID_SIZE = 30
BOARD_WIDTH = GAME_WIDTH // GRID_SIZE
BOARD_HEIGHT = GAME_HEIGHT // GRID_SIZE
SPEED = 500  # Milliseconds between moves

SHAPES = [
    ([[1, 1, 1, 1]], "cyan"),  # I
    ([[1, 1], [1, 1]], "yellow"),  # O
    ([[1, 1, 0], [0, 1, 1]], "green"),  # S
    ([[0, 1, 1], [1, 1, 0]], "red"),  # Z
    ([[1, 1, 1], [0, 1, 0]], "purple"),  # T
    ([[1, 1, 1], [1, 0, 0]], "orange"),  # L
    ([[1, 1, 1], [0, 0, 1]], "blue"),  # J
]

class Tetris(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tetris")
        self.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self, width=GAME_WIDTH, height=GAME_HEIGHT, bg="black")
        self.canvas.pack()

        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.colors = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

        self.current_shape, self.current_color = self.get_new_shape()
        self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2]

        self.bind("<Left>", self.move_left)
        self.bind("<Right>", self.move_right)
        self.bind("<Down>", self.move_down)
        self.bind("<Up>", self.rotate_shape)

        self.after(SPEED, self.game_loop)

    def get_new_shape(self):
        return random.choice(SHAPES)

    def draw_shape(self):
        self.canvas.delete("shape")
        for i, row in enumerate(self.current_shape):
            for j, val in enumerate(row):
                if val:
                    x = (self.current_position[1] + j) * GRID_SIZE
                    y = (self.current_position[0] + i) * GRID_SIZE
                    self.canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=self.current_color, tags="shape")
        
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("board")
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val:
                    x = j * GRID_SIZE
                    y = i * GRID_SIZE
                    self.canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=self.colors[i][j], tags="board")

    def move_left(self, event):
        self.current_position[1] -= 1
        if not self.valid_position():
            self.current_position[1] += 1

    def move_right(self, event):
        self.current_position[1] += 1
        if not self.valid_position():
            self.current_position[1] -= 1

    def move_down(self, event=None):
        self.current_position[0] += 1
        if not self.valid_position():
            self.current_position[0] -= 1
            self.lock_shape()
            self.clear_lines()
            self.current_shape, self.current_color = self.get_new_shape()
            self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2]
            if not self.valid_position():
                self.game_over()

    def rotate_shape(self, event):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        if not self.valid_position():
            self.current_shape = [list(row) for row in zip(*self.current_shape)][::-1]

    def valid_position(self):
        for i, row in enumerate(self.current_shape):
            for j, val in enumerate(row):
                if val:
                    x = self.current_position[1] + j
                    y = self.current_position[0] + i
                    if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT or self.board[y][x]:
                        return False
        return True

    def lock_shape(self):
        for i, row in enumerate(self.current_shape):
            for j, val in enumerate(row):
                if val:
                    self.board[self.current_position[0] + i][self.current_position[1] + j] = 1
                    self.colors[self.current_position[0] + i][self.current_position[1] + j] = self.current_color

    def clear_lines(self):
        new_board = [row for row in self.board if not all(val == 1 for val in row)]
        new_colors = [row for row in self.colors if not all(col is not None for col in row)]
        lines_cleared = BOARD_HEIGHT - len(new_board)
        new_board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(lines_cleared)] + new_board
        new_colors = [[None for _ in range(BOARD_WIDTH)] for _ in range(lines_cleared)] + new_colors
        self.board = new_board
        self.colors = new_colors

    def game_loop(self):
        self.move_down()
        self.draw_shape()
        self.after(SPEED, self.game_loop)

    def game_over(self):
        self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, text="Game Over", fill="red", font=("Helvetica", 24))
        self.unbind("<Left>")
        self.unbind("<Right>")
        self.unbind("<Down>")
        self.unbind("<Up>")

if __name__ == "__main__":
    game = Tetris()
    game.mainloop()
