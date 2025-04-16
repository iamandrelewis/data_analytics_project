
import pygame
import sys
from statistics import mean, median, mode

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scoreboard Stats")

# Color Scheme
BG_COLOR = (50, 50, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)

# Fonts
TITLE_FONT = pygame.font.SysFont(None, 48)
STAT_FONT = pygame.font.SysFont(None, 30)
SMALL_FONT = pygame.font.SysFont(None, 24)

# Sample score data
player_scores = {
    "Player 1": 0,
    "Player 2": 0,
}

def calculate_stats(score):
    """

    Calculates mode, mean, median, min, and max from a list of scores.

    Parameters:
        scores (list): A list of numerical scores.

    Returns:
        dict: A dictionary containing calculated statistics.
    """
    with open("scores.txt","r") as f:
        player1, player2 = f.read().split('\t')

    player1 = int(player1)
    player2 = int(player2)

    scores = list()
    scores.append(player1)
    try:
        return {
            "mean": round(mean(scores), 2),
            "median": median(scores),
            "mode": mode(scores),
            "min": min(scores),
            "max": max(scores)
        }
    except Exception as e:
        return {"error": str(e)}

def draw_text_center(text, y, font, color):
    """
    Draws centered text horizontally at a given y-coordinate.

    Parameters:
        text (str): The text to render.
        y (int): Vertical position on the screen.
        font (pygame.font.Font): Font object to use.
        color (tuple): RGB color.
    """
    render = font.render(text, True, color)
    screen.blit(render, (WIDTH // 2 - render.get_width() // 2, y))

def draw_scoreboard():
    """
    Renders the scoreboard statistics for each player.
    """
    screen.fill(BG_COLOR)
    draw_text_center("Scoreboard Statistics", 20, TITLE_FONT, YELLOW)

    y_offset = 80
    for player, scores in player_scores.items():
        stats = calculate_stats(scores)
        draw_text_center(f"{player} Scores: {scores}", y_offset, SMALL_FONT, GREEN if '1' in player else RED)
        y_offset += 30
        if 'error' not in stats:
            for key, value in stats.items():
                draw_text_center(f"{key.capitalize()}: {value}", y_offset, STAT_FONT, WHITE)
                y_offset += 25
        else:
            draw_text_center(f"Error: {stats['error']}", y_offset, STAT_FONT, RED)
            y_offset += 25
        y_offset += 20

def main():
    running = True
    while running:
        
        draw_scoreboard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()