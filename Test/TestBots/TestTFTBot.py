import unittest
from bots.TFTBot import TFTBot

class TestTFTBot(unittest.TestCase):

    def setUp(self):
        self.bot = TFTBot()

    def test_name(self):
        self.assertEqual(self.bot.name, "TFTBot")

    def test_choose_action_always_mirror(self):
        self.assertEqual(self.bot.choose_action(None), "Cooperate")
        self.assertEqual(self.bot.choose_action("Cooperate"), "Cooperate")
        self.assertEqual(self.bot.choose_action("Defect"), "Defect")
        self.assertEqual(self.bot.choose_action("Cooperate"), "Cooperate")

    def test_reset(self):
        # Simulate the end of a round where the bot would defect
        self.bot.choose_action(None)
        self.assertEqual(self.bot.choose_action("Defect"), "Defect")
        self.bot.reset()
        self.assertEqual(self.bot.choose_action(None), "Cooperate")

if __name__ == "__main__":
    unittest.main()