import random
from typing import Optional
from model.bots.BaseBot import BaseBot
from model.constants import COOPERATE, DEFECT

class TFT90Bot(BaseBot):
    """
    A bot that uses a modified Tit-for-Tat strategy. Starts off cooperating
    then mirrors the opponent's last move, but has a 10% chance of forgiving defections.
    """

    def __init__(self):
        super().__init__(name="TFT90Bot")
        self.is_first_round = True

    def choose_action(self, name,opponent_last_action: Optional[str] = None) -> str:
        if self.is_first_round:
            self.is_first_round = False
            return COOPERATE

        if opponent_last_action == DEFECT:
            return DEFECT if random.random() < 0.9 else COOPERATE

        return COOPERATE

    def reset(self):
        self.is_first_round = True
