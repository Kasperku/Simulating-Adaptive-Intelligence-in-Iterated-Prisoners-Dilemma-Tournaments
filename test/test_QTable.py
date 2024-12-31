import unittest
from model.QTable import QTable
from model.constants import COOPERATE, DEFECT, LEARNING_RATE, DISCOUNT_FACTOR

class TestQTable(unittest.TestCase):
    def setUp(self):
        self.states = [COOPERATE, DEFECT]
        self.actions = [COOPERATE, DEFECT]
        self.qtable = QTable(self.states, self.actions)

    def test_initialization(self):
        """Test that QTable initializes with correct structure and zero values"""
        # Check structure
        self.assertEqual(set(self.qtable.table.keys()), {COOPERATE, DEFECT})
        for state in self.states:
            self.assertEqual(set(self.qtable.table[state].keys()), {COOPERATE, DEFECT})
        
        # Check initial values are 0
        for state in self.states:
            for action in self.actions:
                self.assertEqual(self.qtable.get_q_value(state, action), 0.0)

    def test_get_q_value(self):
        """Test getting Q-values, including edge cases"""
        # Test normal case
        self.assertEqual(self.qtable.get_q_value(COOPERATE, COOPERATE), 0.0)
        
        # Test after manual update
        self.qtable.table[COOPERATE][DEFECT] = 1.5
        self.assertEqual(self.qtable.get_q_value(COOPERATE, DEFECT), 1.5)
        
        # Test invalid state/action
        with self.assertRaises(KeyError):
            self.qtable.get_q_value("INVALID", COOPERATE)
        with self.assertRaises(KeyError):
            self.qtable.get_q_value(COOPERATE, "INVALID")

    def test_update_q_value(self):
        """Test Q-value updates using the Bellman equation"""
        # Set up initial values
        self.qtable.table[DEFECT][COOPERATE] = 2.0  # Max future value
        self.qtable.table[DEFECT][DEFECT] = 1.0
        
        # Test update with known values
        state = COOPERATE
        action = DEFECT
        learning_rate = 0.1
        immediate_reward = 5
        discount_factor = 0.9
        next_state = DEFECT
        
        self.qtable.update_q_value(
            state=state,
            action=action,
            learning_rate=learning_rate,
            immediate_reward=immediate_reward,
            discount_factor=discount_factor,
            next_state=next_state
        )
        
        # Calculate expected value manually:
        # Q(s,a) = Q(s,a) + α[r + γmax(Q(s',a')) - Q(s,a)]
        current_q = 0.0  # Initial value
        max_future_q = 2.0  # max(Q(DEFECT, *))
        expected_q = current_q + learning_rate * (
            immediate_reward + (discount_factor * max_future_q) - current_q
        )
        
        self.assertAlmostEqual(
            self.qtable.get_q_value(state, action),
            expected_q,
            places=10
        )

    def test_multiple_updates(self):
        """Test multiple sequential updates to ensure values accumulate correctly"""
        state = COOPERATE
        action = DEFECT
        
        # First update
        self.qtable.update_q_value(
            state=state,
            action=action,
            learning_rate=0.1,
            immediate_reward=5,
            discount_factor=0.9,
            next_state=DEFECT
        )
        first_update = self.qtable.get_q_value(state, action)
        
        # Second update with different values
        self.qtable.update_q_value(
            state=state,
            action=action,
            learning_rate=0.1,
            immediate_reward=3,
            discount_factor=0.9,
            next_state=COOPERATE
        )
        
        # Ensure value changed
        self.assertNotEqual(
            self.qtable.get_q_value(state, action),
            first_update
        )

if __name__ == '__main__':
    unittest.main()
