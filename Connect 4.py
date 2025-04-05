import pygame
import sys
import numpy as np
import math

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Board Dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

# ---------- Game Logic ----------
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

def draw_board(screen, board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2),
                int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.display.update()

# ---------- Button Class ----------
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_x, mouse_y) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# ---------- Home Page ----------
def homepage():
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Connect Four Homepage")
    font_large = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 32)
    title = font_large.render("CONNECT FOUR", True, GRAY)
    title_rect = title.get_rect(center=(300, 60))

    play_button = Button("Play", 200, 150, 200, 50, GRAY, RED, font_small)
    exit_button = Button("Exit", 200, 250, 200, 50, GRAY, RED, font_small)

    while True:
        screen.fill(BLACK)
        screen.blit(title, title_rect)
        play_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if play_button.is_clicked(event):
                return  # Start game
            if exit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# ---------- Game Loop ----------
def connect_four_game():
    board = create_board()
    game_over = False
    turn = 0
    screen = pygame.display.set_mode(size)
    draw_board(screen, board)
    font = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                color = RED if turn == 0 else YELLOW
                pygame.draw.circle(screen, color, (posx, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1 if turn == 0 else 2)

                    if winning_move(board, 1 if turn == 0 else 2):
                        label = font.render(f"Player {turn + 1} wins!!", 1, RED if turn == 0 else YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                    draw_board(screen, board)
                    turn = (turn + 1) % 2

                    if game_over:
                        pygame.display.update()
                        pygame.time.wait(3000)

# ---------- Main ----------
if __name__ == "__main__":
    pygame.init()
    homepage()
    connect_four_game()