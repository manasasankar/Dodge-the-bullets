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

# Player settings
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

# Enemy settings
enemy_size = 50
enemy_speed = 10
enemies = [[random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)]]  # Start with one enemy

# Bullets
bullets = []
bullet_speed = 15
bullet_size = (10, 20)

# Score
score = 0
best_score = 0  # Variable to store the best score

# Music Settings
music_enabled = True  # Default music is enabled

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

# Music Functions
def play_background_music():
    if music_enabled:
        pygame.mixer.music.load("assets/music/background.mp3")
        pygame.mixer.music.play(-1)  # Loop music indefinitely

def stop_music():
    pygame.mixer.music.stop()

def play_game_over_music():
    if music_enabled:
        pygame.mixer.music.load("assets/music/game_over.mp3")
        pygame.mixer.music.play()

# Game functions
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
    stop_music()  # Stop the background music
    play_game_over_music()  # Play game over music
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

def main_start_page():
    """Start page with a stylish title and description."""
    screen.fill(LIGHT_PURPLE)  # Light Purple background
    title_text = large_font.render("Dodge and Shoot the Blocks", True, BLUE)
    description_text = font.render("Avoid enemies and shoot to score.", True, BLACK)
    start_button_text = font.render("Press Space to Start", True, RED)
    settings_button_text = font.render("Settings", True, BLACK)

    # Draw title and description
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(description_text, (WIDTH//2 - description_text.get_width()//2, HEIGHT//2 - 50))
    
    # Draw settings button
    screen.blit(settings_button_text, (WIDTH//2 - settings_button_text.get_width()//2, HEIGHT//2 + 80))
    screen.blit(start_button_text, (WIDTH//2 - start_button_text.get_width()//2, HEIGHT//2 + 120))

    pygame.display.update()

    # Wait for player input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Start the game
                if event.key == pygame.K_s:
                    show_settings()  # Show settings page
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def show_settings():
    """Show settings for music and instructions."""
    global music_enabled

    # Settings screen background
    screen.fill(LIGHT_BLUE)
    
    settings_title = large_font.render("Settings", True, BLUE)
    music_text = font.render(f"Music: {'On' if music_enabled else 'Off'}", True, BLACK)
    help_text = font.render("Press H for Help (Instructions)", True, BLACK)
    back_text = font.render("Press B to go Back", True, RED)

    # Draw settings text
    screen.blit(settings_title, (WIDTH//2 - settings_title.get_width()//2, HEIGHT//2 - 100))
    screen.blit(music_text, (WIDTH//2 - music_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(help_text, (WIDTH//2 - help_text.get_width()//2, HEIGHT//2))
    screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT//2 + 50))

    pygame.display.update()

    # Wait for player input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return  # Go back to the start page
                if event.key == pygame.K_h:
                    game_instructions()  # Show the instructions
                if event.key == pygame.K_m:
                    music_enabled = not music_enabled  # Toggle music
                    if music_enabled:
                        play_background_music()
                    else:
                        stop_music()

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def game_instructions():
    """Show game instructions."""
    instructions_title = large_font.render("Game Instructions", True, BLUE)
    instruction1 = font.render("1. Use Arrow Keys to Move", True, BLACK)
    instruction2 = font.render("2. Press Spacebar to Shoot", True, BLACK)
    instruction3 = font.render("3. Avoid Enemies and Dodge Bullets", True, BLACK)
    start_text = font.render("Press Space to Start", True, RED)

    screen.fill(LIGHT_BLUE)  # Light Blue background for instructions
    screen.blit(instructions_title, (WIDTH//2 - instructions_title.get_width()//2, HEIGHT//2 - 100))
    screen.blit(instruction1, (WIDTH//2 - instruction1.get_width()//2, HEIGHT//2 - 50))
    screen.blit(instruction2, (WIDTH//2 - instruction2.get_width()//2, HEIGHT//2))
    screen.blit(instruction3, (WIDTH//2 - instruction3.get_width()//2, HEIGHT//2 + 50))
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 120))

    pygame.display.update()

    # Wait for player to press 'Space' to start the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Start the game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Main loop
load_best_score()
play_background_music()  # Start the background music

while True:
    main_start_page()  # Show start page
    # Main game logic goes here...
