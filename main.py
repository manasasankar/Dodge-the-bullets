import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.Sound("assets/bgmusic.mp3").play(-1)
except pygame.error as e:
    print(f"Error loading music: {e}") 

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Dodge the bullets")

WHITE = (255, 255, 255)
LIGHT_PURPLE = (216, 169, 255)  
LIGHT_BLUE = (169, 216, 255)    
LIGHT_GRAY = (211, 211, 211)    
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 35)
large_font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

player_img = pygame.image.load("assets/enemy/idle.png")
enemy_imgs = [
    pygame.image.load("assets/enemy/off.png"),
    pygame.image.load("assets/enemy/RockHead.png"),
    pygame.image.load("assets/enemy/Spiked Ball.png"),
    pygame.image.load("assets/enemy/spikehead.png")
]
background_img = pygame.image.load("assets/Background/Purple.png")
brown_bg_img = pygame.image.load("assets/Background/Brown.png")
bullet_img = pygame.image.load("assets/bullet.png")

player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

enemy_size = 50
enemy_speed = 7
max_enemies = 10
enemies = [[random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)] for _ in range(random.randint(3, 5))]

bullets = []
bullet_speed = 15
bullet_size = (10, 20)

score = 0
best_score = 0

def load_best_score():
    global best_score
    try:
        with open("best_score.txt", "r") as file:
            best_score = int(file.read())
    except FileNotFoundError:
        best_score = 0

def save_best_score():
    global best_score
    with open("best_score.txt", "w") as file:
        file.write(str(best_score))

def detect_collision(pos1, size1, pos2, size2):
    x1, y1 = pos1
    x2, y2 = pos2
    w1, h1 = size1
    w2, h2 = size2

    if (x1 < x2 + w2 and x1 + w1 > x2) and (y1 < y2 + h2 and y1 + h1 > y2):
        return True
    return False

def show_game_over_screen():
    game_over_text = large_font.render("Game Over", True, RED)
    replay_text = font.render("Press R to replay", True, WHITE)
    best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))

    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    screen.blit(replay_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    screen.blit(best_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))
    pygame.display.update()

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
    instructions_text = large_font.render("Instructions", True, BLUE)
    instruction1 = font.render("Use Arrow Keys to Move", True, RED)
    instruction2 = font.render("Press Spacebar to Shoot", True, RED)
    instruction3 = font.render("Avoid Enemies and Dodge Bullets", True, RED)
    start_text = font.render("Press Space to Start", True, BLUE)

    current_width, current_height = pygame.display.get_surface().get_size()

    instruction_start_x = (current_width - instructions_text.get_width()) // 2

    screen.blit(instructions_text, (instruction_start_x, current_height // 2 - 100))
    screen.blit(instruction1, (instruction_start_x, current_height // 2 - 50))
    screen.blit(instruction2, (instruction_start_x, current_height // 2))
    screen.blit(instruction3, (instruction_start_x, current_height // 2 + 50))
    screen.blit(start_text, (instruction_start_x, current_height // 2 + 100))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def update_enemies():
    global score

    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemy[0] = random.randint(0, WIDTH - enemy_size)
            enemy[1] = 0
            enemy[2] = random.choice(enemy_imgs)
            score += 1

    max_enemies = 10 if score >= 3 else 7

    if score % 5 == 0 and score != 0:
        if len(enemies) < max_enemies:
            enemies.append([random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)])

def draw_background(page="game"):
    if page == "start" or page == "instructions":
        screen.fill(BLACK)
    else:
        screen.fill(BLACK)

def resize_screen():
    global WIDTH, HEIGHT, screen, player_pos
    current_width, current_height = pygame.display.get_surface().get_size()

    if current_width != WIDTH or current_height != HEIGHT:
        WIDTH, HEIGHT = current_width, current_height
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]

def main_game():
    global WIDTH, HEIGHT, score, enemies, bullets, player_pos, best_score, screen
    
    if not pygame.display.get_surface():    
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    screen = pygame.display.get_surface()
    
    score = 0
    enemies = [[random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)]]
    bullets = []
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
    
    bullet_fire_interval = 300
    last_bullet_time = 0

    game_over = False
    while not game_over:
        resize_screen()
        draw_background(page="game")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                resize_screen()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                elif event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += 10

        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_bullet_time >= bullet_fire_interval:
            bullets.append([player_pos[0] + player_size // 2 - bullet_size[0] // 2, player_pos[1]])
            last_bullet_time = current_time

        bullets = [[b[0], b[1] - bullet_speed] for b in bullets if b[1] > 0]
        update_enemies()
        
        if score % 5 == 0 and score != 0 and len(enemies) < 7:
            enemies.append([random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)])

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if detect_collision(bullet, bullet_size, (enemy[0], enemy[1]), (enemy_size, enemy_size)):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append([random.randint(0, WIDTH - enemy_size), 0, random.choice(enemy_imgs)])
                    score += 5
                    break

        for enemy in enemies:
            if detect_collision(player_pos, (player_size, player_size), (enemy[0], enemy[1]), (enemy_size, enemy_size)):
                game_over = True
                break

        screen.blit(player_img, (player_pos[0], player_pos[1]))
        for enemy in enemies:
            screen.blit(enemy[2], (enemy[0], enemy[1]))
        for bullet in bullets:
            screen.blit(bullet_img, (bullet[0], bullet[1]))

        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(30)

    if score > best_score:
        best_score = score
        save_best_score()

    return show_game_over_screen()

load_best_score()

start_page = True
while start_page:
    draw_background(page="start")
    pygame.mixer.music.stop()

    start_text = large_font.render("Dodge the Bullets!", True, BLUE)
    start_button = font.render("Press Space to Start", True, RED)

    current_width, current_height = pygame.display.get_surface().get_size()

    screen.blit(start_text, ((current_width - start_text.get_width()) // 2, current_height // 2 - 50))
    screen.blit(start_button, ((current_width - start_button.get_width()) // 2, current_height // 2 + 50))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_page = False
                break
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_page = False
                break
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

screen.fill(WHITE)
draw_background(page="instructions")
game_instructions()

while True:
    if not main_game():
        break
