import unittest
from model.bots.GrimBot import GrimBot
from model.constants import COOPERATE, DEFECT


class TestGrimBot(unittest.TestCase):

    def setUp(self):
        self.bot = GrimBot()

    def test_initial_state(self):
        """Test initial state of GrimBot"""
        self.assertEqual(self.bot.name, "GrimBot")
        self.assertTrue(self.bot.cooperate)

    def test_first_move(self):
        """Test that GrimBot cooperates on first move"""
        self.assertEqual(self.bot.choose_action(None), COOPERATE)
        self.assertTrue(self.bot.cooperate)  # State should remain cooperative

    def test_response_to_cooperation(self):
        """Test that GrimBot keeps cooperating when opponent cooperates"""
        moves = [COOPERATE] * 5
        for move in moves:
            self.assertEqual(self.bot.choose_action(move), COOPERATE)
            self.assertTrue(self.bot.cooperate)  # State should remain cooperative

    def test_response_to_defection(self):
        """Test that GrimBot switches to permanent defection after opponent defects"""
        # First cooperate
        self.assertEqual(self.bot.choose_action(COOPERATE), COOPERATE)
        self.assertTrue(self.bot.cooperate)

        # Switch to defection after opponent defects
        self.assertEqual(self.bot.choose_action(DEFECT), DEFECT)
        self.assertFalse(self.bot.cooperate)

        # Keep defecting regardless of opponent's moves
        test_moves = [COOPERATE, DEFECT, COOPERATE, COOPERATE]
        for move in test_moves:
            self.assertEqual(self.bot.choose_action(move), DEFECT)
            self.assertFalse(self.bot.cooperate)

    def test_reset(self):
        """Test that reset restores initial cooperative state"""
        # Make bot defect
        self.bot.choose_action(DEFECT)
        self.assertFalse(self.bot.cooperate)
        
        # Reset should restore cooperative state
        self.bot.reset()
        self.assertTrue(self.bot.cooperate)
        self.assertEqual(self.bot.choose_action(None), COOPERATE)

    def test_state_persistence(self):
        """Test that state persists between moves until reset"""
        # Start cooperative
        self.assertTrue(self.bot.cooperate)
        self.assertEqual(self.bot.choose_action(COOPERATE), COOPERATE)

        # Switch to defection
        self.assertEqual(self.bot.choose_action(DEFECT), DEFECT)
        self.assertFalse(self.bot.cooperate)

        # Create new instance to verify state isn't shared
        new_bot = GrimBot()
        self.assertTrue(new_bot.cooperate)
        self.assertEqual(new_bot.choose_action(COOPERATE), COOPERATE)


if __name__ == "__main__":
    unittest.main()
