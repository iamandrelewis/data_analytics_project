
import pygame
import subprocess
import sys

# Initialize Pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Group #3 Arcade: Data Analytics Project: Main Menu")

# Color Scheme
BG_COLOR = (50, 50, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
DARK_GREEN = (0, 200, 0)
DARK_BLUE = (0, 0, 200)
DARK_RED = (200, 0, 0)
GRAY = (180, 180, 180)

# Fonts
TITLE_FONT = pygame.font.SysFont(None, 60)
BTN_FONT = pygame.font.SysFont(None, 36)

# Buttons
btn_ttt = pygame.Rect(200, 100, 250, 50)
btn_blackjack = pygame.Rect(200, 170, 250, 50)
btn_snakes = pygame.Rect(200, 240, 250, 50)
btn_quit = pygame.Rect(200, 380, 250, 50)
btn_dice = pygame.Rect(200, 310,250,50 )
btn_score = pygame.Rect(200, 510,250,50 )

def draw_button(rect, text, color, hover_color):
    """Draws an interactive button."""
    mouse_pos = pygame.mouse.get_pos()
    current_color = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, current_color, rect)
    label = BTN_FONT.render(text, True, BLACK)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + 10))

def run_game(script_name):
    """Launches a game script."""
    try:
        subprocess.run([sys.executable, script_name])
    except Exception as e:
        print(f"Failed to launch {script_name}: {e}")

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)

    # Title
    title_text = TITLE_FONT.render("Group #3 Arcade", True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))

    # Draw Buttons
    draw_button(btn_ttt, "Tic Tac Toe", GREEN, DARK_GREEN)
    draw_button(btn_blackjack, "Blackjack", BLUE, DARK_BLUE)
    draw_button(btn_snakes, "Snakes & Ladders", RED, DARK_RED)
    draw_button(btn_dice,"Dice Game",WHITE,GRAY)
    draw_button(btn_score,"View Scoreboard",YELLOW,WHITE)
    draw_button(btn_quit, "Quit", WHITE, BLACK)


    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn_ttt.collidepoint(event.pos):
                run_game("./games/tic_tac_toe_game.py")
            elif btn_blackjack.collidepoint(event.pos):
                run_game("./games/blackjack.py")
            elif btn_snakes.collidepoint(event.pos):
                run_game("./games/snakes_n_ladders/snakes.py")
            elif btn_quit.collidepoint(event.pos):
                with open("./main/scores.txt","w") as f:
                    f.write(" ")
                running = False
            elif btn_dice.collidepoint(event.pos):
                run_game("./games/dice_game.py")
            elif btn_score.collidepoint(event.pos):
                run_game("./main/scoreboard.py")

    pygame.display.flip()

pygame.quit()
