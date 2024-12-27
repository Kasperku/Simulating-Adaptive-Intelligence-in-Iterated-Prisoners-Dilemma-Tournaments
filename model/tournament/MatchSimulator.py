from typing import Dict, List, Optional
from model.bots.BaseBot import BaseBot
from model.constants import PAYOFF_MATRIX, COOPERATE


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

        # Initialize match data
        bot1_actions: List[str] = []
        bot2_actions: List[str] = []
        bot1_total_payoff = 0
        bot2_total_payoff = 0

        # Play rounds
        for _ in range(round_num):
            # Get bot decisions based on game history
            action1 = bot1.choose_action(bot2_actions[-1] if bot2_actions else COOPERATE)
            action2 = bot2.choose_action(bot1_actions[-1] if bot1_actions else COOPERATE)
            
            # Record actions
            bot1_actions.append(action1)
            bot2_actions.append(action2)
            
            # Calculate and accumulate payoffs
            payoffs = self.payoff_matrix[(action1, action2)]
            bot1_total_payoff += payoffs[0]
            bot2_total_payoff += payoffs[1]

        # Create and store match results
        self.last_match_results = {
            "rounds_played": round_num,
            f"{bot1.name}_actions": bot1_actions,
            f"{bot2.name}_actions": bot2_actions,
            f"{bot1.name}_total_payoff": bot1_total_payoff,
            f"{bot2.name}_total_payoff": bot2_total_payoff
        }
        
        return self.last_match_results

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
