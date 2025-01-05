from typing import Optional

class BaseBot():
    """
    Represents a generic bot for the Prisoner's Dilemma game

    This is a base class for all bot strategies. It provides a structure for implementing
    specific strategies by defining common methods that can be overridden by subclasses
    """
    def __init__(self, name):
        self.name = name

    def get_name(self) -> str:
        return self.name

    # Determines the action (Cooperate/Defect) the bot will take in the current round.
    def choose_action(self, name, opponent_last_action: Optional[str]) -> str:
        """Defines the action the bot will take."""
        raise NotImplementedError("This method should be overridden by subclasses")

    # resets the internal state of the bot to its initial condition
    def reset(self) -> None:
        """Resets the bot's state for a new round."""
        pass
