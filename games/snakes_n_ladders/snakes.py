"""
References
https://www.pygame.org/docs/
https://github.com/manan-d8/snakes-and-ladders-pygame
https://medium.com/@codeitup1234/building-a-snake-and-ladder-game-in-python-a-step-by-step-guide-683947e32bbf
https://www.youtube.com/watch?v=fv8mgvsuSKY&t=3s
"""
import pygame
import random
from player import Player
from dice import Dice
from board import draw_board, check_snake_or_ladder
from analytics import calculate_analytics
from utils import draw_text

# Color Scheme
BG_COLOR = (50, 50, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)

PLAYER_COLORS = {
    "Player 1": RED,
    "Player 2": GREEN,
    "Player 3": BLUE,
    "Player 4": YELLOW
}

BUTTON_DEFAULTS = {
    "roll": GREEN,
    "start": BLUE,
    "exit": RED
}

BUTTON_HOVERS = {
    "roll": (0, 200, 0),
    "start": (0, 0, 200),
    "exit": (200, 0, 0)
}

global scoreboard 
scoreboard = {'Player 1': 0, 'Player 2': 0}

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snakes and Ladders")
font = pygame.font.SysFont(None, 24)
large_font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Load dice images
dice_images = [pygame.image.load(f"assets/dice_{i}.png") for i in range(1, 7)]

# Initialize players and dice
def init_game():
    return [
        Player("Player 1", PLAYER_COLORS["Player 1"]),
        Player("Player 2", PLAYER_COLORS["Player 2"])
    ], Dice(), 0, None, False

players, dice, current_player_index, winner, show_win_screen = init_game()

# Button setup
button_roll = pygame.Rect(450, 500, 120, 40)
button_restart = pygame.Rect(450, 550, 120, 40)
button_main_menu = pygame.Rect(200, 400, 200, 50)

def animate_dice_roll():
    for _ in range(10):
        val = random.randint(1, 6)
        screen.blit(dice_images[val - 1], (470, 420))
        pygame.display.flip()
        pygame.time.wait(100)
    return val
active = True
while active:
    
    screen.fill(BG_COLOR)

    if show_win_screen:
        draw_text(screen, f"{winner} Wins!", 180, 200, large_font, YELLOW)
        pygame.draw.rect(screen, BUTTON_DEFAULTS["start"], button_main_menu)
        draw_text(screen, "Play Again", 240, 415, font, WHITE)

        draw_text(screen, "Scoreboard:", 230, 280, font, WHITE)
        draw_text(screen, f"Player 1: {scoreboard['Player 1']}", 230, 300, font, PLAYER_COLORS["Player 1"])
        draw_text(screen, f"Player 2: {scoreboard['Player 2']}", 230, 320, font, PLAYER_COLORS["Player 2"])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_main_menu.collidepoint(event.pos):
                    players, dice, current_player_index, winner, show_win_screen = init_game()
        continue

    draw_board(screen, font)

    pygame.draw.rect(screen, BUTTON_DEFAULTS["roll"], button_roll)
    draw_text(screen, "Roll Dice", 470, 510, font, BLACK)

    pygame.draw.rect(screen, BUTTON_DEFAULTS["exit"], button_restart)
    draw_text(screen, "Restart", 470, 560, font, WHITE)

    for i, player in enumerate(players):
        draw_text(screen, f"{player.name} Position: {player.position}", 10, 560 + i * 20, font, PLAYER_COLORS[player.name])

    draw_text(screen, f"{players[current_player_index].name}'s Turn", 10, 20, font, YELLOW)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False 

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_roll.collidepoint(event.pos) and not winner:
                current_player = players[current_player_index]
                rolled_value = animate_dice_roll()
                dice.history.append(rolled_value)
                current_player.move(rolled_value)
                current_player.position, _ = check_snake_or_ladder(current_player.position)

                if current_player.position == 100:
                                
                    with open("./main/scores.txt","r") as f:
                        players = f.read().split('\t')

                    scores = list()
                    for items in players:
                        try:
                            scores.append(int(items))
                        except:
                            continue
                    if len(scores) > 0:
                        player1 = scores[0]
                        player2 = scores[1]
                        scoreboard["Player 1"] = player1
                        scoreboard["Player 2"] = player2

                    winner = current_player.name
                    
                    scoreboard[winner] += 1
                    with open("./main/scores.txt","w") as f:
                        f.write(f"{scoreboard['Player 1']}\t\t{scoreboard['Player 2']}")
                    show_win_screen = True

                current_player_index = (current_player_index + 1) % len(players)

            if button_restart.collidepoint(event.pos):
                players, dice, current_player_index, winner, show_win_screen = init_game()

    tile_size = 60
    for i, player in enumerate(players):
        row = 9 - (player.position - 1) // 10
        col = (player.position - 1) % 10 if (row % 2 == 0) else 9 - (player.position - 1) % 10
        x = col * tile_size + 20 + i * 5
        y = row * tile_size + 20
        pygame.draw.circle(screen, player.color, (x, y), 10)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

stats = calculate_analytics(dice.history)
print("\nDice Roll Analytics:")
for k, v in stats.items():
    print(f"{k.capitalize()}: {v}")
