import unittest

from model.QTable import QTable
from model.QLearningAgent import QLearningAgent
from model.constants import COOPERATE, DEFECT


class TestQLearningAgent(unittest.TestCase):
    def setUp(self):
        """
        Sets up the testing environment before each test.
        """
        self.actions = [COOPERATE, DEFECT]
        self.agent = QLearningAgent(actions=self.actions)

    def test_initialize_q_table_for_opponent(self):
        """
        Tests whether QTables are correctly initialized for opponents.
        """
        opponent_name = "TFTBot"

        # Ensure the QTable is not present initially
        self.assertNotIn(opponent_name, self.agent.QTables)

        # Initialize QTable for the opponent
        self.agent.initialize_q_table_for_opponent(opponent_name)

        # Check if the QTable is now present
        self.assertIn(opponent_name, self.agent.QTables)
        self.assertIsInstance(self.agent.QTables[opponent_name], QTable)

        # Verify the QTable's structure
        q_table = self.agent.QTables[opponent_name]
        for state in self.actions:
            for action in self.actions:
                self.assertEqual(q_table.get_q_value(state, action), 0.0)

    def test_get_q_value_existing_opponent(self):
        """
        Tests retrieving Q-values for an opponent with an existing QTable.
        """
        opponent_name = "AlwaysDefectBot"
        self.agent.initialize_q_table_for_opponent(opponent_name)

        # Set a Q-value for testing
        self.agent.QTables[opponent_name].update_q_value(
            state=COOPERATE,
            action=DEFECT,
            learning_rate=0.1,
            immediate_reward=5,
            discount_factor=0.9,
            next_state=DEFECT
        )

        # Retrieve the Q-value and verify correctness
        q_value = self.agent.get_q_value(opponent_name, COOPERATE, DEFECT)
        self.assertGreater(q_value, 0.0)  # Verify it has been updated

    def test_get_q_value_new_opponent(self):
        """
        Tests retrieving Q-values for a new opponent without a QTable.
        """
        opponent_name = "NewOpponent"

        # Ensure the QTable does not exist initially
        self.assertNotIn(opponent_name, self.agent.QTables)

        # Retrieve a Q-value for the new opponent
        q_value = self.agent.get_q_value(opponent_name, COOPERATE, DEFECT)

        # Verify that a QTable was created and the default Q-value is returned
        self.assertIn(opponent_name, self.agent.QTables)
        self.assertEqual(q_value, 0.0)

    def test_initialize_q_table_twice(self):
        """
        Tests that initializing a QTable for the same opponent twice does not overwrite existing data.
        """
        opponent_name = "GrimBot"
        self.agent.initialize_q_table_for_opponent(opponent_name)

        # Set a Q-value for the opponent
        self.agent.QTables[opponent_name].update_q_value(
            state=DEFECT,
            action=DEFECT,
            learning_rate=0.1,
            immediate_reward=3,
            discount_factor=0.9,
            next_state=DEFECT
        )

        # Re-initialize the same opponent
        self.agent.initialize_q_table_for_opponent(opponent_name)

        # Verify that the Q-value is not reset
        q_value = self.agent.get_q_value(opponent_name, DEFECT, DEFECT)
        self.assertGreater(q_value, 0.0)

    def test_epsilon_greedy_action_selection(self):
        """
        Tests the agent's ε-greedy policy for action selection.
        Our agent against a TFT Bot with the last action COOPERATE should continue to COOPERATE
        when the exploration rate is 0 and should randomize when exploration rate is 1
        """
        opponent_name = "TFTBot"
        self.agent.initialize_q_table_for_opponent(opponent_name)

        # Mock Q-values, the reward for COOPERATE(10) > DEFECT
        self.agent.QTables[opponent_name].update_q_value(COOPERATE, DEFECT, 0.1, 5, 0.9, DEFECT)
        self.agent.QTables[opponent_name].update_q_value(COOPERATE, COOPERATE, 0.1, 10, 0.9, DEFECT)

        # Ensure the agent can exploit (choose the best action) when exploration_rate = 0
        self.agent.exploration_rate = 0.0
        action = self.agent.choose_action(opponent_name, COOPERATE)
        self.assertEqual(action, COOPERATE)

        # Ensure the agent can explore (choose random actions) when exploration_rate = 1
        self.agent.exploration_rate = 1.0
        actions = [self.agent.choose_action(opponent_name, COOPERATE) for _ in range(100)]
        self.assertIn(COOPERATE, actions)
        self.assertIn(DEFECT, actions)



if __name__ == "__main__":
    unittest.main()
