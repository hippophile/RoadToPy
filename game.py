import pygame
import sys

# Αρχικοποίηση Pygame
pygame.init()

# Ρυθμίσεις παραθύρου
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Χρώματα
WHITE = (255, 255, 255)

# Φόρτωση εικόνων
background = pygame.image.load('pic.jpg')
character_idle = pygame.image.load('pic.jpg')
character_run1 = pygame.image.load('pic.jpg')
character_run2 = pygame.image.load('pic.jpg')
platform_img = pygame.image.load('pic.jpg')

# Ρυθμίσεις χαρακτήρα
character = character_idle
character_rect = character.get_rect()
character_rect.topleft = (100, 100)
character_speed = 5
character_vel_y = 0
on_ground = False

# Πλατφόρμες
platforms = [pygame.Rect(200, 500, 400, 50), pygame.Rect(600, 400, 200, 50), pygame.Rect(50, 300, 200, 50)]

# Σημείο ελέγχου (checkpoint)
checkpoint = pygame.Rect(700, 100, 50, 50)
spawn_point = (100, 100)

# Βοηθητικές συναρτήσεις
def draw_background():
    screen.blit(background, (0, 0))

def draw_platforms():
    for platform in platforms:
        screen.blit(platform_img, platform)

def check_collision(rect, platforms):
    for platform in platforms:
        if rect.colliderect(platform):
            return platform
    return None

def reset_to_checkpoint():
    global character_rect, character_vel_y
    character_rect.topleft = spawn_point
    character_vel_y = 0

# Κύριος βρόχος παιχνιδιού
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Κίνηση χαρακτήρα
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        character_rect.x -= character_speed
        character = character_run1 if character == character_run2 else character_run2
    if keys[pygame.K_d]:
        character_rect.x += character_speed
        character = character_run1 if character == character_run2 else character_run2

    # Βαρύτητα
    character_vel_y += 1  # Σταδιακή αύξηση της ταχύτητας λόγω βαρύτητας
    character_rect.y += character_vel_y

    # Έλεγχος αν ο χαρακτήρας βρίσκεται στο έδαφος
    platform = check_collision(character_rect, platforms)
    if platform:
        if character_vel_y > 0:
            character_rect.bottom = platform.top
            character_vel_y = 0
            on_ground = True
    else:
        on_ground = False

    # Άλμα
    if keys[pygame.K_w] and on_ground:
        character_vel_y = -15  # Αρνητική ταχύτητα για να κινηθεί προς τα πάνω

    # Επαναφορά σε σημείο ελέγχου αν πέσει εκτός παραθύρου
    if character_rect.top > HEIGHT:
        reset_to_checkpoint()

    # Σχεδίαση
    draw_background()
    draw_platforms()
    screen.blit(character, character_rect)
    pygame.display.flip()

    clock.tick(30)
