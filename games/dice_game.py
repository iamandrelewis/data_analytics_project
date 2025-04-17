"""
References
https://www.pygame.org/docs/
https://www.youtube.com/watch?v=x-Ag2_bJ40Y
https://stackoverflow.com/questions/66731019/whats-difference-between-get-rect-and-pygame-rect/66731068#66731068

"""
import pygame
import random
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (50, 50, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
FONT_SIZE = 24
DICE_SIZE = 80
DICE_COLOR = WHITE
DOT_COLOR = BLACK
PLAYER_COLORS = [RED, GREEN, BLUE, YELLOW]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiplayer Dice Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Arial', FONT_SIZE)
title_font = pygame.font.SysFont('Arial', FONT_SIZE * 2)
button_font = pygame.font.SysFont('Arial', FONT_SIZE)

global scoreboard
scoreboard = {'Player 1': 0, 'Player 2': 0}

class Button:
    """A class to create interactive buttons in Pygame.
    
    Attributes:
        rect (pygame.Rect): The rectangular area of the button
        text (str): The text displayed on the button
        color (tuple): The button's normal color (RGB)
        hover_color (tuple): The button's color when hovered (RGB)
        is_hovered (bool): Whether the mouse is currently over the button
    """
    
    def __init__(self, x, y, width, height, text, color, hover_color):
        """Initialize the Button object.
        
        Args:
            x (int): X-coordinate of the button's top-left corner
            y (int): Y-coordinate of the button's top-left corner
            width (int): Width of the button in pixels
            height (int): Height of the button in pixels
            text (str): Text to display on the button
            color (tuple): Normal color of the button (RGB)
            hover_color (tuple): Color when mouse hovers over button (RGB)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        """Draw the button on the specified surface.
        
        Args:
            surface (pygame.Surface): The surface to draw the button on
        """
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        """Check if the mouse is hovering over the button.
        
        Args:
            pos (tuple): The current mouse position (x, y)
            
        Returns:
            bool: True if mouse is over the button, False otherwise
        """
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        """Check if the button was clicked.
        
        Args:
            pos (tuple): The current mouse position (x, y)
            event (pygame.Event): The event to check for mouse click
            
        Returns:
            bool: True if button was clicked, False otherwise
        """
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

def draw_dice(surface, value, x, y, size=80, color=WHITE, dot_color=BLACK):
    """Draw a dice with the given value at the specified position.
    
    Args:
        surface (pygame.Surface): The surface to draw on
        value (int): The dice value (1-6)
        x (int): X-coordinate of the dice's top-left corner
        y (int): Y-coordinate of the dice's top-left corner
        size (int, optional): Size of the dice in pixels. Defaults to 80.
        color (tuple, optional): Color of the dice. Defaults to WHITE.
        dot_color (tuple, optional): Color of the dots. Defaults to BLACK.
    """
    # Dice body
    dice_rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surface, color, dice_rect, border_radius=size//10)
    pygame.draw.rect(surface, BLACK, dice_rect, 2, border_radius=size//10)
    
    # Calculate dot positions
    center = size // 2
    offset = size // 4
    dot_radius = size // 10
    
    positions = {
        1: [(center, center)],
        2: [(offset, offset), (size - offset, size - offset)],
        3: [(offset, offset), (center, center), (size - offset, size - offset)],
        4: [(offset, offset), (offset, size - offset), 
            (size - offset, offset), (size - offset, size - offset)],
        5: [(offset, offset), (offset, size - offset), 
            (center, center), 
            (size - offset, offset), (size - offset, size - offset)],
        6: [(offset, offset), (offset, center), (offset, size - offset),
            (size - offset, offset), (size - offset, center), (size - offset, size - offset)]
    }
    
    # Draw dots
    for pos in positions[value]:
        pygame.draw.circle(surface, dot_color, (x + pos[0], y + pos[1]), dot_radius)

def roll_dice(num_of_dice):
    """Generate random dice rolls.
    
    Args:
        num_of_dice (int): Number of dice to roll
        
    Returns:
        list: List of integers representing dice values (1-6)
    """
    return [random.randint(1, 6) for _ in range(num_of_dice)]

def draw_text(surface, text, pos, color=WHITE, font=font, center=False):
    """Draw text on a surface at the specified position.
    
    Args:
        surface (pygame.Surface): The surface to draw on
        text (str): The text to display
        pos (tuple): (x, y) coordinates for text position
        color (tuple, optional): Text color. Defaults to WHITE.
        font (pygame.font.Font, optional): Font to use. Defaults to global font.
        center (bool, optional): Whether to center the text at pos. Defaults to False.
        
    Returns:
        pygame.Rect: The rectangular area of the rendered text
    """
    text_surf = font.render(text, True, color)
    if center:
        text_rect = text_surf.get_rect(center=pos)
    else:
        text_rect = text_surf.get_rect(topleft=pos)
    surface.blit(text_surf, text_rect)
    return text_rect

def player_setup_screen():
    """Display the player setup screen and collect player names.
    
    This screen allows users to:
    - Start the game when ready
    
    Returns:
        list: List of player names entered by the user
    """
    players = ['Player 1', 'Player 2']
    active = False
    input_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 40)
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('gray15')
    color = color_inactive
    
    done_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 120, 200, 40, "Start Game", BLUE, (0, 0, 200))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
                    
                if done_button.is_clicked(mouse_pos, event) and len(players) >= 2:
                    return players
                    
        
        screen.fill(BG_COLOR)
        draw_text(screen, "Multiplayer Dice Game", (SCREEN_WIDTH//2, 100), WHITE, title_font, True)
                
        # Draw player list
        if players:
            draw_text(screen, "Players:", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 80))
            for i, player in enumerate(players):
                draw_text(screen, f"{i+1}. {player}", (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 40 + i * 30), PLAYER_COLORS[i])
        
        # Update buttons
        done_button.check_hover(mouse_pos)
        
        # Draw buttons
        done_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(30)

def dice_selection_screen(round_num):
    """Display the dice selection screen for each round.
    
    Args:
        round_num (int): The current round number (1-6)
        
    Returns:
        int: The number of dice selected for this round (1-5)
    """
    num_dice = 1
    roll_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50, "Roll Dice!", GREEN, (0, 200, 0))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if roll_button.is_clicked(mouse_pos, event):
                    return num_dice
                    
            if event.type == KEYDOWN:
                if event.key == K_UP and num_dice < 5:
                    num_dice += 1
                elif event.key == K_DOWN and num_dice > 1:
                    num_dice -= 1
                elif event.key == K_RETURN:
                    return num_dice
        
        screen.fill(BG_COLOR)
        draw_text(screen, f"Round {round_num}", (SCREEN_WIDTH//2, 100), WHITE, title_font, True)
        draw_text(screen, "Select number of dice to roll (1-5)", (SCREEN_WIDTH//2, 180), WHITE, font, True)
        
        # Draw dice number
        draw_text(screen, str(num_dice), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), WHITE, pygame.font.SysFont('Arial', 72), True)
        
        # Draw dice preview
        for i in range(num_dice):
            draw_dice(screen, random.randint(1, 6), SCREEN_WIDTH//2 - (num_dice * DICE_SIZE)//2 + i * DICE_SIZE, 
                     SCREEN_HEIGHT//2 + 50, DICE_SIZE//2)
        
        # Draw instructions
        draw_text(screen, "Use UP/DOWN arrows to change", (SCREEN_WIDTH//2, SCREEN_HEIGHT - 150), WHITE, font, True)
        draw_text(screen, "Press ENTER or click Roll Dice to continue", (SCREEN_WIDTH//2, SCREEN_HEIGHT - 120), WHITE, font, True)
        
        # Update and draw button
        roll_button.check_hover(mouse_pos)
        roll_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(30)

def show_round_results(players, round_num, num_dice, round_totals, round_winners):
    """Display the results of a completed round.
    
    Args:
        players (list): List of player names
        round_num (int): The current round number (1-6)
        num_dice (int): Number of dice rolled this round
        round_totals (dict): Dictionary mapping players to their round totals
        round_winners (list): List of players who won this round
    """
    continue_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Continue", BLUE, (0, 0, 200))
    
    # Calculate positions for dice
    dice_start_x = SCREEN_WIDTH // 2 - (num_dice * DICE_SIZE) // 2
    player_dice_y = SCREEN_HEIGHT // 3
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if continue_button.is_clicked(mouse_pos, event):
                    return
                    
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
        
        screen.fill(BG_COLOR)
        draw_text(screen, f"Round {round_num} Results", (SCREEN_WIDTH//2, 50), WHITE, title_font, True)
        
        # Draw each player's dice and total
        for player in players:
            player_color = PLAYER_COLORS[players.index(player)]
            y_pos = player_dice_y + players.index(player) * (DICE_SIZE + 60)
            
            # Draw player name and total
            draw_text(screen, f"{player}: {round_totals[player]}", (100, y_pos + DICE_SIZE//2 - 10), player_color)
            
            # Draw dice
            for j in range(num_dice):
                draw_dice(screen, random.randint(1, 6), dice_start_x + j * DICE_SIZE, y_pos)
        
        # Draw round winner(s)
        if len(round_winners) == 1:
            winner_text = f"{round_winners[0]} wins the round!"
            winner_color = PLAYER_COLORS[players.index(round_winners[0])]
        else:
            winner_text = f"Tie between {', '.join(round_winners)}!"
            winner_color = WHITE
            
        draw_text(screen, winner_text, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 150), winner_color, font, True)
        
        # Draw continue button
        continue_button.check_hover(mouse_pos)
        continue_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(30)


def show_final_results(players, scores):
    """Display the final results after all rounds are completed.
    
    Args:
        players (list): List of player names
        scores (dict): Dictionary mapping players to their total wins
        
    Returns:
        bool: True if players want to play again, False to quit
    """
    max_score = max(scores.values())
    final_winners = [p for p, score in scores.items() if score == max_score]
    
    play_again_button = Button(SCREEN_WIDTH//2 - 220, SCREEN_HEIGHT - 100, 200, 50, "Play Again", GREEN, (0, 200, 0))
    quit_button = Button(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 100, 200, 50, "Quit", RED, (200, 0, 0))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if play_again_button.is_clicked(mouse_pos, event):
                    return True
                if quit_button.is_clicked(mouse_pos, event):
                    return False
        
        screen.fill(BG_COLOR)
        draw_text(screen, "Game Over - Final Results", (SCREEN_WIDTH//2, 50), WHITE, title_font, True)
        
        # Draw scores
        for i, (player, score) in enumerate(scores.items()):
            player_color = PLAYER_COLORS[i]
            y_pos = 150 + i * 50
            is_winner = player in final_winners
            
            # Highlight winners
            text_color = YELLOW if is_winner else player_color
            text_size = FONT_SIZE + 10 if is_winner else FONT_SIZE
            text_font = pygame.font.SysFont('Arial', text_size)
            
            draw_text(screen, f"{player}: {score} wins", (SCREEN_WIDTH//2, y_pos), text_color, text_font, True)
        
        # Draw champion announcement
        if len(final_winners) == 1:
            winner_text = f"{final_winners[0]} is the champion!"
            winner_color = PLAYER_COLORS[players.index(final_winners[0])]
        else:
            winner_text = f"Tie between {', '.join(final_winners)}!"
            winner_color = YELLOW
            
        draw_text(screen, winner_text, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 180), winner_color, title_font, True)
        
        # Draw buttons
        play_again_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        play_again_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(30)

def main_game_loop(players):
    """Run the main game loop with all rounds.
    
    Args:
        players (list): List of player names
        
    Returns:
        bool: True if players want to play again, False to quit
    """
    scores = {player: 0 for player in players}
    round_num = 1
    
    while round_num <= 6:
        # Select number of dice for this round
        num_dice = dice_selection_screen(round_num)
        
        # Each player rolls the dice
        round_totals = {}
        for player in players:
            dice_values = roll_dice(num_dice)
            round_totals[player] = sum(dice_values)
        
        # Determine round winner(s)
        max_score = max(round_totals.values())
        round_winners = [p for p, score in round_totals.items() if score == max_score]
        
        # Update scores
        for winner in round_winners:
                
            with open("./main/scores.txt","r") as f:
                x = f.read().split('\t')

            scores = list()
            for items in x:
                try:
                    scores.append(int(items))
                except:
                    continue
            if len(scores) > 0:
                player1 = scores[0]
                player2 = scores[1]
                scoreboard["Player 1"] = player1
                scoreboard["Player 2"] = player2
                
            scoreboard[winner] += 1
            scores[winner] += 1
            with open("./main/scores.txt","w") as f:
                f.write(f"{scoreboard['Player 1']}\t\t{scoreboard['Player 2']}")
        
        # Show round results
        show_round_results(players, round_num, num_dice, round_totals, round_winners)
        
        round_num += 1
    
    # Show final results
    return show_final_results(players, scores)

def main():
    """Main function to initialize and run the game.
    
    Handles the game lifecycle including:
    - Player setup
    - Running game rounds
    - Restarting or quitting
    """
    while True:
        # Player setup
        players = player_setup_screen()
        
        # Run the game
        play_again = main_game_loop(players)
        
        if not play_again:
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()