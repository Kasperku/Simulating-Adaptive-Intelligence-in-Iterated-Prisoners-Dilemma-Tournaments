from typing import Optional

from bots.BaseBot import BaseBot


class TFTBot(BaseBot):
    """
    A bot that uses the tit-for-tat strategy. Starts off cooperating,
    then copies opponents last move.
    """

    def __init__(self):
        super().__init__(name="TFTBot")
        self.is_first_round = True # check whether it is the start of a round

    # returns "Cooperate" if first move, then copies opponents last move.
    def choose_action(self, opponent_last_action: Optional[str] = None) -> str:
        if self.is_first_round:
            self.is_first_round = False
            return "Cooperate"
        else:
            return opponent_last_action

    def reset(self):
        self.is_first_round = True
