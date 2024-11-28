import pygame

# Ρυθμίσεις παραθύρου
WIDTH, HEIGHT = 600, 700  # Extra χώρο για την εμφάνιση πληροφοριών
GRID_SIZE = WIDTH // 8
BACKGROUND_COLOR = (0, 100, 0)
LINE_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 0)

# Αρχικοποίηση Pygame
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reversi (Othello)")
FONT = pygame.font.Font(None, 40)

# Αρχικοποίηση bitboards
black_bitboard = 0x0000000810000000  # Κεντρικές θέσεις για μαύρα
white_bitboard = 0x0000001008000000  # Κεντρικές θέσεις για άσπρα
turn = "BLACK"  # Ο πρώτος παίκτης είναι ο μαύρος

# Διευθύνσεις για κινήσεις (οριζόντια, κάθετα, διαγώνια)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Βοηθητικές συναρτήσεις για bitboards
def set_bit(board, row, col):
    return board | (1 << (row * 8 + col))

def clear_bit(board, row, col):
    return board & ~(1 << (row * 8 + col))

def is_bit_set(board, row, col):
    return board & (1 << (row * 8 + col))

# Έλεγχος έγκυρης κίνησης
def is_valid_move(row, col, current_board, opponent_board):
    if is_bit_set(current_board | opponent_board, row, col):
        return False

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        flipped = False
        while 0 <= r < 8 and 0 <= c < 8 and is_bit_set(opponent_board, r, c):
            flipped = True
            r += dr
            c += dc
        if flipped and 0 <= r < 8 and 0 <= c < 8 and is_bit_set(current_board, r, c):
            return True
    return False

# Εύρεση διαθέσιμων κινήσεων
def get_valid_moves(current_board, opponent_board):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(row, col, current_board, opponent_board):
                valid_moves.append((row, col))
    return valid_moves

# Ανατροπή πλακιδίων
def flip_pieces(row, col, current_board, opponent_board):
    global black_bitboard, white_bitboard
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        path = []
        while 0 <= r < 8 and 0 <= c < 8 and is_bit_set(opponent_board, r, c):
            path.append((r, c))
            r += dr
            c += dc
        if 0 <= r < 8 and 0 <= c < 8 and is_bit_set(current_board, r, c):
            for pr, pc in path:
                current_board = set_bit(current_board, pr, pc)
                opponent_board = clear_bit(opponent_board, pr, pc)
    return current_board, opponent_board

# Τοποθέτηση πλακιδίου
def place_piece(row, col, turn):
    global black_bitboard, white_bitboard
    if turn == "BLACK":
        if not is_valid_move(row, col, black_bitboard, white_bitboard):
            return False
        black_bitboard = set_bit(black_bitboard, row, col)
        black_bitboard, white_bitboard = flip_pieces(row, col, black_bitboard, white_bitboard)
    else:
        if not is_valid_move(row, col, white_bitboard, black_bitboard):
            return False
        white_bitboard = set_bit(white_bitboard, row, col)
        white_bitboard, black_bitboard = flip_pieces(row, col, white_bitboard, black_bitboard)
    return True

# Έλεγχος αν υπάρχουν διαθέσιμες κινήσεις
def has_valid_moves(current_board, opponent_board):
    return len(get_valid_moves(current_board, opponent_board)) > 0

# Υπολογισμός σκορ
def calculate_score(board):
    return bin(board).count("1")

# Σχεδιασμός ταμπλό
def draw_board(valid_moves):
    SCREEN.fill(BACKGROUND_COLOR)

    # Σχεδιασμός γραμμών
    for i in range(9):
        pygame.draw.line(SCREEN, LINE_COLOR, (0, i * GRID_SIZE), (WIDTH, i * GRID_SIZE), 2)
        pygame.draw.line(SCREEN, LINE_COLOR, (i * GRID_SIZE, 0), (i * GRID_SIZE, HEIGHT - 100), 2)

    # Σχεδιασμός πλακιδίων
    for row in range(8):
        for col in range(8):
            if is_bit_set(black_bitboard, row, col):
                pygame.draw.circle(SCREEN, BLACK_COLOR, (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 3)
            elif is_bit_set(white_bitboard, row, col):
                pygame.draw.circle(SCREEN, WHITE_COLOR, (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 3)

    # Σχεδιασμός διαθέσιμων κινήσεων
    for row, col in valid_moves:
        pygame.draw.circle(SCREEN, HIGHLIGHT_COLOR, (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 8)

    # Εμφάνιση πληροφοριών
    black_score = calculate_score(black_bitboard)
    white_score = calculate_score(white_bitboard)
    info_text = f"Turn: {turn} | Black: {black_score} | White: {white_score}"
    text = FONT.render(info_text, True, WHITE_COLOR)
    SCREEN.blit(text, (20, HEIGHT - 80))

# Κύριος βρόχος παιχνιδιού
def main():
    global turn
    clock = pygame.time.Clock()
    running = True

    while running:
        valid_moves = get_valid_moves(black_bitboard, white_bitboard) if turn == "BLACK" else get_valid_moves(white_bitboard, black_bitboard)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if y < HEIGHT - 100:
                    col, row = x // GRID_SIZE, y // GRID_SIZE
                    if place_piece(row, col, turn):
                        turn = "WHITE" if turn == "BLACK" else "BLACK"

        if not has_valid_moves(black_bitboard, white_bitboard) and not has_valid_moves(white_bitboard, black_bitboard):
            black_score = calculate_score(black_bitboard)
            white_score = calculate_score(white_bitboard)
            print(f"Game Over! Black: {black_score}, White: {white_score}")
            running = False

        draw_board(valid_moves)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
