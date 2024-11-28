import unittest
from model.bots.GrimBot import GrimBot


class TestGrimBot(unittest.TestCase):

    def setUp(self):
        self.bot = GrimBot()

    def test_name(self):
        self.assertEqual(self.bot.name, "GrimBot")

    def test_choose_action_cooperate_until_betrayed(self):
        self.assertEqual(self.bot.choose_action(None), "Cooperate")
        self.assertEqual(self.bot.choose_action("Cooperate"), "Cooperate")
        self.assertEqual(self.bot.choose_action("Defect"), "Defect")
        self.assertEqual(self.bot.choose_action("Cooperate"), "Defect")
        self.assertEqual(self.bot.choose_action("Cooperate"), "Defect")

    def test_reset(self):
        # Simulate defection
        self.bot.choose_action("Defect")
        self.assertEqual(self.bot.choose_action("Cooperate"), "Defect")  # Defects permanently
        self.assertEqual(self.bot.choose_action("Cooperate"), "Defect")
        self.bot.reset()

        # Should cooperate again after reset
        self.assertEqual(self.bot.choose_action(None), "Cooperate")


if __name__ == "__main__":
    unittest.main()
