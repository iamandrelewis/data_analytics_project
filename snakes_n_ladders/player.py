
class Player:
    """Class representing a player in the game."""

    def __init__(self, name, color):
        self.name = name
        self.position = 1
        self.color = color

    def move(self, steps):
        """Move the player by a number of steps."""
        self.position += steps
        if self.position > 100:
            self.position = 100
