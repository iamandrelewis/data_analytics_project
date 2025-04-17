import pygame

def draw_text(screen, text, x, y, font, color=(0, 0, 0)):
    """Utility function to draw text on screen."""
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))
