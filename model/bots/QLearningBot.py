from typing import Optional
from model.bots.BaseBot import BaseBot
from model.QLearningAgent import QLearningAgent
from model.constants import COOPERATE, DEFECT, PAYOFF_MATRIX, DECAY_RATE

class QLearningBot(BaseBot):
    """
    A wrapper bot that uses QLearningAgent to make decisions.
    This bot implements the BaseBot interface while delegating decision-making to QLearningAgent.
    """

    def __init__(self):
        super().__init__(name="QLearningBot")
        self.agent = QLearningAgent()
        self.opponent_name = None
        self.last_state = None
        self.last_action = None
        self.opponent_last_action = None

    def choose_action(self, opponent_last_action: Optional[str]) -> str:
        """Delegates the decision to the QLearningAgent and learns from previous interaction"""
        if opponent_last_action is None:
            opponent_last_action = COOPERATE
            
        # Set opponent name if not set (should be done by tournament, but as fallback)
        if self.opponent_name is None:
            self.opponent_name = "Unknown"
            
        # Initialize Q-table for new opponents (do this first!)
        if self.opponent_name not in self.agent.get_qtables():
            self.agent.initialize_q_table_for_opponent(self.opponent_name)
            
        # Learn from previous interaction if we have one
        if self.last_state is not None and self.last_action is not None:
            # Calculate reward from last interaction
            my_action = self.last_action
            opp_action = self.opponent_last_action
            reward = PAYOFF_MATRIX[(my_action, opp_action)][0]  # Get our payoff
            
            # Debug print
            #print(f"Q-Learning Update - State: {self.last_state}, Action: {my_action}, Reward: {reward}")
            #print(f"Current Q-values - Defect: {self.agent.get_qtables()[self.opponent_name].get_q_value(self.last_state, DEFECT)}, Cooperate: {self.agent.get_qtables()[self.opponent_name].get_q_value(self.last_state, COOPERATE)}")
            
            self.agent.update_q_value(
                self.opponent_name,
                state=self.last_state,
                action=self.last_action,
                reward=reward,
                next_state=opponent_last_action
            )
            
            # Decay exploration rate after each interaction
            self.agent.decay_exploration_rate(DECAY_RATE)
            
            # Debug print after update
            #print(f"Updated Q-values - Defect: {self.agent.get_qtables()[self.opponent_name].get_q_value(self.last_state, DEFECT)}, Cooperate: {self.agent.get_qtables()[self.opponent_name].get_q_value(self.last_state, COOPERATE)}")
            #print(f"Exploration rate: {self.agent.get_exploration_rate()}")
            
        # Choose next action
        action = self.agent.choose_action(self.opponent_name, opponent_last_action)
        
        # Store state and action for next learning update
        self.last_state = opponent_last_action
        self.last_action = action
        self.opponent_last_action = opponent_last_action
        
        return action

    def set_opponent(self, opponent_name: str) -> None:
        """Sets the name of the current opponent"""
        self.opponent_name = opponent_name

    def reset(self) -> None:
        """Reset the bot's state for a new match, but preserve learning"""
        pass