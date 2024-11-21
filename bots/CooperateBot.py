from typing import Optional

from bots.BaseBot import BaseBot


class CooperateBot(BaseBot):
    """
    A bot that always cooperates, regardless of the opponent's actions.
    """

    def __init__(self):
        super().__init__(name="CooperateBot")

    # always returns "Cooperate" regardless of opponent_last_action
    def choose_action(self, opponent_last_action: Optional[str] = None) -> str:
        return "Cooperate"
