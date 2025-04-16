"""
References

https://www.pygame.org/docs
https://github.com/baraltech/Tic-Tac-Toe
https://www.youtube.com/watch?v=IL_PMGVxEUY

"""
import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

global scoreboard 
scoreboard = {'Player 1': 0, 'Player 2': 0}

# Color Scheme
BG_COLOR = (50, 50, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)

LINE_COLOR = WHITE
CROSS_COLOR = RED
CIRCLE_COLOR = GREEN

FONT = pygame.font.SysFont(None, 60)
SMALL_FONT = pygame.font.SysFont(None, 30)

CELL_SIZE = WIDTH // 3
LINE_WIDTH = 10

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False
winner = None

# Player data
players = {"X": "Player 1", "O": "Player 2"}
game_state = "menu"  # "menu", "game", "end"

def draw_board():
    screen.fill(BG_COLOR)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_symbols():
    for row in range(3):
        for col in range(3):
            symbol = board[row][col]
            if symbol == "X":
                draw_x(row, col)
            elif symbol == "O":
                draw_o(row, col)

def draw_x(row, col):
    start_x = col * CELL_SIZE + 30
    start_y = row * CELL_SIZE + 30
    end_x = (col + 1) * CELL_SIZE - 30
    end_y = (row + 1) * CELL_SIZE - 30
    pygame.draw.line(screen, CROSS_COLOR, (start_x, start_y), (end_x, end_y), LINE_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, (start_x, end_y), (end_x, start_y), LINE_WIDTH)

def draw_o(row, col):
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CELL_SIZE // 3, LINE_WIDTH)

def check_winner():
    global game_over, winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            winner = board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            winner = board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        winner = board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        winner = board[0][2]
    if winner:
        game_over = True
        scoreboard[players[winner]] += 1
        with open("scores.txt","w") as f:
            f.write(f"{scoreboard['Player 1']}\t\t{scoreboard['Player 2']}")
    elif all(board[row][col] != "" for row in range(3) for col in range(3)):
        game_over = True
        winner = "Tie"

def reset_game():
    global board, current_player, game_over, winner
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    winner = None

def draw_winner():
    if winner == "Tie":
        text = FONT.render("It's a Tie!", True, YELLOW)
    else:
        text = FONT.render(f"{players[winner]} Wins!", True, YELLOW)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

def draw_scoreboard():
    score_text = f"{players['X']}: {scoreboard[players['X']]}  |  {players['O']}: {scoreboard[players['O']]}"
    text = SMALL_FONT.render(score_text, True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

def draw_menu():
    screen.fill(BG_COLOR)
    draw_text_center("TIC TAC TOE", FONT, YELLOW, HEIGHT // 4)
    draw_text_center("Press 1 to start game", SMALL_FONT, WHITE, HEIGHT // 2)
    draw_text_center("Press Q to quit", SMALL_FONT, WHITE, HEIGHT // 2 + 40)

def draw_text_center(text, font, color, y):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, y))

def draw_end_screen():
    screen.fill(BG_COLOR)
    draw_winner()
    draw_text_center("Press R to Restart", SMALL_FONT, WHITE, HEIGHT // 2 + 60)
    draw_text_center("Press M for Main Menu", SMALL_FONT, WHITE, HEIGHT // 2 + 100)

running = True
while running:
    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_board()
        draw_symbols()
        draw_scoreboard()
        if game_over:
            draw_winner()
    elif game_state == "end":
        draw_end_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_1:
                    game_state = "game"
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False
            elif game_state == "end":
                if event.key == pygame.K_r:
                    game_state = "game"
                    reset_game()
                elif event.key == pygame.K_m:
                    game_state = "menu"

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == "game" and not game_over:
            x, y = pygame.mouse.get_pos()
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            if row < 3 and col < 3 and board[row][col] == "":
                board[row][col] = current_player
                check_winner()
                if not game_over:
                    current_player = "O" if current_player == "X" else "X"
                else:
                    game_state = "end"

    pygame.display.flip()

pygame.quit()
