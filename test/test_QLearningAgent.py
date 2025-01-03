import unittest

from model.QTable import QTable
from model.QLearningAgent import QLearningAgent
from model.constants import *


class TestQLearningAgent(unittest.TestCase):
    def setUp(self):
        """
        Sets up a default agent with custom variables
        """
        self.agent = QLearningAgent()
    
    def test_initialization(self):
        """
        Tests whether the agent is initialized correctly
        """
        self.assertEqual(self.agent.get_exploration_rate("TFTBot"), DEFAULT_EXPLORATION_RATE)
        self.assertEqual(self.agent.get_learning_rate(), LEARNING_RATE)
        self.assertEqual(self.agent.get_discount_factor(), DISCOUNT_FACTOR)
        self.assertEqual(self.agent.actions, [COOPERATE, DEFECT])
        self.assertEqual(self.agent.QTables, {})
    
    def test_get_q_value_table_not_initialized(self):
        """
        Tests whether the Q-value is updated correctly
        """
        self.assertEqual(self.agent.get_q_value("TFTBot", state=COOPERATE, action=DEFECT), 0.0)
        self.assertEqual(self.agent.get_q_value("TFTBot", state=COOPERATE, action=COOPERATE), 0.0)
        self.assertEqual(self.agent.get_q_value("TFTBot", state=DEFECT, action=DEFECT), 0.0)
        self.assertEqual(self.agent.get_q_value("TFTBot", state=DEFECT, action=COOPERATE), 0.0)
    
    def test_update_q_value(self):
        """
        Tests whether the Q-value is updated correctly
        """

        reward = 5

        self.assertEqual(self.agent.get_q_value("TFTBot", state=COOPERATE, action=DEFECT), 0.0)
        self.agent.update_q_value("TFTBot", state=COOPERATE, action=DEFECT, reward=reward, next_state=DEFECT)

        # New Q-value = Current Q-value + Learning Rate (Immediate Reward + Discount Factor * Max Future Q-value - Current Q-value)
        q_value1 = self.agent.get_q_value("TFTBot", state=COOPERATE, action=DEFECT)
        self.assertEqual(q_value1,  LEARNING_RATE * (reward + DISCOUNT_FACTOR * 0.0 - 0.0))
        
        # Update Q-value again for state=next_state
        self.agent.update_q_value("TFTBot", state=COOPERATE, action=DEFECT, reward=reward, next_state=COOPERATE)
        q_value2 = self.agent.get_q_value("TFTBot", state=COOPERATE, action=DEFECT)
        self.assertEqual(q_value2,  q_value1 + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max(q_value1, 0.0) - q_value1))

        # Update Q-value for state!=next_state
        self.agent.update_q_value("TFTBot", state=COOPERATE, action=DEFECT, reward=reward, next_state=DEFECT)
        q_value3 = self.agent.get_q_value("TFTBot", state=COOPERATE, action=DEFECT)
        self.assertEqual(q_value3,  q_value2 + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max(0.0, 0.0) - q_value2))

    def test_choose_action_exploration_rate_0(self):
        """Tests whether the agent chooses the best action when exploration rate is 0"""
        opponent = "TFTBot"
        
        # Initialize opponent's Q-table and exploration rate
        self.agent.initialize_q_table_for_opponent(opponent)
        self.agent.initialize_exploration_rate(opponent)
        
        # Verify initial Q-values are 0
        self.assertEqual(self.agent.get_q_value(opponent, state=COOPERATE, action=DEFECT), 0.0)
        self.assertEqual(self.agent.get_q_value(opponent, state=COOPERATE, action=COOPERATE), 0.0)

        # Set exploration rate to 0 for this opponent
        self.agent.set_exploration_rate(opponent, 0.0)
        self.assertEqual(self.agent.get_exploration_rate(opponent), 0.0)

        # Update Q-values with rewards
        reward = 5
        self.agent.update_q_value(opponent, state=COOPERATE, action=DEFECT, reward=reward, next_state=COOPERATE)
        self.agent.update_q_value(opponent, state=COOPERATE, action=DEFECT, reward=reward, next_state=DEFECT)
        self.agent.update_q_value(opponent, state=COOPERATE, action=COOPERATE, reward=reward*2, next_state=COOPERATE)  # Double reward
        self.agent.update_q_value(opponent, state=COOPERATE, action=COOPERATE, reward=reward*2, next_state=DEFECT)    # Double reward

        # Get final Q-values
        q_value_defect = self.agent.get_q_value(opponent, state=COOPERATE, action=DEFECT)
        q_value_cooperate = self.agent.get_q_value(opponent, state=COOPERATE, action=COOPERATE)
        
        # Verify COOPERATE has higher Q-value
        self.assertGreater(q_value_cooperate, q_value_defect, 
                          "COOPERATE should have higher Q-value due to double reward")

        # With exploration rate 0, should always choose the action with highest Q-value
        chosen_action = self.agent.choose_action(opponent, state=COOPERATE)
        self.assertEqual(chosen_action, COOPERATE, 
                        f"Should choose COOPERATE (Q={q_value_cooperate}) over DEFECT (Q={q_value_defect})")

    def test_choose_action_exploration_rate_1(self):
        """Tests whether the agent explores randomly when exploration rate is 1"""
        opponent = "TFTBot"
        
        # Initialize opponent's Q-table and exploration rate
        self.agent.initialize_q_table_for_opponent(opponent)
        self.agent.initialize_exploration_rate(opponent)
        
        # Set exploration rate to 1 for this opponent
        self.agent.set_exploration_rate(opponent, 1.0)
        self.assertEqual(self.agent.get_exploration_rate(opponent), 1.0)
        
        # Even with different Q-values, should still explore randomly
        self.agent.update_q_value(opponent, state=COOPERATE, action=DEFECT, reward=5, next_state=COOPERATE)
        self.agent.update_q_value(opponent, state=COOPERATE, action=COOPERATE, reward=1, next_state=COOPERATE)
        
        # Make 100 choices and count them
        actions = [self.agent.choose_action(opponent, state=COOPERATE) for _ in range(100)]
        cooperate_count = actions.count(COOPERATE)
        defect_count = actions.count(DEFECT)
        
        # With exploration rate 1, choices should be roughly 50-50
        self.assertAlmostEqual(cooperate_count, 50, delta=15, 
                             msg=f"Expected ~50 COOPERATE, got {cooperate_count}")
        self.assertAlmostEqual(defect_count, 50, delta=15,
                             msg=f"Expected ~50 DEFECT, got {defect_count}")

    def test_decay_exploration_rate(self):
        """Tests whether the exploration rate is decayed correctly for specific opponents"""
        # Test for first opponent
        opponent1 = "TFTBot"
        self.agent.initialize_exploration_rate(opponent1)
        initial_rate1 = self.agent.get_exploration_rate(opponent1)
        self.assertEqual(initial_rate1, DEFAULT_EXPLORATION_RATE)
        
        self.agent.decay_exploration_rate(opponent1, DECAY_RATE)
        self.assertAlmostEqual(
            self.agent.get_exploration_rate(opponent1), 
            DEFAULT_EXPLORATION_RATE * DECAY_RATE, 
            delta=0.01,
            msg="First opponent's rate should decay"
        )
        
        # Test for second opponent (should be independent)
        opponent2 = "DefectBot"
        self.agent.initialize_exploration_rate(opponent2)
        initial_rate2 = self.agent.get_exploration_rate(opponent2)
        self.assertEqual(
            initial_rate2, 
            DEFAULT_EXPLORATION_RATE,
            msg="Second opponent should start with default rate"
        )
        
        # Verify first opponent's rate remains unchanged
        self.assertAlmostEqual(
            self.agent.get_exploration_rate(opponent1),
            DEFAULT_EXPLORATION_RATE * DECAY_RATE,
            delta=0.01,
            msg="First opponent's rate should remain unchanged"
        )

    def test_choose_action_equal_q_values(self):
        """Tests whether the agent randomly chooses between actions with equal Q-values"""
        opponent = "TFTBot"
        
        # Initialize opponent's Q-table and exploration rate
        self.agent.initialize_q_table_for_opponent(opponent)
        self.agent.initialize_exploration_rate(opponent)
        
        # Set exploration rate to 0 to ensure choices are based on Q-values
        self.agent.set_exploration_rate(opponent, 0.0)
        self.assertEqual(self.agent.get_exploration_rate(opponent), 0.0)

        # Set equal Q-values for both actions
        table = self.agent.get_qtable_for_opponent(opponent)
        equal_q_value = 10.0
        table.set_q_value(COOPERATE, DEFECT, equal_q_value)
        table.set_q_value(COOPERATE, COOPERATE, equal_q_value)
        
        # Verify Q-values are equal
        self.assertEqual(
            self.agent.get_q_value(opponent, COOPERATE, DEFECT),
            self.agent.get_q_value(opponent, COOPERATE, COOPERATE),
            "Q-values should be equal"
        )

        # Make 100 choices and count them
        actions = [self.agent.choose_action(opponent, COOPERATE) for _ in range(100)]
        cooperate_count = actions.count(COOPERATE)
        defect_count = actions.count(DEFECT)
        
        # With equal Q-values, should randomly choose between them
        self.assertAlmostEqual(cooperate_count, 50, delta=15,
                             msg=f"Expected ~50 COOPERATE, got {cooperate_count}")
        self.assertAlmostEqual(defect_count, 50, delta=15,
                             msg=f"Expected ~50 DEFECT, got {defect_count}")
