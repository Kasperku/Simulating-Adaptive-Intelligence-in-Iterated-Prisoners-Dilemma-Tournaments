from typing import List, Dict
from model.constants import COOPERATE, DEFECT


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
                Must contain 'rounds_played' and for each bot: '_actions' and '_total_payoff'

        Raises:
            KeyError: If the result format is invalid
        """
        # Validate required fields
        if 'rounds_played' not in result:
            raise KeyError("Result must contain 'rounds_played'")

        # Find bot names by looking for '_actions' suffix
        bot_names = {key.split('_')[0] for key in result.keys() if key.endswith('_actions')}
        
        # Validate that each bot has both actions and total_payoff
        for bot_name in bot_names:
            if f"{bot_name}_total_payoff" not in result:
                raise KeyError(f"Missing total_payoff for bot {bot_name}")
            if f"{bot_name}_actions" not in result:
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
                  with aggregate statistics (total payoff, matches played, cooperate count, defect count).
        """
        aggregate_stats = {}

        for result in self.results:
            # Extract bot names from the result
            bot_names = {key.split('_')[0] for key in result.keys() 
                        if key.endswith('_actions') or key.endswith('_total_payoff')}

            for bot_name in bot_names:
                if bot_name not in aggregate_stats:
                    aggregate_stats[bot_name] = {
                        "total_payoff": 0,
                        "matches_played": 0,
                        "cooperate_count": 0,
                        "defect_count": 0
                    }

                self._update_payoff_and_matches(aggregate_stats, bot_name, result)
                self._count_actions(aggregate_stats, bot_name, result)

        return aggregate_stats

    def _update_payoff_and_matches(self, aggregate_stats: Dict, bot_name: str, result: Dict):
        """Helper method to update payoff and match count statistics"""
        aggregate_stats[bot_name]["total_payoff"] = aggregate_stats[bot_name]["total_payoff"] + result[f"{bot_name}_total_payoff"]
        aggregate_stats[bot_name]["matches_played"] += 1

    def _count_actions(self, aggregate_stats: Dict, bot_name: str, result: Dict):
        """Helper method to count cooperate and defect actions"""
        actions = result[f"{bot_name}_actions"]
        aggregate_stats[bot_name]["cooperate_count"] += actions.count(COOPERATE)
        aggregate_stats[bot_name]["defect_count"] += actions.count(DEFECT)

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
            "total_payoff": 0,
            "matches_played": 0,
            "cooperate_count": 0,
            "defect_count": 0,
            "cooperation_rate": 0.0
        }

        bot_found = False

        # Aggregate statistics from all matches
        for result in self.results:
            if f"{bot_name}_actions" in result:
                bot_found = True
                stats["total_payoff"] += result[f"{bot_name}_total_payoff"]
                stats["matches_played"] += 1

                actions = result[f"{bot_name}_actions"]
                stats["cooperate_count"] += actions.count(COOPERATE)
                stats["defect_count"] += actions.count(DEFECT)

        if not bot_found:
            raise KeyError(f"No statistics found for bot: {bot_name}")

        # Calculate cooperation rate
        total_actions = stats["cooperate_count"] + stats["defect_count"]
        if total_actions > 0:
            stats["cooperation_rate"] = float(stats["cooperate_count"] / total_actions)

        return stats

    def clear_results(self):
        """
        Clears all stored results.
        """
        self.results = []
