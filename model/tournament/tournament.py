from typing import List, Dict
from model.bots.BaseBot import BaseBot
from model.tournament import MatchSimulator, ResultManager


class Tournament:
    # Static field
    MATCHES_PER_PAIR: int = 10

    def __init__(self, participants: List[BaseBot], rounds: int, match_simulator: MatchSimulator,
                 result_manager: ResultManager):
        """
        Initializes the tournament with participants and the number of rounds.

        Args:
            participants (List[BaseBot]): List of bots participating in the tournament.
            rounds (int): Number of rounds to play.
            match_simulator (MatchSimulator): Object responsible for simulating matches.
            result_manager (ResultManager): Object responsible for managing results.
        """
        if not all(isinstance(bot, BaseBot) for bot in participants):
            raise ValueError("All participants must be of type BaseBot.")

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
        for round_number in range(1, self.get_rounds() + 1):
            print(f"Starting Round {round_number}")
            match_results = self.play_round(round_number)
            self.record_results(match_results)
            self.reset_bots()
        print("Tournament Completed")

    def play_round(self, round_number: int) -> List[Dict]:
        """
        Executes a single round where each bot plays multiple matches against every other bot.

        Args:
            round_number (int): The current round number.

        Returns:
            List[Dict]: A list of match results for the round.
        """
        round_results = []
        for i in range(len(self.participants)):
            for j in range(i + 1, len(self.participants)):
                bot1 = self.participants[i]
                bot2 = self.participants[j]

                for _ in range(Tournament.MATCHES_PER_PAIR):
                    match_result = self.match_simulator.simulate_match(bot1, bot2, round_number)
                    round_results.append(match_result)

        return round_results

    def reset_bots(self):
        """
        Resets all bots to their initial state for the next round.
        """
        for bot in self.participants:
            bot.reset()

    def record_results(self, match_results: List[Dict]):
        """
        Records the results of a round.

        Args:
            match_results (List[Dict]): A list of match results to record.
        """
        for result in match_results:
            self.result_manager.record_match_results(result)

    def get_results(self) -> List[Dict]:
        """
        Retrieves the results of the tournament.

        Returns:
            List[Dict]: A list of recorded results from the ResultManager.
        """
        return self.result_manager.get_all_results()
