import pygame
import pygame_menu
import sys
import random

pygame.init()

font = pygame.font.Font(None, 72)
screen_size = 900
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Click And Win")

background_image = pygame.image.load("click_and_win.jpg")
background_image = pygame.transform.scale(background_image, (screen_size, screen_size))

margin = 50
radius = 30
score = 0
running = False
match = False
game_state = True

# Δημιουργία αρχικών συντεταγμένων για τον κύκλο
x = random.randint(radius + margin, screen_size - radius - margin)
y = random.randint(radius + margin, screen_size - radius - margin)

# for the timer 
total_time = 5

def draw_courses():
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

def start_the_game():
    global running, match, t0, game_state, score, x, y
    print("Starting the game!")
    match = True
    running = True
    game_state = True
    score = 0
    t0 = pygame.time.get_ticks()  # Αποθηκεύει τον χρόνο που ξεκίνησε το παιχνίδι
    x = random.randint(radius + margin, screen_size - radius - margin)
    y = random.randint(radius + margin, screen_size - radius - margin)
    menu.disable()

# Δημιουργία μενού
custom_theme = pygame_menu.Theme(
    background_color=(0, 0, 0),  # Μαύρο φόντο
    title_background_color=(255, 0, 0),  # Κόκκινος τίτλος
    title_font_size=60,
    widget_font=pygame_menu.font.FONT_BEBAS,
    widget_font_color=(255, 255, 255),
)

menu = pygame_menu.Menu('Welcome', 850, 850, theme=custom_theme)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

game_over_menu = pygame_menu.Menu('Game Over', 850, 850, theme=custom_theme)

# Εμφάνιση μενού πριν από το παιχνίδι
menu.mainloop(screen)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_state:
            mouse_x, mouse_y = event.pos
            if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= radius ** 2:
                score += 1
                print(f"Score: {score}")
                x = random.randint(radius + margin, screen_size - radius - margin)
                y = random.randint(radius + margin, screen_size - radius - margin)

    if game_state:
        # Υπολογισμός χρόνου
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - t0) / 1000
        remaining_time = max(0, total_time - elapsed_time)

        # Έλεγχος αν τελείωσε ο χρόνος
        if remaining_time <= 0:
            game_state = False
            running = False
            game_over_menu.clear()
            game_over_menu.add.label(f"Your score was: {score}")
            game_over_menu.add.button('Play Again', start_the_game)
            game_over_menu.add.button('Quit', pygame_menu.events.EXIT)
            game_over_menu.mainloop(screen)

    # Ενημέρωση οθόνης για το παιχνίδι
    screen.blit(background_image, (0, 0))
    draw_courses()
    text_surface = font.render(f"Time: {remaining_time:.2f}", True, (255, 0, 0))
    screen.blit(text_surface, (650, 20))
    pygame.display.flip()

pygame.quit()
sys.exit()
