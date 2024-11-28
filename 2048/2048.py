import pygame
import random

# Ρυθμίσεις παραθύρου
WIDTH, HEIGHT = 400, 400
TILE_SIZE = WIDTH // 4
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Αρχικοποίηση Pygame
pygame.init()
FONT = pygame.font.Font(None, 40)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# Δημιουργία πίνακα
def init_board():
    board = [[0] * 4 for _ in range(4)]
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    empty_tiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_tiles:
        x, y = random.choice(empty_tiles)
        board[x][y] = 2 if random.random() < 0.9 else 4

# Σχεδίαση GUI
def draw_board(board):
    SCREEN.fill(BACKGROUND_COLOR)
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(SCREEN, TILE_COLORS.get(value, TILE_COLORS[2048]), rect)
            if value != 0:
                text = FONT.render(str(value), True, (119, 110, 101))
                text_rect = text.get_rect(center=rect.center)
                SCREEN.blit(text, text_rect)

# Κινήσεις
def move_left(board):
    for row in board:
        compressed_row = [num for num in row if num != 0]
        while len(compressed_row) < 4:
            compressed_row.append(0)
        for i in range(3):
            if compressed_row[i] == compressed_row[i + 1] and compressed_row[i] != 0:
                compressed_row[i] *= 2
                compressed_row[i + 1] = 0
        compressed_row = [num for num in compressed_row if num != 0]
        while len(compressed_row) < 4:
            compressed_row.append(0)
        row[:] = compressed_row

def move_right(board):
    for row in board:
        row.reverse()
        move_left([row])
        row.reverse()

def move_up(board):
    for col in range(4):
        column = [board[row][col] for row in range(4)]
        compressed_column = [num for num in column if num != 0]
        while len(compressed_column) < 4:
            compressed_column.append(0)
        for i in range(3):
            if compressed_column[i] == compressed_column[i + 1] and compressed_column[i] != 0:
                compressed_column[i] *= 2
                compressed_column[i + 1] = 0
        compressed_column = [num for num in compressed_column if num != 0]
        while len(compressed_column) < 4:
            compressed_column.append(0)
        for row in range(4):
            board[row][col] = compressed_column[row]

def move_down(board):
    for col in range(4):
        column = [board[row][col] for row in range(4)]
        column.reverse()
        compressed_column = [num for num in column if num != 0]
        while len(compressed_column) < 4:
            compressed_column.append(0)
        for i in range(3):
            if compressed_column[i] == compressed_column[i + 1] and compressed_column[i] != 0:
                compressed_column[i] *= 2
                compressed_column[i + 1] = 0
        compressed_column = [num for num in compressed_column if num != 0]
        while len(compressed_column) < 4:
            compressed_column.append(0)
        compressed_column.reverse()
        for row in range(4):
            board[row][col] = compressed_column[row]

# Έλεγχος για έγκυρη κίνηση
def valid_move_exists(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:  # Υπάρχει κενό πλακίδιο
                return True
            if i < 3 and board[i][j] == board[i + 1][j]:  # Κάθετη συγχώνευση
                return True
            if j < 3 and board[i][j] == board[i][j + 1]:  # Οριζόντια συγχώνευση
                return True
    return False

# Κύριος βρόχος παιχνιδιού
def main():
    clock = pygame.time.Clock()
    board = init_board()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left(board)
                elif event.key == pygame.K_RIGHT:
                    move_right(board)
                elif event.key == pygame.K_UP:
                    move_up(board)
                elif event.key == pygame.K_DOWN:
                    move_down(board)
                add_random_tile(board)

        if not valid_move_exists(board):
            print("Game Over!")
            running = False

        draw_board(board)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
