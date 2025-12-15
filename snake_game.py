import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window setup
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game - Survival AI")

# Font for score and Game Over
font = pygame.font.SysFont(None, 30)
score = 0

# Grid settings
CELL_SIZE = 20
ROWS = WINDOW_HEIGHT // CELL_SIZE
COLS = WINDOW_WIDTH // CELL_SIZE

# Snake settings
snake_pos = [[5, 5]]  # initial snake head at grid position (5,5)
snake_direction = "RIGHT"

# Food settings
food_pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
food_color = (255, 0, 0)  # red

# Function to calculate next position based on direction
def next_pos(direction, head):
    x, y = head
    if direction == "UP":
        y = (y - 1) % ROWS
    elif direction == "DOWN":
        y = (y + 1) % ROWS
    elif direction == "LEFT":
        x = (x - 1) % COLS
    elif direction == "RIGHT":
        x = (x + 1) % COLS
    return [x, y]

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move snake
    head_x, head_y = snake_pos[0]

    # Survival-First AI
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    safe_moves = [d for d in directions if next_pos(d, [head_x, head_y]) not in snake_pos]

    # Prefer moves toward food
    preferred_moves = []
    if head_x < food_pos[0]:
        preferred_moves.append("RIGHT")
    elif head_x > food_pos[0]:
        preferred_moves.append("LEFT")
    if head_y < food_pos[1]:
        preferred_moves.append("DOWN")
    elif head_y > food_pos[1]:
        preferred_moves.append("UP")

    # Choose a move that is both preferred and safe
    for move in preferred_moves:
        if move in safe_moves:
            snake_direction = move
            break
    else:
        # No preferred safe move, pick any safe move
        if safe_moves:
            snake_direction = safe_moves[0]

    # Screen wrapping & move head
    if snake_direction == "UP":
        head_y = (head_y - 1) % ROWS
    elif snake_direction == "DOWN":
        head_y = (head_y + 1) % ROWS
    elif snake_direction == "LEFT":
        head_x = (head_x - 1) % COLS
    elif snake_direction == "RIGHT":
        head_x = (head_x + 1) % COLS

    # Insert new head position
    snake_pos.insert(0, [head_x, head_y])

    # Check for self-collision (Game Over)
    if snake_pos[0] in snake_pos[1:]:
        window.fill((0, 0, 0))
        game_over_text = font.render(f"Game Over! Final Score: {score}", True, (255, 0, 0))
        window.blit(game_over_text, (50, WINDOW_HEIGHT // 2 - 15))
        pygame.display.update()
        pygame.time.delay(3000)  # show for 3 seconds
        running = False
        continue

    # Check if snake eats food
    if snake_pos[0] == food_pos:
        score += 1  # increase score
        food_pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
    else:
        snake_pos.pop()

    # Fill window (clean, no grid)
    window.fill((0, 0, 0))

    # Draw snake
    for segment in snake_pos:
        rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(window, (0, 255, 0), rect)

    # Draw food
    food_rect = pygame.Rect(food_pos[0]*CELL_SIZE, food_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(window, food_color, food_rect)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    # Update display
    pygame.display.update()

    # Control speed
    pygame.time.delay(150)

# Quit Pygame
pygame.quit()
sys.exit()
