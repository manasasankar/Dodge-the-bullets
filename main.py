import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge and Shoot the Blocks")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)  # Added definition for BLACK color

# Fonts
font = pygame.font.Font(None, 35)
large_font = pygame.font.Font(None, 50)

# Clock
clock = pygame.time.Clock()

# Player settings
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

# Enemy settings
enemy_size = 50
enemy_speed = 10
enemies = [[random.randint(0, WIDTH - enemy_size), 0]]

# Bullets
bullets = []
bullet_speed = 15
bullet_size = (10, 20)

# Score
score = 0
best_score = 0  # Variable to store the best score

# Load the best score from a file
def load_best_score():
    global best_score
    try:
        with open("best_score.txt", "r") as file:
            best_score = int(file.read())
    except FileNotFoundError:
        best_score = 0  # If the file doesn't exist, the best score is 0

# Save the best score to a file
def save_best_score():
    global best_score
    with open("best_score.txt", "w") as file:
        file.write(str(best_score))

def detect_collision(pos1, size1, pos2, size2):
    """Detects collision between two rectangles."""
    x1, y1 = pos1
    x2, y2 = pos2
    w1, h1 = size1
    w2, h2 = size2

    if (x1 < x2 + w2 and x1 + w1 > x2) and (y1 < y2 + h2 and y1 + h1 > y2):
        return True
    return False

def show_game_over_screen():
    """Display game over message and prompt to replay."""
    pygame.mixer.music.stop()  # Stop any background music
    game_over_text = large_font.render("Game Over", True, RED)
    replay_text = font.render("Press R to replay", True, BLUE)
    best_score_text = font.render(f"Best Score: {best_score}", True, BLACK)
    
    screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
    screen.blit(replay_text, (WIDTH//2 - 100, HEIGHT//2 + 50))
    screen.blit(best_score_text, (WIDTH//2 - 100, HEIGHT//2 + 100))
    pygame.display.update()

    # Wait for player to press 'R' to replay or 'Q' to quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def game_instructions():
    """Display game instructions."""
    pygame.mixer.music.stop()  # Stop any background music
    instructions_text = large_font.render("Instructions", True, BLUE)
    instruction1 = font.render("Use Arrow Keys to Move", True, BLACK)
    instruction2 = font.render("Press Spacebar to Shoot", True, BLACK)
    instruction3 = font.render("Avoid Enemies and Dodge Bullets", True, BLACK)
    start_text = font.render("Press Space to Start", True, RED)

    screen.blit(instructions_text, (WIDTH//2 - 150, HEIGHT//2 - 100))
    screen.blit(instruction1, (WIDTH//2 - 150, HEIGHT//2 - 50))
    screen.blit(instruction2, (WIDTH//2 - 150, HEIGHT//2))
    screen.blit(instruction3, (WIDTH//2 - 150, HEIGHT//2 + 50))
    screen.blit(start_text, (WIDTH//2 - 150, HEIGHT//2 + 100))
    pygame.display.update()

    # Wait for player to press 'Space' to start the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_game():
    global score, enemies, bullets, player_pos, best_score

    # Reset game variables
    score = 0
    enemies = [[random.randint(0, WIDTH - enemy_size), 0]]
    bullets = []
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

    # Game loop
    game_over = False
    while not game_over:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += 10

        # Shoot bullets
        if keys[pygame.K_SPACE]:
            bullets.append([player_pos[0] + player_size // 2 - bullet_size[0] // 2, player_pos[1]])

        # Update bullet positions
        bullets = [[b[0], b[1] - bullet_speed] for b in bullets if b[1] > 0]

        # Add more enemies as score increases
        if score >= 5 and len(enemies) < 2:
            enemies.append([random.randint(0, WIDTH - enemy_size), 0])
        if score >= 10 and len(enemies) < 4:
            enemies.append([random.randint(0, WIDTH - enemy_size), 0])
        if score >= 20 and len(enemies) < 6:
            enemies.append([random.randint(0, WIDTH - enemy_size), 0])

        # Update enemies
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                enemy[0] = random.randint(0, WIDTH - enemy_size)
                enemy[1] = 0
                score += 1

        # Check collisions between bullets and enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if detect_collision(bullet, bullet_size, enemy, (enemy_size, enemy_size)):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append([random.randint(0, WIDTH - enemy_size), 0])
                    score += 5
                    break

        # Collision detection between player and enemies
        for enemy in enemies:
            if detect_collision(player_pos, (player_size, player_size), enemy, (enemy_size, enemy_size)):
                game_over = True

        # Draw player, enemies, and bullets
        pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_size[0], bullet_size[1]))

        # Show score
        text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(30)

    # Update the best score if necessary
    if score > best_score:
        best_score = score
        save_best_score()

    # Display game over screen and wait for player input
    return show_game_over_screen()

# Load the best score from the file
load_best_score()

# Main loop for start page
start_page = True
while start_page:
    screen.fill(WHITE)  # Clear the screen before displaying anything
    pygame.mixer.music.stop()  # Stop any background music

    # Display start page with instructions
    start_text = large_font.render("Dodge the Bullets!", True, BLUE)
    start_button = font.render("Press Space to Start", True, RED)

    screen.blit(start_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
    screen.blit(start_button, (WIDTH//2 - 100, HEIGHT//2 + 50))
    pygame.display.update()

    # Wait for player to press 'Space' to start the game
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_page = False
                break  # Exit the loop when space is pressed
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Clear the screen before showing instructions
screen.fill(WHITE)  # Clear screen

# Now display game instructions **after** the start page ends
game_instructions()  # This will show instructions once space is pressed

# Start the main game loop
while main_game():
    # If main_game returns True (player wants to replay), restart the game
    continue

pygame.quit()
