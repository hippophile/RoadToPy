import pygame
import pygame_menu
import sys
import random

pygame.init()

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

# Δημιουργία αρχικών συντεταγμένων για τον κύκλο
x = random.randint(radius + margin, screen_size - radius - margin)
y = random.randint(radius + margin, screen_size - radius - margin)

def draw_courses():
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

def set_difficulty(value, difficulty):
    print(f'Difficulty set to {difficulty}')

def start_the_game():
    global running, match
    print("Starting the game!")
    match = True
    running = True
    menu.disable()

# Δημιουργία μενού
menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Εμφάνιση μενού πριν από το παιχνίδι
menu.mainloop(screen)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Έλεγχος αν ο χρήστης έκανε κλικ στον κύκλο
            if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= radius ** 2:
                score += 1
                print(f"Score: {score}")
                # Μετακίνηση του κύκλου σε νέα τυχαία θέση
                x = random.randint(radius + margin, screen_size - radius - margin)
                y = random.randint(radius + margin, screen_size - radius - margin)

    # Ενημέρωση οθόνης
    screen.blit(background_image, (0, 0))
    draw_courses()
    pygame.display.flip()

pygame.quit()
sys.exit()
