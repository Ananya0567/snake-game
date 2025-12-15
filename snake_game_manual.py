import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window setup
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game - Phase 2")

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

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"

    # Move snake
    head_x, head_y = snake_pos[0]

    # Screen wrapping
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

    # Check for self-collision
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
