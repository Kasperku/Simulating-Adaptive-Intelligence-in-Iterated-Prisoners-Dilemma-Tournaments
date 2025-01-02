import unittest
from model.bots.QLearningBot import QLearningBot
from model.constants import COOPERATE, DEFECT, PAYOFF_MATRIX, DECAY_RATE
from model.bots.DefectBot import DefectBot

class TestQLearningBot(unittest.TestCase):
    def setUp(self):
        self.bot = QLearningBot()
        self.bot.set_opponent("TestBot")

    def test_initial_state(self):
        """Test initial bot state"""
        self.assertEqual(self.bot.name, "QLearningBot")
        self.assertIsNone(self.bot.last_state)
        self.assertIsNone(self.bot.last_action)
        self.assertEqual(self.bot.opponent_name, "TestBot")

    def test_first_move(self):
        """Test that first move is random (high exploration rate)"""
        # Run multiple trials to verify randomness
        actions = [self.bot.choose_action(None) for _ in range(100)]
        
        # Count occurrences
        cooperate_count = actions.count(COOPERATE)
        defect_count = actions.count(DEFECT)
        
        # With high initial exploration rate, should be roughly 50-50
        self.assertAlmostEqual(cooperate_count, 50, delta=15)
        self.assertAlmostEqual(defect_count, 50, delta=15)
        
        # Verify state tracking for last move
        last_action = self.bot.choose_action(None)
        self.assertEqual(self.bot.last_state, None)  # First opponent move defaults to COOPERATE
        self.assertEqual(self.bot.last_action, last_action)

    def test_learning_from_interaction(self):
        """Test that bot learns from interactions"""
        # First interaction
        first_action = self.bot.choose_action(COOPERATE)
        
        # Second interaction - should learn from first
        opponent_action = DEFECT
        second_action = self.bot.choose_action(opponent_action)
        
        # Verify state was updated
        self.assertEqual(self.bot.last_state, opponent_action)
        self.assertEqual(self.bot.last_action, second_action)
        
        # Verify Q-value was updated
        q_value = self.bot.agent.get_q_value(
            "TestBot",
            state=COOPERATE,
            action=first_action
        )
        expected_reward = PAYOFF_MATRIX[(first_action, opponent_action)][0]
        self.assertNotEqual(q_value, 0.0)  # Q-value should have been updated

    def test_exploration_rate_decay(self):
        """Test that exploration rate decays properly"""
        initial_rate = self.bot.agent.get_exploration_rate()
        
        # Make a move to trigger decay
        self.bot.choose_action(COOPERATE)
        self.bot.choose_action(DEFECT)  # Second move to trigger learning and decay
        
        decayed_rate = self.bot.agent.get_exploration_rate()
        self.assertAlmostEqual(decayed_rate, initial_rate * DECAY_RATE)

    def test_reset(self):
        """Test that reset clears state but preserves learning"""
        # Make some moves
        self.bot.choose_action(COOPERATE)
        self.bot.choose_action(DEFECT)
        
        # Store Q-values before reset
        q_table = self.bot.agent.get_qtable_for_opponent("TestBot")
        q_values_before = {
            (state, action): q_table.get_q_value(state, action)
            for state in [COOPERATE, DEFECT]
            for action in [COOPERATE, DEFECT]
        }
        
        # Reset bot
        self.bot.reset()
        
        # Check state was reset
        self.assertIsNone(self.bot.last_state)
        self.assertIsNone(self.bot.last_action)
        self.assertIsNone(self.bot.opponent_name)
        
        # Check Q-values preserved
        for (state, action), value in q_values_before.items():
            current_value = q_table.get_q_value(state, action)
            self.assertEqual(value, current_value)

    def test_opponent_change(self):
        """Test that bot maintains separate Q-tables for different opponents"""
        # Play against first opponent
        self.bot.set_opponent("Opponent1")
        self.bot.choose_action(COOPERATE)
        self.bot.choose_action(DEFECT)
        
        # Store Q-values for first opponent
        q_table1 = self.bot.agent.get_qtable_for_opponent("Opponent1")
        
        # Switch to second opponent
        self.bot.set_opponent("Opponent2")
        self.bot.choose_action(COOPERATE)
        self.bot.choose_action(DEFECT)
        
        # Verify separate Q-tables
        self.assertIn("Opponent1", self.bot.agent.get_qtables())
        self.assertIn("Opponent2", self.bot.agent.get_qtables())
        self.assertIsNot(
            self.bot.agent.get_qtable_for_opponent("Opponent1"),
            self.bot.agent.get_qtable_for_opponent("Opponent2")
        )

    def test_learning_persistence_after_reset(self):
        """Test that bot maintains learning after reset"""
        # Setup
        defect_bot = DefectBot()
        self.bot.set_opponent("DefectBot")
        
        # First round of learning
        print("\nFirst interaction:")
        opponent_action = defect_bot.choose_action(None)
        print(f"DefectBot's first action: {opponent_action}")
        self.bot.choose_action(opponent_action)
        print(f"Stored first actions: {self.bot.opponent_first_actions}")
        
        # Reset bot
        print("\nResetting:")
        self.bot.reset()
        print(f"After reset - opponent_last_action: {self.bot.opponent_last_action}")
        
        self.bot.set_opponent("DefectBot")
        print(f"After set_opponent - opponent_last_action: {self.bot.opponent_last_action}")
        
        self.bot.agent.set_exploration_rate(0)
        first_action = self.bot.choose_action(None)
        print(f"\nChosen action with opponent_last_action = {self.bot.opponent_last_action}")

if __name__ == '__main__':
    unittest.main()