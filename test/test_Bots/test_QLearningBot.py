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
        self.bot.set_opponent("TestBot")
        
        # First interaction - bot defects against cooperation
        first_action = DEFECT  # Force DEFECT to ensure non-zero reward
        self.bot.last_action = first_action  # Set up the action
        self.bot.last_state = COOPERATE  # Set up the state
        initial_q = self.bot.agent.get_q_value("TestBot", COOPERATE, first_action)
        
        # Learn from interaction where we DEFECT against COOPERATE (reward = 5)
        self.bot.learn_from_interaction(first_action, COOPERATE)
        
        # Get Q-value after learning
        updated_q = self.bot.agent.get_q_value(
            "TestBot",
            state=COOPERATE,
            action=first_action
        )
        
        # Q-value should change after learning
        self.assertNotEqual(initial_q, updated_q, 
            "Q-value should be updated after interaction")
        
        # Q-value should reflect the reward from payoff matrix (5 for defecting against cooperation)
        expected_reward = PAYOFF_MATRIX[(first_action, COOPERATE)][0]  # Should be 5
        self.assertGreater(updated_q, initial_q, 
            f"Q-value should increase from {initial_q} to {updated_q} with reward {expected_reward}")

    def test_exploration_rate_decay(self):
        """Test that exploration rate decays properly and independently for each opponent"""
        # Setup first opponent
        self.bot.set_opponent("Opponent1")
        initial_rate1 = self.bot.agent.get_exploration_rate("Opponent1")
        
        # Make moves and learn against first opponent
        action1 = self.bot.choose_action(COOPERATE)
        self.bot.learn_from_interaction(action1, COOPERATE)
        
        action2 = self.bot.choose_action(DEFECT)
        self.bot.learn_from_interaction(action2, DEFECT)
        
        # Check decay for first opponent
        decayed_rate1 = self.bot.agent.get_exploration_rate("Opponent1")
        self.assertAlmostEqual(decayed_rate1, initial_rate1 * DECAY_RATE * DECAY_RATE)
        
        # Setup second opponent
        self.bot.set_opponent("Opponent2")
        initial_rate2 = self.bot.agent.get_exploration_rate("Opponent2")
        
        # Make one move and learn against second opponent
        action3 = self.bot.choose_action(COOPERATE)
        self.bot.learn_from_interaction(action3, COOPERATE)
        
        # Check rates
        self.assertAlmostEqual(
            self.bot.agent.get_exploration_rate("Opponent2"), 
            initial_rate2 * DECAY_RATE,
            msg="Second opponent's rate should decay once"
        )
        self.assertAlmostEqual(
            self.bot.agent.get_exploration_rate("Opponent1"),
            decayed_rate1,
            msg="First opponent's rate should remain unchanged"
        )

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
            self.bot.learn_from_interaction(self.bot.choose_action(opponent_action), opponent_action)
        
        # Reset bot
        self.bot.reset()
        self.bot.set_opponent("DefectBot") 
        self.bot.agent.set_exploration_rate("DefectBot", 0)
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