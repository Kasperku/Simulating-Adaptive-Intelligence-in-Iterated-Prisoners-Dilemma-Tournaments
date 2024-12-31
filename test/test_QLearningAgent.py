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

































    # def test_initialize_q_table_for_opponent(self):
    #     """
    #     Tests whether QTables are correctly initialized for opponents.
    #     """
    #     opponent_name = "TFTBot"

    #     # Ensure the QTable is not present initially
    #     self.assertNotIn(opponent_name, self.agent.QTables)

    #     # Initialize QTable for the opponent
    #     self.agent.initialize_q_table_for_opponent(opponent_name)

    #     # Check if the QTable is now present
    #     self.assertIn(opponent_name, self.agent.QTables)
    #     self.assertIsInstance(self.agent.QTables[opponent_name], QTable)

    #     # Verify the QTable's structure
    #     q_table = self.agent.QTables[opponent_name]
    #     for state in self.actions:
    #         for action in self.actions:
    #             self.assertEqual(q_table.get_q_value(state, action), 0.0)

    # def test_get_q_value_existing_opponent(self):
    #     """
    #     Tests retrieving Q-values for an opponent with an existing QTable.
    #     """
    #     opponent_name = "AlwaysDefectBot"
    #     self.agent.initialize_q_table_for_opponent(opponent_name)

    #     # Set a Q-value for testing
    #     self.agent.QTables[opponent_name].update_q_value(
    #         state=COOPERATE,
    #         action=DEFECT,
    #         learning_rate=LEARNING_RATE,
    #         immediate_reward=5,
    #         discount_factor=DISCOUNT_FACTOR,
    #         next_state=DEFECT
    #     )

    #     # Retrieve the Q-value and verify correctness
    #     q_value = self.agent.get_q_value(opponent_name, COOPERATE, DEFECT)
    #     self.assertGreater(q_value, 0.0)  # Verify it has been updated

    # def test_get_q_value_new_opponent(self):
    #     """
    #     Tests retrieving Q-values for a new opponent without a QTable.
    #     """
    #     opponent_name = "NewOpponent"

    #     # Ensure the QTable does not exist initially
    #     self.assertNotIn(opponent_name, self.agent.QTables)

    #     # Retrieve a Q-value for the new opponent
    #     q_value = self.agent.get_q_value(opponent_name, COOPERATE, DEFECT)

    #     # Verify that a QTable was created and the default Q-value is returned
    #     self.assertIn(opponent_name, self.agent.QTables)
    #     self.assertEqual(q_value, 0.0)

    # def test_initialize_q_table_twice(self):
    #     """
    #     Tests that initializing a QTable for the same opponent twice does not overwrite existing data.
    #     """
    #     opponent_name = "GrimBot"
    #     self.agent.initialize_q_table_for_opponent(opponent_name)

    #     # Set a Q-value for the opponent
    #     self.agent.QTables[opponent_name].update_q_value(
    #         state=DEFECT,
    #         action=DEFECT,
    #         learning_rate=LEARNING_RATE,
    #         immediate_reward=3,
    #         discount_factor=DISCOUNT_FACTOR,
    #         next_state=DEFECT
    #     )

    #     # Re-initialize the same opponent
    #     self.agent.initialize_q_table_for_opponent(opponent_name)

    #     # Verify that the Q-value is not reset
    #     q_value = self.agent.get_q_value(opponent_name, DEFECT, DEFECT)
    #     self.assertGreater(q_value, 0.0)

    # def test_epsilon_greedy_action_selection(self):
    #     """
    #     Tests the agent's ε-greedy policy for action selection.
    #     Our agent against a TFT Bot with the last action COOPERATE should continue to COOPERATE
    #     when the exploration rate is 0 and should randomize when exploration rate is 1
    #     """
    #     opponent_name = "TFTBot"
    #     self.agent.initialize_q_table_for_opponent(opponent_name)

    #     # Mock Q-values, the reward for COOPERATE(10) > DEFECT
    #     self.agent.QTables[opponent_name].update_q_value(COOPERATE, DEFECT, LEARNING_RATE, 5, DISCOUNT_FACTOR, DEFECT)
    #     self.agent.QTables[opponent_name].update_q_value(COOPERATE, COOPERATE, LEARNING_RATE, 10, DISCOUNT_FACTOR,
    #                                                      DEFECT)

    #     # Ensure the agent can exploit (choose the best action) when exploration_rate = 0
    #     self.agent.exploration_rate = 0.0
    #     action = self.agent.choose_action(opponent_name, COOPERATE)
    #     self.assertEqual(action, COOPERATE)

    #     # Ensure the agent can explore (choose random actions) when exploration_rate = 1
    #     self.agent.exploration_rate = 1.0
    #     actions = [self.agent.choose_action(opponent_name, COOPERATE) for _ in range(100)]
    #     self.assertIn(COOPERATE, actions)
    #     self.assertIn(DEFECT, actions)

    # def test_update_q_value(self):
    #     opponent_name = "TFTBot"
    #     self.agent.initialize_q_table_for_opponent(opponent_name)

    #     # Step 1: First update
    #     table = self.agent.get_qtables()[opponent_name]
    #     table.update_q_value(
    #         state=COOPERATE, 
    #         action=DEFECT, 
    #         learning_rate=LEARNING_RATE,  # 0.1
    #         immediate_reward=5, 
    #         discount_factor=DISCOUNT_FACTOR,  # 0.9
    #         next_state=DEFECT
    #     )

    #     # Step 2: Verify first update result
    #     curr_q = table.get_q_value(state=COOPERATE, action=DEFECT)
    #     self.assertAlmostEqual(curr_q, 0.5, 5)

    #     # Step 3: Second update - let's break it down
    #     current_q = curr_q  # Should be 0.5
    #     reward = 10
    #     next_state_max_q = max(table.get_table()[COOPERATE].values())  # Should be 0
        
    #     # Calculate expected value step by step
    #     future_value = DISCOUNT_FACTOR * next_state_max_q  # 0.9 * 0
    #     temporal_diff = reward + future_value - current_q  # 10 + 0 - 0.5
    #     update = LEARNING_RATE * temporal_diff  # 0.1 * 9.5
    #     expected = current_q + update  # 0.5 + 0.95

    #     # Step 4: Perform actual update
    #     self.agent.update_q_value(
    #         opponent_name, 
    #         state=COOPERATE, 
    #         action=DEFECT,
    #         reward=10, 
    #         next_state=COOPERATE
    #     )

    #     # Step 5: Compare results
    #     actual = self.agent.get_q_value(opponent_name, state=COOPERATE, action=DEFECT)
        
    #     # Raise an error with detailed information
    #     if abs(actual - expected) > 0.00001:
    #         raise AssertionError(
    #             f"\nCalculation breakdown:"
    #             f"\n  Current Q: {current_q}"
    #             f"\n  Reward: {reward}"
    #             f"\n  Next state max Q: {next_state_max_q}"
    #             f"\n  Future value (γ * max Q'): {future_value}"
    #             f"\n  Temporal difference: {temporal_diff}"
    #             f"\n  Update amount (α * TD): {update}"
    #             f"\n  Expected final value: {expected}"
    #             f"\n  Actual final value: {actual}"
    #             f"\n  Difference: {actual - expected}"
    #         )

    #     self.assertAlmostEqual(actual, expected, 5)

    # def test_exploration_rate_init(self):
    #     # exploration rate initialized to 1.0
    #     self.assertEqual(self.agent.get_exploration_rate(), DEFAULT_EXPLORATION_RATE)

    # def test_exploration_rate_invalid(self):
    #     # raise ValueError if out of range
    #     with self.assertRaises(ValueError):
    #         self.agent.set_exploration_rate(1.1)

    # def test_exploration_rate_decay(self):
    #     # check that init exploration rate is default exploration rate
    #     self.assertEqual(self.agent.get_exploration_rate(), DEFAULT_EXPLORATION_RATE)

    #     # Decay once
    #     self.agent.decay_exploration_rate(DECAY_RATE)
    #     self.assertAlmostEqual(DEFAULT_EXPLORATION_RATE*DECAY_RATE, self.agent.get_exploration_rate(), 5)



if __name__ == "__main__":
    unittest.main()
