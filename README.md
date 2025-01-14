# Dodge and Shoot the Blocks Game

This is a simple dodge-and-shoot game created using Python's `pygame` library. The player controls a character that must dodge falling enemies and shoot them with bullets to earn points.

## Game Features:
- **Player Movement:** Use the arrow keys to move the player left and right.
- **Shooting:** Press the spacebar to shoot bullets at the enemies.
- **Enemies:** Enemies randomly appear from the top and fall towards the player. Avoid the enemies or shoot them to gain points.
- **Score System:** Earn points by shooting enemies. Your score is displayed at the top of the screen.
- **Game Over:** The game ends if the player collides with an enemy.
- **Best Score:** The best score is saved and displayed across game sessions.

## Installation

To run the game, ensure that you have Python installed on your machine. Then, install the `pygame` library.

1. Install Python (if not already installed): [Download Python](https://www.python.org/downloads/)
2. Install the `pygame` library:
    ```bash
    pip install pygame
    ```

## Game Assets

The game uses images for the player and enemies, which are loaded from the `assets/` folder. You can customize these images as per your preference.

Make sure the following files are present:
- **Player Image:** `assets/enemy/idle.png`
- **Enemy Images:** `assets/enemy/off.png`, `assets/enemy/RockHead.png`, `assets/enemy/Spiked Ball.png`, `assets/enemy/spikehead.png`
- **Background Image:** `assets/Background/Purple.png`

## Game Instructions

1. **Start Screen:** Press the spacebar to start the game.
2. **Movement:** Use the left and right arrow keys to move the player.
3. **Shooting:** Press the spacebar to shoot bullets.
4. **Avoidance:** Avoid colliding with enemies or their bullets.
5. **End Game:** The game ends when the player collides with an enemy.

## Game Controls:
- **Arrow Keys (Left/Right):** Move the player.
- **Spacebar:** Shoot bullets.

## Files

- **`best_score.txt`:** Stores the highest score achieved across game sessions.
- **`main.py`:** Main game code.

## Run the Game

To play the game, simply run the Python script:

```bash
python main.py
