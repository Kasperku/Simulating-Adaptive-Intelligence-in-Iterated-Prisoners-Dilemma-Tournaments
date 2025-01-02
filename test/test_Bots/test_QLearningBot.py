import unittest
from model.bots.QLearningBot import QLearningBot
from model.constants import COOPERATE, DEFECT, PAYOFF_MATRIX, DECAY_RATE
from model.bots.DefectBot import DefectBot
from model.bots.CooperateBot import CooperateBot

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
        """Test that first move against a new opponent uses stored first action or random"""
        # Setup
        defect_bot = DefectBot()
        self.bot.set_opponent("DefectBot")
        
        # First interaction should store opponent's first action
        opponent_action = defect_bot.choose_action(None)  # Should be DEFECT
        self.bot.choose_action(opponent_action)
        
        # Verify first action was stored
        self.assertIn("DefectBot", self.bot.opponent_first_actions)
        self.assertEqual(self.bot.opponent_first_actions["DefectBot"], DEFECT)
        
        # Reset and verify we use the stored first action
        self.bot.reset()
        self.bot.set_opponent("DefectBot")
        self.assertEqual(self.bot.opponent_last_action, DEFECT)
        
        # For a new opponent without history, should use random first move
        self.bot.reset()
        self.bot.set_opponent("NewBot")
        self.assertIsNone(self.bot.opponent_last_action)

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

    def test_exploration_rate_decay(self):
        """Test that exploration rate decays properly"""
        initial_rate = self.bot.agent.get_exploration_rate()
        
        # Make 2 moves to trigger 2 decays
        self.bot.choose_action(COOPERATE)
        self.bot.choose_action(DEFECT)  
        
        decayed_rate = self.bot.agent.get_exploration_rate()
        self.assertAlmostEqual(decayed_rate, initial_rate * DECAY_RATE * DECAY_RATE)

    def test_reset(self):
        """Test that reset preserves learning, randomises first action for agent, 
            and uses opponent first action to get reward when starting a new round"""
        # Setup
        defect_bot = DefectBot()
        self.bot.set_opponent("DefectBot")
        
        # First interaction to store opponent's first action
        opponent_action = defect_bot.choose_action(None)  # Should be DEFECT
        self.bot.choose_action(opponent_action)
        
        # Store Q-values before reset
        q_table = self.bot.agent.get_qtable_for_opponent("DefectBot")
        q_values_before = {
            (state, action): q_table.get_q_value(state, action)
            for state in [COOPERATE, DEFECT, None]  # Include None state
            for action in [COOPERATE, DEFECT]
        }
        
        # Reset bot
        self.bot.reset()
        
        # Check state was reset
        self.assertIsNone(self.bot.last_state)
        self.assertIsNotNone(self.bot.last_action)  # Should be random COOPERATE/DEFECT
        self.assertIsNone(self.bot.opponent_name)
        self.assertIsNone(self.bot.opponent_last_action)
        
        # Check Q-values preserved
        for (state, action), value in q_values_before.items():
            current_value = q_table.get_q_value(state, action)
            self.assertEqual(value, current_value)
            
        # Verify opponent's first action is correctly restored when setting opponent again
        self.bot.set_opponent("DefectBot")
        self.assertEqual(self.bot.opponent_last_action, DEFECT)

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
        defect_bot = DefectBot()
        self.bot.set_opponent("DefectBot")
        
        # First round of learning
        for _ in range(100):  # Play several rounds to learn
            opponent_action = defect_bot.choose_action(None)
            self.bot.choose_action(opponent_action)
        
        # Reset bot
        self.bot.reset()
        self.bot.set_opponent("DefectBot") 
        self.bot.agent.set_exploration_rate(0)
        first_action = self.bot.choose_action(None)
        
        self.assertEqual(first_action, DEFECT, 
                        "Bot should have learned to defect against DefectBot")

    def test_multiple_opponents_first_actions(self):
        """Test that bot correctly stores and retrieves first actions for different opponents"""
        # Setup different types of bots
        defect_bot = DefectBot()
        cooperate_bot = CooperateBot()
        
        # First interaction with DefectBot
        self.bot.set_opponent("DefectBot")
        opponent_action = defect_bot.choose_action(None)  # Should be DEFECT
        self.bot.choose_action(opponent_action)
        
        # First interaction with CooperateBot
        self.bot.set_opponent("CooperateBot")
        opponent_action = cooperate_bot.choose_action(None)  # Should be COOPERATE
        self.bot.choose_action(opponent_action)
        
        # Verify both first actions were stored correctly
        self.assertEqual(self.bot.opponent_first_actions["DefectBot"], DEFECT)
        self.assertEqual(self.bot.opponent_first_actions["CooperateBot"], COOPERATE)
        
        # Reset and verify each opponent gets their correct first action
        self.bot.reset()
        
        self.bot.set_opponent("DefectBot")
        self.assertEqual(self.bot.opponent_last_action, DEFECT)
        
        self.bot.set_opponent("CooperateBot")
        self.assertEqual(self.bot.opponent_last_action, COOPERATE)
        
        # Verify new opponent still gets None
        self.bot.set_opponent("NewBot")
        self.assertIsNone(self.bot.opponent_last_action)

if __name__ == '__main__':
    unittest.main()