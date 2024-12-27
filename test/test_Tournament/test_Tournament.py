import unittest
from unittest.mock import MagicMock
from model.bots.BaseBot import BaseBot
from model.tournament.MatchSimulator import MatchSimulator
from model.tournament.ResultManager import ResultManager
from model.tournament.tournament import Tournament
from model.constants import *


class TestTournament(unittest.TestCase):
    def setUp(self):
        """
        Sets up mock participants, MatchSimulator, and ResultManager for testing.
        """
        self.participants = [MagicMock(spec=BaseBot, name="TFTBot"), MagicMock(spec=BaseBot, name="GrimBot")]
        self.rounds = 5
        self.match_simulator = MagicMock(spec=MatchSimulator)
        self.result_manager = MagicMock(spec=ResultManager)
        self.tournament = Tournament(
            participants=self.participants,
            rounds=self.rounds,
            match_simulator=self.match_simulator,
            result_manager=self.result_manager
        )

    def test_tournament_initialization(self):
        """
        Tests that the Tournament initializes correctly with provided arguments.
        """
        self.assertEqual(self.tournament.get_participants(), self.participants)
        self.assertEqual(self.tournament.get_rounds(), self.rounds)
        self.assertEqual(self.tournament.get_match_simulator(), self.match_simulator)
        self.assertEqual(self.tournament.get_result_manager(), self.result_manager)

    def test_play_round(self):
        """
        Tests the `play_round` method to ensure bots play matches and results are recorded.
        """
        round_number = 1

        # Mock match results
        match_result = {
            "round_number": round_number,
            "TFTBot_actions": [COOPERATE, DEFECT],
            "GrimBot_actions": [COOPERATE, DEFECT],
            "TFTBot_total_payoff": 6,
            "GrimBot_total_payoff": 7
        }
        self.match_simulator.simulate_match.return_value = match_result

        # Call play_round
        results = self.tournament.play_round(round_number)

        # Verify the number of matches played
        expected_matches = (len(self.participants) * (len(self.participants) - 1) // 2) * Tournament.MATCHES_PER_PAIR
        self.assertEqual(self.match_simulator.simulate_match.call_count, expected_matches)

        # Verify `simulate_match` calls with correct arguments
        self.match_simulator.simulate_match.assert_any_call(self.participants[0], self.participants[1], round_number)

        # Verify the returned results
        self.assertEqual(len(results), expected_matches)
        self.assertIn(match_result, results)

    def test_run_tournament(self):
        """
        Tests the `run_tournament` method to ensure the tournament runs for the specified number of rounds.
        """
        # Mock `play_round`
        self.tournament.play_round = MagicMock()

        # Run the tournament
        self.tournament.run_tournament()

        # Verify `play_round` is called for each round
        self.assertEqual(self.tournament.play_round.call_count, self.rounds)

        # Ensure `play_round` is called with correct round numbers
        for round_number in range(1, self.rounds + 1):
            self.tournament.play_round.assert_any_call(round_number)

    def test_get_results(self):
        """
        Tests the `get_results` method to ensure it retrieves results from the `ResultManager`.
        """
        # Mock result data
        mock_results = [
            {"round_number": 1, "TFTBot_total_payoff": 10, "GrimBot_total_payoff": 8},
            {"round_number": 2, "TFTBot_total_payoff": 12, "GrimBot_total_payoff": 6}
        ]
        self.result_manager.get_all_results.return_value = mock_results

        # Call `get_results`
        results = self.tournament.get_results()

        # Verify `get_all_results` was called once
        self.result_manager.get_all_results.assert_called_once()

        # Check the retrieved results match the mock results
        self.assertEqual(results, mock_results)

    def test_empty_participants(self):
        """
        Tests the `Tournament` class behavior when no participants are provided.
        """
        empty_participants = []

        # Create a tournament with no participants
        self.tournament = Tournament(
            participants=empty_participants,
            rounds=5,
            match_simulator=self.match_simulator,
            result_manager=self.result_manager
        )

        # Call `run_tournament`
        self.tournament.run_tournament()

        # Verify `simulate_match` is never called since there are no participants
        self.match_simulator.simulate_match.assert_not_called()

        # Verify `get_results` returns an empty list
        self.result_manager.get_all_results.return_value = []
        self.assertEqual(self.tournament.get_results(), [])

    def test_no_rounds(self):
        """
        Tests the `Tournament` class behavior when `rounds = 0`.
        """
        # Create a tournament with valid participants but no rounds
        self.tournament = Tournament(
            participants=self.participants,
            rounds=0,
            match_simulator=self.match_simulator,
            result_manager=self.result_manager
        )

        # Run the tournament
        self.tournament.run_tournament()

        # Verify `play_round` is never called
        self.tournament.play_round = MagicMock()
        self.tournament.play_round.assert_not_called()

        # Verify `simulate_match` is never called
        self.match_simulator.simulate_match.assert_not_called()

        # Verify `get_results` returns an empty list
        self.result_manager.get_all_results.return_value = []
        self.assertEqual(self.tournament.get_results(), [])

    def test_full_tournament_flow(self):
        """
        Tests the full flow of a tournament with multiple participants and rounds.
        """
        # Create a tournament with valid participants and rounds
        self.tournament = Tournament(
            participants=self.participants,
            rounds=3,
            match_simulator=self.match_simulator,
            result_manager=self.result_manager
        )

        # Mock match results
        mock_match_result = {
            "round_number": 1,
            "GrimBot_actions": [COOPERATE, DEFECT],
            "TFTBot_actions": [COOPERATE, DEFECT],
            "GrimBot_total_payoff": 8,
            "TFTBot_total_payoff": 6
        }
        self.match_simulator.simulate_match.return_value = mock_match_result

        # Run the tournament
        self.tournament.run_tournament()

        # Verify `play_round` was called for each round
        self.tournament.play_round = MagicMock()
        self.assertEqual(self.tournament.play_round.call_count, 3)

        # Verify results were added to the ResultManager
        self.result_manager.record_match_results.assert_called()
        self.result_manager.get_all_results.return_value = [mock_match_result]

        # Verify the `get_results` method retrieves the correct results
        results = self.tournament.get_results()
        self.assertEqual(results, [mock_match_result])




