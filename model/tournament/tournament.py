from typing import List
from model.bots.BaseBot import BaseBot
from model.tournament import MatchSimulator, ResultManager


class Tournament:
    # Static field
    MATCHES_PER_PAIR: int = 10

    def __init__(self, participants: List[BaseBot], rounds: int, match_simulator: MatchSimulator, result_manager: ResultManager):
        """
        Initializes the tournament with participants and the number of rounds.

        Args:
            participants (List[BaseBot]): List of bots participating in the tournament.
            rounds (int): Number of rounds to play.
            match_simulator (MatchSimulator): Object responsible for simulating matches.
            result_manager (ResultManager): Object responsible for managing results.
        """
        self.participants = participants
        self.rounds = rounds
        self.match_simulator = match_simulator
        self.result_manager = result_manager

    # Getters
    def get_participants(self) -> List[BaseBot]:
        return self.participants

    def get_rounds(self) -> int:
        return self.rounds

    def get_match_simulator(self) -> MatchSimulator:
        return self.match_simulator

    def get_result_manager(self) -> ResultManager:
        return self.result_manager

    # Tournament logic
    def run_tournament(self):
        """
        Runs the entire tournament by iterating through self.rounds
        """
        pass

    def play_round(self, round_number: int):
        """
        Executes a single round where each bot plays multiple matches against every other bot.

        Args:
            round_number (int): The current round number.
        """
        pass

    def get_results(self):
        """
        Retrieves the results of the tournament.

        Returns:
            List[Dict]: A list of recorded results from the ResultManager.
        """
        pass

