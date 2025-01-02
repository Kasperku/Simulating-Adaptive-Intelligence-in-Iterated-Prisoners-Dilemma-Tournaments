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
    
        # Learn from previous interaction if we have one
        if self.last_state is not None and self.last_action is not None:
            reward = PAYOFF_MATRIX[(self.last_action, opponent_last_action)][0]  
            
            self.agent.update_q_value(
                self.opponent_name,
                state=self.last_state,
                action=self.last_action,
                reward=reward,
                next_state=opponent_last_action
            )
            
            # Decay exploration rate after each interaction
            self.agent.decay_exploration_rate(DECAY_RATE)
            
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
        """Reset the bot's state for a new tournament"""
        self.opponent_name = None
        self.last_state = None
        self.last_action = None
        self.opponent_last_action = None
        # Note: Don't reset self.agent as we want to preserve learning across tournaments