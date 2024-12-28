import unittest
from model.bots.TFTBot import TFTBot
from model.constants import COOPERATE, DEFECT


class TestTFTBot(unittest.TestCase):
    
    def setUp(self):
        self.bot = TFTBot()

    def test_name(self):
        self.assertEqual(self.bot.name, "TFTBot")

    def test_choose_action_always_mirror(self):
        self.assertEqual(self.bot.choose_action(None), COOPERATE)
        self.assertEqual(self.bot.choose_action(COOPERATE), COOPERATE)
        self.assertEqual(self.bot.choose_action(DEFECT), DEFECT)
        self.assertEqual(self.bot.choose_action(COOPERATE), COOPERATE)

    def test_reset(self):
        # Simulate the end of a round where the bot would defect
        self.bot.choose_action(None)
        self.assertEqual(self.bot.choose_action("Defect"), "Defect")
        self.bot.reset()
        self.assertEqual(self.bot.choose_action(None), "Cooperate")


if __name__ == "__main__":
    unittest.main()
