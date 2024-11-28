"""
    Represents a generic bot for the Prisoner's Dilemma game.

    This is a base class for all bot strategies. It provides a structure for implementing
    specific strategies by defining common methods that can be overridden by subclasses.
"""
from typing import Optional

class BaseBot:
    def __init__(self, name):
        self.name = name

    # Determines the action (Cooperate/Defect) the bot will take in the current round.
    def choose_action(self, opponent_last_action: Optional[str]=None):
        """Defines the action the bot will take."""
        raise NotImplementedError("This method should be overridden by subclasses")

    # resets the internal state of the bot to its initial condition
    def reset(self):
        """Resets the bot's state for a new round."""
        pass
