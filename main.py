import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the bullets")

# Colors
WHITE = (255, 255, 255)
LIGHT_PURPLE = (216, 169, 255)  # Light Purple for the start page
LIGHT_BLUE = (169, 216, 255)    # Light Blue for the instructions page
LIGHT_GRAY = (211, 211, 211)   # Light Gray for the game page
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 35)
large_font = pygame.font.Font(None, 50)

# Clock
clock = pygame.time.Clock()

# Load assets
player_img = pygame.image.load("assets/enemy/idle.png")
enemy_imgs = [
    pygame.image.load("assets/enemy/off.png"),
    pygame.image.load("assets/enemy/RockHead.png"),
    pygame.image.load("assets/enemy/Spiked Ball.png"),
    pygame.image.load("assets/enemy/spikehead.png")
]
background_img = pygame.image.load("assets/Background/Purple.png")
brown_bg_img = pygame.image.load("assets/Background/Brown.png")  # Load Brown.png
bullet_img = pygame.image.load("assets/bullet.png")  # Load bullet image

# Player settings
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

# Enemy settings
enemy_size = 50
enemy_speed = 7
enemies = [[random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)]]  # Start with one enemy

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
    replay_text = font.render("Press R to replay", True, WHITE)
    best_score_text = font.render(f"Best Score: {best_score}", True, (255,255,255))
    
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
    instruction1 = font.render("Use Arrow Keys to Move", True, RED)
    instruction2 = font.render("Press Spacebar to Shoot", True, RED)
    instruction3 = font.render("Avoid Enemies and Dodge Bullets", True, RED)
    start_text = font.render("Press Space to Start", True, BLUE)

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

def update_enemies():
    global score  # Access the global score variable
    # Update positions of existing enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed  # Move enemy downward
        if enemy[1] > HEIGHT:
            # Reset to a random x-coordinate and reuse the image
            enemy[0] = random.randint(0, WIDTH - enemy_size)  # Random x position
            enemy[1] = 0  # Reset y-coordinate to the top
            score += 1  # Increase score when an enemy goes off-screen

    # Set max enemy count depending on the score
    max_enemies = 10 if score >= 3 else 7  # Max 10 enemies after score reaches 3

    # Add new enemies after every 5 points, but ensure the total enemies do not exceed max_enemies
    if score % 5 == 0 and score != 0 and len(enemies) < max_enemies:
        available_enemies = [img for img in enemy_imgs if img not in [e[2] for e in enemies]]

        # If there are available enemies to add, choose one; otherwise, reset an existing enemy
        if available_enemies:
            enemy_type = random.choice(available_enemies)
            enemies.append([random.randint(0, WIDTH - enemy_size), 0, enemy_type])
        else:
            # If no unique enemies are left, reset one of the existing enemies
            existing_enemy = random.choice(enemies)
            existing_enemy[0] = random.randint(0, WIDTH - enemy_size)
            existing_enemy[1] = 0  # Reset y-coordinate to the top
            existing_enemy[2] = random.choice(enemy_imgs)  # Randomly select a new image for the enemy


def draw_background(page="game"):
    """Draw background based on the current page."""
    if page == "start" or page == "instructions":
        screen.fill(BLACK)  # Black background for start and instructions pages
    else:
        screen.fill(BLACK)  # Use black background for the game page

def main_game():
    global score, enemies, bullets, player_pos, best_score

    # Reset game variables
    score = 0
    enemies = [[random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)]]  # Assign random image
    bullets = []
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

    # Bullet firing interval (in milliseconds)
    bullet_fire_interval = 300  # Adjust this value for desired gap between bullets
    last_bullet_time = 0  # To track the time of the last bullet fired

    # Game loop
    game_over = False
    while not game_over:
        draw_background(page="game")  # Use Brown.png background for the game page
        
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

        # Bullet firing logic with interval
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if keys[pygame.K_SPACE] and current_time - last_bullet_time >= bullet_fire_interval:
            bullets.append([player_pos[0] + player_size // 2 - bullet_size[0] // 2, player_pos[1]])
            last_bullet_time = current_time  # Update the last bullet time

        # Update bullet positions and enemies
        bullets = [[b[0], b[1] - bullet_speed] for b in bullets if b[1] > 0]
        update_enemies()  # Update enemy positions
        
        # Add new enemies after every 5 points
        if score % 5 == 0 and score != 0 and len(enemies) < 7:
            enemies.append([random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)])

        # Check collisions between bullets and enemies
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if detect_collision(bullet, bullet_size, (enemy[0], enemy[1]), (enemy_size, enemy_size)):  # Pass only the position (x, y)
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append([random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)])  # Assign a random image to the new enemy
                    score += 5
                    break

        # Collision detection between player and enemies
        for enemy in enemies:
            if detect_collision(player_pos, (player_size, player_size), (enemy[0], enemy[1]), (enemy_size, enemy_size)):  # Use only position (x, y)
                game_over = True
                break  # Exit the loop once the game over condition is met

        # Draw player, enemies, and bullets using images
        screen.blit(player_img, (player_pos[0], player_pos[1]))  # Draw the player image
        for enemy in enemies:
            screen.blit(enemy[2], (enemy[0], enemy[1]))  # Draw the specific enemy image (stored in enemy[2])
        for bullet in bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))  # Draw the bullet image

        # Show score
        text = font.render(f"Score: {score}", True, (255,255,255))
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
    draw_background(page="start")  # Use light purple background for the start page
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
                start_page = False  # Exit the loop when space is pressed
                break
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Now, clear the screen and show the instructions
screen.fill(WHITE)  # Ensure the screen is cleared before showing instructions
draw_background(page="instructions")  # Use light blue background for the instructions page
game_instructions()  # Show the game instructions

# Start the game
while True:
    if not main_game():
        break  # Restart the game loop after game over
