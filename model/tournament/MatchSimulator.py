from typing import Dict, List
from model.bots.BaseBot import BaseBot
from model.constants import PAYOFF_MATRIX


class MatchSimulator:
    """
    Simulates matches between two bots in a Prisoner's Dilemma tournament.
    """

    def __init__(self, payoff_matrix: Dict[tuple, tuple] = PAYOFF_MATRIX):
        """
        Initializes the match simulator with a custom or default payoff matrix.

        Args:
            payoff_matrix (Dict[tuple, tuple]): A custom payoff matrix. Defaults to the standard Prisoner's Dilemma payoffs.
        """
        self.payoff_matrix = payoff_matrix

    def simulate_match(self, bot_1: BaseBot, bot_2: BaseBot, rounds: int) -> Dict:
        """
        Simulates a single match between two bots over a specified number of rounds.

        Args:
            bot_1 (BaseBot): The first bot.
            bot_2 (BaseBot): The second bot.
            rounds (int): The number of rounds to play in the match.

        Returns:
            Dict: A dictionary containing the results of the match with the following keys:
                - "rounds_played": Number of rounds played (int).
                - <bot_1_name>_actions: List of actions taken by bot_1 (List[str]).
                - <bot_2_name>_actions: List of actions taken by bot_2 (List[str]).
                - <bot_1_name>_total_payoff: Total payoff accumulated by bot_1 (float).
                - <bot_2_name>_total_payoff: Total payoff accumulated by bot_2 (float).
        """
        pass

    def get_match_results(self) -> Dict:
        """
            Retrieves the results of the last simulated match.

            Returns:
                Dict: A dictionary containing the match results with the following keys:
                    - "rounds_played": Number of rounds played (int).
                    - <bot_1_name>_actions: List of actions taken by bot_1 (List[str]).
                    - <bot_2_name>_actions: List of actions taken by bot_2 (List[str]).
                    - <bot_1_name>_total_payoff: Total payoff accumulated by bot_1 (float).
                    - <bot_2_name>_total_payoff: Total payoff accumulated by bot_2 (float).
            """
        pass
