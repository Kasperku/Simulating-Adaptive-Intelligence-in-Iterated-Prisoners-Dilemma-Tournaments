from typing import Optional

from model.bots.BaseBot import BaseBot
from model.constants import DEFECT, COOPERATE


class GrimBot(BaseBot):
    """
    A bot that uses the grim strategy. Starts off cooperating, until
    opponent defects, then it defects forever
    """

    def __init__(self):
        super().__init__(name="GrimBot")
        self.cooperate = True  # grim will start off cooperating

    def choose_action(self, opponent_last_action: Optional[str] = None) -> str:

        if not self.cooperate:
            return DEFECT
        
        if opponent_last_action == DEFECT:
            self.cooperate = False
            return DEFECT
        
        return COOPERATE

    def reset(self):
        self.cooperate = True
