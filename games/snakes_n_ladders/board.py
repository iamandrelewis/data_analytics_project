import pygame
from pygame import image

# Define snakes and ladders positions
snakes = {16: 6, 49: 11, 62: 19, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Load the images for snakes and ladders
snake_img = pygame.image.load("assets/snake.png")
ladder_img = pygame.image.load("assets/ladder.png")

def check_snake_or_ladder(pos):
    """Check if current position has a snake or ladder."""
    if pos in snakes:
        return snakes[pos], "snake"
    elif pos in ladders:
        return ladders[pos], "ladder"
    return pos, None

def draw_board(screen, font):
    """Draws the grid for the Snakes and Ladders game."""
    tile_size = 60
    for row in range(10):
        for col in range(10):
            x = col * tile_size
            y = row * tile_size
            pygame.draw.rect(screen, (255, 255, 255), (x, y, tile_size, tile_size), 1)
            number = 100 - (row * 10 + col) if row % 2 == 0 else 91 - (row * 10) + col
            text = font.render(str(number), True, (0, 0, 0))
            screen.blit(text, (x + 5, y + 5))

    # Draw snakes and ladders images
    for position, new_position in snakes.items():
        row = 9 - (position - 1) // 10
        col = (position - 1) % 10 if (row % 2 == 0) else 9 - (position - 1) % 10
        x = col * tile_size + 20
        y = row * tile_size + 20
        screen.blit(snake_img, (x, y))

    for position, new_position in ladders.items():
        row = 9 - (position - 1) // 10
        col = (position - 1) % 10 if (row % 2 == 0) else 9 - (position - 1) % 10
        x = col * tile_size + 20
        y = row * tile_size + 20
        screen.blit(ladder_img, (x, y))

