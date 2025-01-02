from typing import Dict, List, Optional
from model.bots.BaseBot import BaseBot
from model.constants import *


class MatchSimulator:
    """
    Simulates matches between two bots in a Prisoner's Dilemma tournament.
    """

    def __init__(self, turns_per_round: int = TURNS_PER_ROUND):
        """
        Initializes the match simulator with a custom or default payoff matrix.

        Args:
            turns_per_round (int): Number of turns per match. Defaults to TURNS_PER_ROUND.
        """
        self.turns_per_match = turns_per_round
        self.payoff_matrix = PAYOFF_MATRIX
        self.last_match_results: Optional[Dict[str, object]] = None

    def simulate_match(self, bot1: BaseBot, bot2: BaseBot, round_num: int) -> Dict:
        """
        Simulates a single match between two bots over a specified number of rounds.

        Args:
            bot1 (BaseBot): The first bot.
            bot2 (BaseBot): The second bot.
            round_num (int): The number of rounds to play in the match.

        Returns:
            Dict: A dictionary containing the results of the match with the following keys:
                - "rounds_played": Number of rounds played (int).
                - <bot_1_name>_actions: List of actions taken by bot_1 (List[str]).
                - <bot_2_name>_actions: List of actions taken by bot_2 (List[str]).
                - <bot_1_name>_total_payoff: Total payoff accumulated by bot_1 (float).
                - <bot_2_name>_total_payoff: Total payoff accumulated by bot_2 (float).
        """
        if round_num <= 0:
            raise ValueError("Number of rounds must be positive")

        # Set opponent names if bots support it
        if hasattr(bot1, 'set_opponent'):
            bot1.set_opponent(bot2.name)
        if hasattr(bot2, 'set_opponent'):
            bot2.set_opponent(bot1.name)

        # Initialize match data
        bot1_actions: List[str] = []
        bot2_actions: List[str] = []
        bot1_total_payoff = 0
        bot2_total_payoff = 0

        # Play turns_per_match number of turns (not round_num)
        for _ in range(self.turns_per_match):
            # Get simultaneous actions
            action1 = bot1.choose_action(bot2_actions[-1] if bot2_actions else None)
            action2 = bot2.choose_action(bot1_actions[-1] if bot1_actions else None)
            
            # Notify both bots of the results
            bot1.notify_turn_result(action1, action2, bot2.name)
            bot2.notify_turn_result(action2, action1, bot1.name)
            
            # Store actions and update payoffs
            bot1_actions.append(action1)
            bot2_actions.append(action2)
            payoffs = self.payoff_matrix[(action1, action2)]
            bot1_total_payoff += payoffs[0]
            bot2_total_payoff += payoffs[1]

        return {
            ROUND_NUM: round_num,
            f"{bot1.name}{ACTIONS_SUFFIX}": bot1_actions,
            f"{bot2.name}{ACTIONS_SUFFIX}": bot2_actions,
            f"{bot1.name}{PAYOFF_SUFFIX}": bot1_total_payoff,
            f"{bot2.name}{PAYOFF_SUFFIX}": bot2_total_payoff
        }

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
        if self.last_match_results is None:
            raise RuntimeError("No match has been simulated yet")
        return self.last_match_results
