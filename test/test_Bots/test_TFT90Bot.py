import unittest
from model.bots.TFT90Bot import TFT90Bot
from model.constants import COOPERATE, DEFECT


class TestTFT90Bot(unittest.TestCase):

    def setUp(self):
        self.bot = TFT90Bot()

    def test_name(self):
        self.assertEqual(self.bot.name, "TFT90Bot")

    def test_choose_action_first_round(self):
        self.assertEqual(self.bot.choose_action(None), COOPERATE)

    def test_choose_action_forgives_defect(self):
        forgiven = False
        retaliated = False

        # Run the test multiple times to ensure forgiveness happens probabilistically
        for _ in range(100):
            action = self.bot.choose_action("SomeOpponentName", DEFECT)
            if action == COOPERATE:
                forgiven = True
            elif action == DEFECT:
                retaliated = True
            if forgiven and retaliated:
                break

        self.assertTrue(forgiven, "The bot should forgive defections at least occasionally.")
        self.assertTrue(retaliated, "The bot should retaliate against defections most of the time.")

    def test_choose_action_mirror_cooperate(self):
        self.bot.choose_action(None)  # First round
        self.assertEqual(self.bot.choose_action("SomeOpponentName", COOPERATE), COOPERATE)
        self.assertEqual(self.bot.choose_action("SomeOpponentName", COOPERATE), COOPERATE)

    def test_reset(self):
        """
        Tests if the reset method restores the bot's initial cooperative state.
        """
        # Simulate a few rounds
        self.bot.choose_action("SomeOpponentName", DEFECT)
        self.bot.reset()

        # Ensure it cooperates again in the first round of the new match
        self.assertEqual(self.bot.choose_action(None), COOPERATE)


if __name__ == "__main__":
    unittest.main()
