from typing import Optional

from bots.BaseBot import BaseBot
from strategies import DEFECT


class DefectBot(BaseBot):
    """
    A bot that always Defects, regardless of the opponent's actions.
    """

    def __init__(self):
        super().__init__(name="DefectBot")

    # always returns "Defect" regardless of opponent_last_action
    def choose_action(self, opponent_last_action: Optional[str] = None) -> str:
        return DEFECT
