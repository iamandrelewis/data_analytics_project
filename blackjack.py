"""
References
https://www.pygame.org/docs/
https://medium.com/nerd-for-tech/creating-blackjack-game-with-python-80a3b87b1995
https://github.com/Mozes721/BlackJack

"""
import pygame
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack Multiplayer")
clock = pygame.time.Clock()

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
    "Dealer": BLUE
}

BUTTON_DEFAULTS = {
    "hit": GREEN,
    "stand": BLUE,
    "restart": RED
}

BUTTON_HOVERS = {
    "hit": (0, 200, 0),
    "stand": (0, 0, 200),
    "restart": (200, 0, 0)
}

scoreboard = {'Player 1': 0, 'Player 2': 0}

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

def create_deck():
    values = ['Ace','2','3','4','5','6','7','8','9','10','J','Q','K']
    suits = ['Hearts','Spades','Clubs','Diamonds']
    return [f"{v} of {s}" for s in suits for v in values]

def get_card_value(card, current_total):
    if card.startswith('10'):
        return 10
    first = card.split()[0]
    if first in ['J', 'Q', 'K']:
        return 10
    elif first == 'Ace':
        return 11 if current_total + 11 <= 21 else 1
    else:
        return int(first)

def draw_text(text, x, y, font, color=WHITE):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_button(rect, color, text, hover_color=None):
    mouse_pos = pygame.mouse.get_pos()
    current_color = hover_color if hover_color and rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, current_color, rect)
    draw_text(text, rect.x + 10, rect.y + 10, small_font, BLACK)

btn_hit = pygame.Rect(600, 450, 120, 40)
btn_stand = pygame.Rect(600, 500, 120, 40)
btn_restart = pygame.Rect(600, 550, 120, 40)

def init_game():
    deck = create_deck()
    random.shuffle(deck)
    player1 = [deck.pop(), deck.pop()]
    player2 = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    return {
        "deck": deck,
        "players": [
            {"name": "Player 1", "cards": player1, "total": sum(get_card_value(c, 0) for c in player1), "stand": False, "bust": False},
            {"name": "Player 2", "cards": player2, "total": sum(get_card_value(c, 0) for c in player2), "stand": False, "bust": False}
        ],
        "dealer": {"cards": dealer, "total": sum(get_card_value(c, 0) for c in dealer)},
        "current_player": 0,
        "game_over": False,
        "message": ""
    }

game = init_game()
running = True

while running:
    screen.fill(BG_COLOR)
    draw_text("BLACKJACK - Multiplayer", 20, 20, font, YELLOW)

    for i, player in enumerate(game["players"]):
        y_offset = 60 + i * 180
        draw_text(f"{player['name']} Cards:", 50, y_offset, font, PLAYER_COLORS[player['name']])
        for j, card in enumerate(player["cards"]):
            draw_text(card, 70, y_offset + 40 + j * 25, small_font)
        draw_text(f"Total: {player['total']}", 50, y_offset + 120, small_font, WHITE)

    draw_text("Dealer Cards:", 450, 60, font, PLAYER_COLORS["Dealer"])
    dealer_cards = game["dealer"]["cards"] if game["game_over"] else [game["dealer"]["cards"][0], "Hidden"]
    for j, card in enumerate(dealer_cards):
        draw_text(str(card), 470, 100 + j * 25, small_font, WHITE)
    if game["game_over"]:
        draw_text(f"Dealer Total: {game['dealer']['total']}", 450, 180, small_font, WHITE)

    draw_text(game["message"], 50, 500, font, YELLOW)
    current_player = game["players"][game["current_player"]]

    draw_button(btn_hit, BUTTON_DEFAULTS["hit"], "Hit", BUTTON_HOVERS["hit"])
    draw_button(btn_stand, BUTTON_DEFAULTS["stand"], "Stand", BUTTON_HOVERS["stand"])
    draw_button(btn_restart, BUTTON_DEFAULTS["restart"], "Restart", BUTTON_HOVERS["restart"])

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn_restart.collidepoint(event.pos):
                game = init_game()

            if not game["game_over"]:
                if btn_hit.collidepoint(event.pos) and not current_player["stand"]:
                    card = game["deck"].pop()
                    current_player["cards"].append(card)
                    current_player["total"] += get_card_value(card, current_player["total"])
                    if current_player["total"] > 21:
                        current_player["bust"] = True
                        current_player["stand"] = True

                if btn_stand.collidepoint(event.pos):
                    current_player["stand"] = True

                if current_player["stand"] or current_player["bust"]:
                    if game["current_player"] < len(game["players"]) - 1:
                        game["current_player"] += 1
                    else:
                        while game["dealer"]["total"] < 17:
                            card = game["deck"].pop()
                            game["dealer"]["cards"].append(card)
                            game["dealer"]["total"] += get_card_value(card, game["dealer"]["total"])

                        message = ""
                        dealer_total = game["dealer"]["total"]
                        for player in game["players"]:
                            if player["bust"]:
                                result = "busted"
                            elif dealer_total > 21 or player["total"] > dealer_total:
                                result = "wins"
                                scoreboard[player['name']] += 1
                                with open("scores.txt","w") as f:
                                    f.write(f"{scoreboard['Player 1']}\t\t{scoreboard['Player 2']}")


                            elif player["total"] < dealer_total:
                                result = "loses"
                            else:
                                result = "ties"
                            message += f"{player['name']} {result}.  "
                        game["message"] = message.strip()
                        game["game_over"] = True

    clock.tick(30)

pygame.quit()
