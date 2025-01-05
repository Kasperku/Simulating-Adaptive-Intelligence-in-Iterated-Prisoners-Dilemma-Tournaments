from typing import Optional

from model.bots.BaseBot import BaseBot
from model.constants import COOPERATE


class TFTBot(BaseBot):
    """
    A bot that uses the tit-for-tat strategy. Starts off cooperating,
    then copies opponents last move
    """

    def __init__(self):
        super().__init__(name="TFTBot")
        self.is_first_round = True 

    # returns "Cooperate" if first move, then copies opponents last move.
    def choose_action(self,name, opponent_last_action: Optional[str]) -> str:
        if self.is_first_round:
            self.is_first_round = False
            return COOPERATE
        else:
            return opponent_last_action if opponent_last_action else COOPERATE

    def reset(self):
        self.is_first_round = True

