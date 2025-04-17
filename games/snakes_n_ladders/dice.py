
import random

class Dice:
    """Class for rolling a dice and storing roll history."""

    def __init__(self):
        self.history = []

    def roll(self):
        """Simulate rolling a 6-sided dice."""
        try:
            value = random.randint(1, 6)
            self.history.append(value)
            return value
        except Exception as e:
            print(f"Error rolling dice: {e}")
            return 1
