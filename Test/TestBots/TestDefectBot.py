import unittest
from bots.DefectBot import DefectBot

class TestDefectBot(unittest.TestCase):

    def setUp(self):
        self.bot = DefectBot()

    def test_name(self):
        self.assertEqual(self.bot.name, "DefectBot")

    def test_choose_action_always_defect(self):
        self.assertEqual(self.bot.choose_action("Cooperate"), "Defect")
        self.assertEqual(self.bot.choose_action("Defect"), "Defect")
        self.assertEqual(self.bot.choose_action(None), "Defect")

    def test_reset_no_change(self):
        self.bot.reset()
        self.assertEqual(self.bot.choose_action("Cooperate"), "Defect")
        self.assertEqual(self.bot.choose_action("Defect"), "Defect")

if __name__ == "__main__":
    unittest.main()