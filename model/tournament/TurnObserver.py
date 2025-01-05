from abc import ABC, abstractmethod
from typing import Optional

class TurnObserver(ABC):
    @abstractmethod
    def notify_turn_result(self, my_action: str, opponent_action: str, opponent_name: str) -> None:
        """Called after each turn to notify observers of the results"""
        pass 