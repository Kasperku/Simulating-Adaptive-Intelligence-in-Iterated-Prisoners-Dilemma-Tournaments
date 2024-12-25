from typing import List, Dict


class ResultManager:
    """
    Manages and analyzes results from matches in a Prisoner's Dilemma tournament.
    """

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
        """
        pass

    def get_all_results(self) -> List[Dict]:
        """
        Retrieves all recorded results. (round by round details)

        Returns:
            List[Dict]: A list of dictionaries representing all match results.
        """
        pass

    def get_aggregate_results(self) -> Dict:
        """
        Aggregates total payoffs and actions for each bot across all matches

        Returns:
            Dict: A dictionary where each key is a bot's name and the value is a dictionary
                  with aggregate statistics (e.g., total payoff, total actions).
        """
        pass

    def get_bot_statistics(self, bot_name: str) -> Dict:
        """
        Retrieves detailed statistics for a specific bot.

        Args:
            bot_name (str): The name of the bot.

        Returns:
            Dict: A dictionary with statistics for the bot (e.g., total payoff, matches played).
        """
        pass

    def clear_results(self):
        """
        Clears all stored results.
        """
        pass
