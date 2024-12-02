import pygame
import sys

pygame.init()

screen_size = 600

screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Triliza")

background_color = (225, 225, 255)  # white
line_color = (0, 0, 0)  # black

line_thickness = 15

# Grid state (3x3)
grid = [[None for _ in range(3)] for _ in range(3)]

font = pygame.font.Font(None, 60)  # Default font for messages
button_font = pygame.font.Font(None, 40)  # Font for button text

button_rect = None

def draw_grid():
    # Horizontal lines
    pygame.draw.line(screen, line_color, (0, screen_size // 3), (screen_size, screen_size // 3), line_thickness)
    pygame.draw.line(screen, line_color, (0, 2 * screen_size // 3), (screen_size, 2 * screen_size // 3), line_thickness)

    # Vertical lines
    pygame.draw.line(screen, line_color, (screen_size // 3, 0), (screen_size // 3, screen_size), line_thickness)
    pygame.draw.line(screen, line_color, (2 * screen_size // 3, 0), (2 * screen_size // 3, screen_size), line_thickness)

def is_cell_empty(row, col):
    return grid[row][col] is None

def switch_player(player):
    return 'O' if player == 'X' else 'X'

def draw_symbol(row, col, player):
    if player == 'X':
        draw_x(row, col)
    elif player == 'O':
        draw_o(row, col)

def draw_x(row, col):
    cell_size = screen_size // 3
    x_start = col * cell_size
    y_start = row * cell_size
    pygame.draw.line(screen, (200, 0, 0), (x_start + 20, y_start + 20), (x_start + cell_size - 20, y_start + cell_size - 20), line_thickness)
    pygame.draw.line(screen, (200, 0, 0), (x_start + 20, y_start + cell_size - 20), (x_start + cell_size - 20, y_start + 20), line_thickness)

def draw_o(row, col):
    cell_size = screen_size // 3
    x_center = col * cell_size + cell_size // 2
    y_center = row * cell_size + cell_size // 2
    pygame.draw.circle(screen, (0, 0, 200), (x_center, y_center), cell_size // 3 - 20, line_thickness)

def check_winner():
    # Check rows
    for row in grid:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    # Check columns
    for col in range(3):
        if grid[0][col] == grid[1][col] == grid[2][col] and grid[0][col] is not None:
            return grid[0][col]

    # Check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] is not None:
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] is not None:
        return grid[0][2]

    # No winner
    return None

def check_tie():
    for row in grid:
        if None in row:
            return False
    return True

def display_end_message(winner):
    global button_rect  # Make button_rect accessible globally
    if winner:
        message = f"Player {winner} wins!"
    else:
        message = "It's a tie!"
    text = font.render(message, True, (0, 0, 0))
    screen.blit(text, (screen_size // 2 - text.get_width() // 2, screen_size // 2 - text.get_height() // 2))

    # Draw "Play Again" button
    button_text = button_font.render("Play Again", True, (255, 255, 255))
    button_rect = pygame.Rect(screen_size // 2 - 100, screen_size // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (0, 128, 0), button_rect)
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

    return button_rect

def reset_game():
    global grid, current_player, match
    grid = [[None for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    match = True

running = True
match = True
current_player = 'X'

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and match:
            mouse_x, mouse_y = event.pos
            row = mouse_y // (screen_size // 3)
            col = mouse_x // (screen_size // 3)

            if is_cell_empty(row, col):
                grid[row][col] = current_player
                draw_symbol(row, col, current_player)

                winner = check_winner()
                if winner:
                    print(f"Player {winner} wins!")
                    match = False
                elif check_tie():
                    match = False
                else:
                    current_player = switch_player(current_player)

        elif event.type == pygame.MOUSEBUTTONDOWN and not match:
            mouse_x, mouse_y = event.pos
            if button_rect.collidepoint(mouse_x, mouse_y):
                reset_game()

    screen.fill(background_color)
    draw_grid()
    
    for r in range(3):
        for c in range(3):
            if grid[r][c]:
                draw_symbol(r, c, grid[r][c])

    if not match:
        button_rect = display_end_message(check_winner())

    pygame.display.flip()

pygame.quit()
sys.exit()
