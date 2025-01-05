from typing import Optional

from model.bots.BaseBot import BaseBot
from model.constants import DEFECT


class DefectBot(BaseBot):
    """
    A bot that always Defects, regardless of the opponent's actions
    """

    def __init__(self):
        super().__init__(name="DefectBot")

    # always returns "Defect" regardless of opponent_last_action
    def choose_action(self, name, opponent_last_action: Optional[str] = None) -> str:
        return DEFECT
