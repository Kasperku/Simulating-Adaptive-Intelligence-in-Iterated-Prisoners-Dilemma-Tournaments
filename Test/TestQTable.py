import unittest

from model.constants import COOPERATE, DEFECT
from model.QTable import QTable


class TestQTable(unittest.TestCase):

    def setUp(self):
        self.states = [COOPERATE, DEFECT]
        self.actions = [COOPERATE, DEFECT]
        self.QTable = QTable(self.states, self.actions)

    def test_get_q_value_initial(self):
        for state in self.states:
            for action in self.actions:
                self.assertEqual(0.0, self.QTable.get_q_value(state, action))

    def test_get_q_value_update(self):

        self.QTable.table[COOPERATE][DEFECT] = 1.5
        self.assertEqual(1.5, self.QTable.get_q_value(COOPERATE, DEFECT))


if __name__ == "__main__":
    unittest.main()
