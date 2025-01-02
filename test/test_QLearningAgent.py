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
        self.assertEqual(self.agent.get_exploration_rate(), DEFAULT_EXPLORATION_RATE)
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
        """
        Tests whether the agent chooses the best action when exploration rate is 0
        """
        self.assertEqual(self.agent.get_q_value("TFTBot", state=COOPERATE, action=DEFECT), 0.0)
        self.assertEqual(self.agent.get_q_value("TFTBot", state=COOPERATE, action=COOPERATE), 0.0)

        reward = 5
        self.agent.set_exploration_rate(0.0)

        self.agent.update_q_value("TFTBot", state=COOPERATE, action=DEFECT, reward=reward, next_state=COOPERATE)
        self.agent.update_q_value("TFTBot", state=COOPERATE, action=DEFECT, reward=reward, next_state=DEFECT)
        self.agent.update_q_value("TFTBot", state=COOPERATE, action=COOPERATE, reward=reward, next_state=COOPERATE)
        self.agent.update_q_value("TFTBot", state=COOPERATE, action=COOPERATE, reward=reward, next_state=DEFECT)

        # q_value2 > q_value1 
        q_value1 = self.agent.get_q_value("TFTBot", state=COOPERATE, action=DEFECT)
        q_value2 = self.agent.get_q_value("TFTBot", state=COOPERATE, action=COOPERATE)

        self.assertEqual(self.agent.choose_action("TFTBot", state=COOPERATE), COOPERATE)

    def test_choose_action_exploration_rate_1(self):
        """
        Tests whether the agent chooses the best action when exploration rate is 1
        """
        self.assertEqual(self.agent.get_exploration_rate(), DEFAULT_EXPLORATION_RATE)
        actions = [self.agent.choose_action("TFTBot", state=COOPERATE) for _ in range(100)]
        cooperate_count = actions.count(COOPERATE)
        defect_count = actions.count(DEFECT)
        
        # both counts should be around 50
        self.assertAlmostEqual(cooperate_count, 50, delta=10)
        self.assertAlmostEqual(defect_count, 50, delta=10)

    def test_decay_exploration_rate(self):
        """
        Tests whether the exploration rate is decayed correctly
        """
        self.assertEqual(self.agent.get_exploration_rate(), DEFAULT_EXPLORATION_RATE)
        self.agent.decay_exploration_rate(DECAY_RATE)
        self.assertAlmostEqual(self.agent.get_exploration_rate(), DEFAULT_EXPLORATION_RATE*DECAY_RATE, delta=0.01)

    def test_choose_action_equal_q_values(self):
        """
        Tests whether the agent chooses the best action when the Q-values are equal
        """
        self.assertEqual(self.agent.get_exploration_rate(), DEFAULT_EXPLORATION_RATE)
        self.agent.set_exploration_rate(0.0)

        table = self.agent.get_qtable_for_opponent("TFTBot")
        table.set_q_value(COOPERATE, DEFECT, 10)
        table.set_q_value(COOPERATE, COOPERATE, 10)

        actions = [self.agent.choose_action("TFTBot", COOPERATE) for _ in range(100)]
        cooperate_count = actions.count(COOPERATE)
        defect_count = actions.count(DEFECT)
        self.assertAlmostEqual(cooperate_count, 50, delta=15)
        self.assertAlmostEqual(defect_count, 50, delta=15)
