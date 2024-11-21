import unittest
from bots.CooperateBot import CooperateBot

class TestCooperateBot(unittest.TestCase):

    def setUp(self):
        self.bot = CooperateBot()

    def test_name(self):
        self.assertEqual(self.bot.name, "CooperateBot")

    def test_choose_action_always_cooperate(self):
        self.assertEqual(self.bot.choose_action("Cooperate"), "Cooperate")
        self.assertEqual(self.bot.choose_action("Defect"), "Cooperate")
        self.assertEqual(self.bot.choose_action(None), "Cooperate")

    def test_reset_no_change(self):
        self.bot.reset()
        self.assertEqual(self.bot.choose_action("Cooperate"), "Cooperate")
        self.assertEqual(self.bot.choose_action("Defect"), "Cooperate")

if __name__ == "__main__":
    unittest.main()
