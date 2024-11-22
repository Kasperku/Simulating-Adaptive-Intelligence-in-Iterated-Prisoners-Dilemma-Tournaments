from typing import Optional

from bots.BaseBot import BaseBot
from strategies import DEFECT, COOPERATE


class GrimBot(BaseBot):
    """
    A bot that uses the grim strategy. Starts off cooperating, until
    opponent defects, then it defects forever
    """

    def __init__(self):
        super().__init__(name="GrimBot")
        self.cooperate = True  # grim will start off cooperating

    # returns "Cooperate" if first move, then copies opponents last move.
    def choose_action(self, opponent_last_action: Optional[str] = None) -> str:
        if opponent_last_action == DEFECT:
            self.cooperate = False
        return COOPERATE if self.cooperate else DEFECT

    def reset(self):
        self.cooperate = True
