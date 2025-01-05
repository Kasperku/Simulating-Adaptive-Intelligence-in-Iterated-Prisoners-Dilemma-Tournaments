import unittest
from model.tournament.MatchSimulator import MatchSimulator
from model.bots.BaseBot import BaseBot
from model.constants import *


class MockBot(BaseBot):
    """
    A mock bot for testing. Always chooses a predefined action.
    """

    def __init__(self, name: str, action: str):
        super().__init__(name)
        self.action = action

    def choose_action(self, opponent_last_action=None):
        return self.action


class TestMatchSimulator(unittest.TestCase):
    def setUp(self):
        self.match_simulator = MatchSimulator()

    def test_simulate_match_structure(self):
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = 1

        result = self.match_simulator.simulate_match(bot1, bot2, round_number)

        # Updated assertions to match implementation
        self.assertIn("round_number", result)
        self.assertIn(f"{bot1.name}_actions", result)
        self.assertIn(f"{bot2.name}_actions", result)
        self.assertIn(f"{bot1.name}_total_payoff", result)
        self.assertIn(f"{bot2.name}_total_payoff", result)

    def test_simulate_match_payoffs(self):
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = ITERATIONS

        result = self.match_simulator.simulate_match(bot1, bot2, round_number)

        # Verify payoffs from PAYOFF_MATRIX
        expected_payoff_bot1, expected_payoff_bot2 = PAYOFF_MATRIX[(COOPERATE, DEFECT)]
        self.assertEqual(result[f"{bot1.name}_total_payoff"], expected_payoff_bot1 * round_number)
        self.assertEqual(result[f"{bot2.name}_total_payoff"], expected_payoff_bot2 * round_number)

    def test_simulate_match_actions(self):
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = ITERATIONS

        result = self.match_simulator.simulate_match(bot1, bot2, round_number)

        # Verify actions are logged correctly
        self.assertEqual(result[f"{bot1.name}_actions"][0], COOPERATE)
        self.assertEqual(result[f"{bot2.name}_actions"][0], DEFECT)

    def test_simulate_match_round_number(self):
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = 5

        result = self.match_simulator.simulate_match(bot1, bot2, round_number)

        # Verify round number is correct
        self.assertEqual(result["round_number"], round_number)

    def test_invalid_round_number(self):
        """Test that negative or zero rounds raise ValueError"""
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        
        with self.assertRaises(ValueError):
            self.match_simulator.simulate_match(bot1, bot2, 0)
        
        with self.assertRaises(ValueError):
            self.match_simulator.simulate_match(bot1, bot2, -1)

    def test_get_match_results_before_simulation(self):
        """Test that getting results before any simulation raises RuntimeError"""
        with self.assertRaises(RuntimeError):
            self.match_simulator.get_match_results()

    def test_accumulating_payoffs(self):
        """Test that payoffs accumulate correctly over multiple rounds"""
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = ITERATIONS
        
        result = self.match_simulator.simulate_match(bot1, bot2, round_number)
        
        # Each round: COOPERATE vs DEFECT = (0, 5)
        expected_bot1_payoff = 0 * round_number  # Always gets 0
        expected_bot2_payoff = 5 * round_number  # Always gets 5
        
        self.assertEqual(result[f"{bot1.name}_total_payoff"], expected_bot1_payoff)
        self.assertEqual(result[f"{bot2.name}_total_payoff"], expected_bot2_payoff)

    def test_action_history_length(self):
        """Test that action history length matches round number"""
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = ITERATIONS
        
        result = self.match_simulator.simulate_match(bot1, bot2, round_number)
        
        self.assertEqual(len(result[f"{bot1.name}_actions"]), round_number)
        self.assertEqual(len(result[f"{bot2.name}_actions"]), round_number)


if __name__ == "__main__":
    unittest.main()
