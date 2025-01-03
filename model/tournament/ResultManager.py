from typing import List, Dict
from model.constants import *


class ResultManager:
    """
    Manages and analyzes results from matches in a Prisoner's Dilemma tournament.
    """
    results: List[Dict] = []

    def __init__(self):
        """
        Initializes the ResultManager with an empty results list.
        """
        self.results: List[Dict] = []
        self.bots_statistics: Dict[str, Dict] = {}

    def record_result(self, result: Dict):
        """
        Adds a single match result to the results list.

        Args:
            result (Dict): A dictionary representing the match result.
                Must contain round_number and for each bot: ACTIONS and PAYOFF_SUFFIX

        Raises:
            KeyError: If the result format is invalid
        """
        # Validate required fields
        if ROUND_NUM not in result:
            raise KeyError("Result must contain round_number")

        # Find bot names by looking for '_actions' suffix
        bot_names = {key.split('_')[0] for key in result.keys() if key.endswith(ACTIONS_SUFFIX)}
        
        # Validate that each bot has both actions and total_payoff
        for bot_name in bot_names:
            if f"{bot_name}{PAYOFF_SUFFIX}" not in result:
                raise KeyError(f"Missing total_payoff for bot {bot_name}")
            if f"{bot_name}{ACTIONS_SUFFIX}" not in result:
                raise KeyError(f"Missing actions for bot {bot_name}")

        # If we get here, the format is valid
        self.results.append(result)

    def get_all_results(self) -> List[Dict]:
        """
        Retrieves all recorded results. (round by round details)

        Returns:
            List[Dict]: A list of dictionaries representing all match results.
        """
        return self.results

    def get_aggregate_results(self) -> Dict:
        """
        Aggregates total payoffs and actions for each bot across all matches

        Returns:
            Dict: A dictionary where each key is a bot's name and the value is a dictionary
                  with aggregate statistics (PAYOFF, MATCHES_PLAYED, COOPERATE_COUNT, DEFECT_COUNT).
        """
        aggregate_stats = {}

        for result in self.results:
            # Extract bot names from the result
            bot_names = {key.split('_')[0] for key in result.keys() 
                        if key.endswith(ACTIONS_SUFFIX) or key.endswith(TOTAL_PAYOFF)}

            for bot_name in bot_names:
                if bot_name not in aggregate_stats:
                    aggregate_stats[bot_name] = {
                        TOTAL_PAYOFF: 0,
                        MATCHES_PLAYED: 0,
                        COOPERATE_COUNT: 0,
                        DEFECT_COUNT: 0
                    }

                self._update_payoff_and_matches(aggregate_stats, bot_name, result)
                self._count_actions(aggregate_stats, bot_name, result)

        return aggregate_stats

    def _update_payoff_and_matches(self, aggregate_stats: Dict, bot_name: str, result: Dict):
        """Helper method to update payoff and match count statistics"""
        aggregate_stats[bot_name][TOTAL_PAYOFF] = aggregate_stats[bot_name][TOTAL_PAYOFF] + result[f"{bot_name}{PAYOFF_SUFFIX}"]
        aggregate_stats[bot_name][MATCHES_PLAYED] += 1

    def _count_actions(self, aggregate_stats: Dict, bot_name: str, result: Dict):
        """Helper method to count cooperate and defect actions"""
        actions = result[f"{bot_name}{ACTIONS_SUFFIX}"]
        cooperate_count = actions.count(COOPERATE)
        defect_count = actions.count(DEFECT)
        aggregate_stats[bot_name][COOPERATE_COUNT] += cooperate_count
        aggregate_stats[bot_name][DEFECT_COUNT] += defect_count

        return aggregate_stats

    def get_bot_statistics(self, bot_name: str) -> Dict:
        """
        Retrieves detailed statistics for a specific bot.

        Args:
            bot_name (str): The name of the bot.

        Returns:
            Dict: A dictionary with statistics for the bot (e.g., total payoff, matches played).

        Raises:
            KeyError: If the bot hasn't participated in any matches.
        """
        # Initialize statistics
        stats = {
            TOTAL_PAYOFF: 0,
            MATCHES_PLAYED: 0,
            COOPERATE_COUNT: 0,
            DEFECT_COUNT: 0,
            COOPERATION_RATE: 0.0
        }

        bot_found = False

        # Aggregate statistics from all matches
        for result in self.results:
            if f"{bot_name}_actions" in result:
                bot_found = True
                stats[TOTAL_PAYOFF] += result[f"{bot_name}{PAYOFF_SUFFIX}"]
                stats[MATCHES_PLAYED] += 1

                actions = result[f"{bot_name}{ACTIONS_SUFFIX}"]
                stats[COOPERATE_COUNT] += actions.count(COOPERATE)
                stats[DEFECT_COUNT] += actions.count(DEFECT)

        if not bot_found:
            raise KeyError(f"No statistics found for bot: {bot_name}")

        # Calculate cooperation rate
        total_actions = stats[COOPERATE_COUNT] + stats[DEFECT_COUNT]
        if total_actions > 0:
            stats[COOPERATION_RATE] = float(stats[COOPERATE_COUNT] / total_actions)

        return stats

    def clear_results(self):
        """
        Clears all stored results.
        """
        self.results = []
