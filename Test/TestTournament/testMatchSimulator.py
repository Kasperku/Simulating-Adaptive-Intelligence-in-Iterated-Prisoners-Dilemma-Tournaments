import unittest
from model.tournament import MatchSimulator
from model.bots.BaseBot import BaseBot
from model.constants import COOPERATE, DEFECT, PAYOFF_MATRIX


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

        # Verify result structure
        self.assertIn("round", result)
        self.assertIn("bot1", result)
        self.assertIn("bot2", result)
        self.assertIn("bot1_actions", result)
        self.assertIn("bot2_actions", result)
        self.assertIn("bot1_payoff", result)
        self.assertIn("bot2_payoff", result)

    def test_simulate_match_payoffs(self):
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = 1

        result = self.match_simulator.simulate_match(bot1, bot2, round_number)

        # Verify payoffs from PAYOFF_MATRIX
        expected_payoff_bot1, expected_payoff_bot2 = PAYOFF_MATRIX[(COOPERATE, DEFECT)]
        self.assertEqual(result["bot1_payoff"], expected_payoff_bot1)
        self.assertEqual(result["bot2_payoff"], expected_payoff_bot2)

    def test_simulate_match_actions(self):
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = 1

        result = self.match_simulator.simulate_match(bot1, bot2, round_number)

        # Verify actions are logged correctly
        self.assertEqual(result["bot1_actions"][0], COOPERATE)
        self.assertEqual(result["bot2_actions"][0], DEFECT)

    def test_simulate_match_round_number(self):
        bot1 = MockBot(name="CooperateBot", action=COOPERATE)
        bot2 = MockBot(name="DefectBot", action=DEFECT)
        round_number = 5

        result = self.match_simulator.simulate_match(bot1, bot2, round_number)

        # Verify round number is correct
        self.assertEqual(result["round"], round_number)


if __name__ == "__main__":
    unittest.main()
