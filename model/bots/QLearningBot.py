from typing import Optional, Dict
from model.bots.BaseBot import BaseBot
from model.QLearningAgent import QLearningAgent
from model.constants import COOPERATE, DEFECT, PAYOFF_MATRIX, DECAY_RATE
from model.logging.InteractionLogger import InteractionLogger
import random

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
        self.opponent_first_actions = {}  # Store first action for each opponent
        self.logger = InteractionLogger()
        self.tournament_num = 0
        self.round_num = 0
        self.turn_num = 0
    
    def _get_current_q_values(self, current_state: str) -> Dict[str, float]:
        """Get current Q-values for both actions"""
        return {
            'COOPERATE': self.agent.get_q_value(self.opponent_name, current_state, COOPERATE),
            'DEFECT': self.agent.get_q_value(self.opponent_name, current_state, DEFECT)
        }

    def _handle_first_action(self, opponent_last_action: Optional[str]) -> str:
        """Handle and store first action from opponent"""
        if opponent_last_action is None:
            return self.opponent_last_action
            
        if self.opponent_name and self.opponent_name not in self.opponent_first_actions:
            self.opponent_first_actions[self.opponent_name] = opponent_last_action
        return opponent_last_action

    def _learn_from_previous_interaction(self, current_state: str, opponent_last_action: str) -> Optional[float]:
        """Learn from previous interaction and return reward if applicable"""
        if self.last_action is None or opponent_last_action is None:
            return None
            
        reward = PAYOFF_MATRIX[(self.last_action, opponent_last_action)][0]
        self.agent.update_q_value(
            self.opponent_name,
            state=self.last_state,
            action=self.last_action,
            reward=reward,
            next_state=current_state
        )
        return reward

    def _log_interaction(self, current_state: str, reward: Optional[float], q_values: Dict[str, float]) -> None:
        """Log the current interaction"""
        if self.last_action is not None:  # Only log if we have a previous action
            self.logger.log_interaction(
                tournament_num=self.tournament_num,
                round_num=self.round_num,
                turn_num=self.turn_num,
                agent_name=self.name,
                opponent_name=self.opponent_name,
                state=str(current_state),
                action_taken=self.last_action,
                reward=reward if reward is not None else 0.0,
                q_values=q_values,
                exploration_rate=self.agent.get_exploration_rate(self.opponent_name)
            )

    def _store_state_and_action(self, current_state: str, action: str) -> None:
        """Store current state and action for next learning update"""
        self.last_state = current_state
        self.last_action = action

    def _decay_exploration_rate(self) -> None:
        """Decay exploration rate for current opponent"""
        if self.opponent_name:
            self.agent.decay_exploration_rate(self.opponent_name, DECAY_RATE)

    def choose_action(self, opponent_last_action: Optional[str]) -> str:
        """Update learning from last interaction and choose next action"""
        # Handle first action logic
        current_state = self._handle_first_action(opponent_last_action)
        
        # Learn from previous interaction
        reward = self._learn_from_previous_interaction(current_state, opponent_last_action)
        
        # Get current Q-values
        q_values = self._get_current_q_values(current_state)
        
        # Log interaction
        self._log_interaction(current_state, reward, q_values)
        
        # Choose action for current state
        action = self.agent.choose_action(self.opponent_name, current_state)
        
        # Store state and action
        self._store_state_and_action(current_state, action)

        # Update exploration rate
        self._decay_exploration_rate()
        
        return action

    def set_opponent(self, opponent_name: str) -> None:
        self.opponent_name = opponent_name
        # Get stored first action for this opponent if we have one
        self.opponent_last_action = self.opponent_first_actions.get(opponent_name, None)
        # Initialize separate Q-table and exploration rate
        self.agent.initialize_q_table_for_opponent(opponent_name)
        self.agent.initialize_exploration_rate(opponent_name)

    def reset(self) -> None:
        self.last_state = None
        self.last_action = random.choice([COOPERATE, DEFECT])
        # Store the current opponent name before resetting it
        current_opponent = self.opponent_name
        self.opponent_name = None
        self.opponent_last_action = None

        