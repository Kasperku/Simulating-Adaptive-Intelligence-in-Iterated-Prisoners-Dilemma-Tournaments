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

    # returns "Cooperate" if first move, then when opponent defects, it defects forever
    def choose_action(self, opponent_last_action: Optional[str] = None) -> str:
        
        # First move, opponent_last_action is None
        if opponent_last_action is None:
            return COOPERATE
        
        # Once opponent defects, switch cooperate to False and defect forever
        if opponent_last_action == DEFECT:
            self.cooperate = False
        
        result = COOPERATE if self.cooperate else DEFECT
        return result

    def reset(self):
        self.cooperate = True
