from typing import Optional
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

    def choose_action(self, opponent_last_action: Optional[str]) -> str:
        # If opponent_last_action is None, use our stored first action
        if opponent_last_action is None:
            opponent_last_action = self.opponent_last_action

        # Store first action we see from this opponent
        if self.opponent_name and opponent_last_action is not None:
            if self.opponent_name not in self.opponent_first_actions:
                self.opponent_first_actions[self.opponent_name] = opponent_last_action

        current_state = opponent_last_action
        
        # Learn from previous interaction
        if self.last_action is not None:
            reward = PAYOFF_MATRIX[(self.last_action, opponent_last_action)][0]
            self.agent.update_q_value(
                self.opponent_name,
                state=None if self.last_state is None else self.last_state,  # Preserve None state
                action=self.last_action,
                reward=reward,
                next_state=current_state
            )
            
            # Get Q-values using agent methods
            current_q_values = {
                'COOPERATE': self.agent.get_q_value(self.opponent_name, current_state, COOPERATE),
                'DEFECT': self.agent.get_q_value(self.opponent_name, current_state, DEFECT)
            }
            
            self.logger.log_interaction(
                tournament_num=self.tournament_num,
                round_num=self.round_num,
                turn_num=self.turn_num,
                agent_name=self.name,
                opponent_name=self.opponent_name,
                state=str(current_state),
                action_taken=self.last_action,
                reward=reward,
                q_values=current_q_values,
                exploration_rate=self.agent.get_exploration_rate()
            )
        
        # Choose action for current state
        action = self.agent.choose_action(self.opponent_name, current_state)
        
        # Store state and action for next learning update
        self.last_state = current_state
        self.last_action = action

        self.agent.decay_exploration_rate(DECAY_RATE)
        
        return action

    def set_opponent(self, opponent_name: str) -> None:
        self.opponent_name = opponent_name

    def reset(self) -> None:
        self.last_state = None
        self.last_action = random.choice([COOPERATE, DEFECT])
        # Store the current opponent name before resetting it
        current_opponent = self.opponent_name
        self.opponent_last_action = (
            self.opponent_first_actions.get(current_opponent, None)
            if current_opponent
            else None
        )
        # Now we can reset the opponent name
        self.opponent_name = None

    def notify_turn_result(self, my_action: str, opponent_action: str, opponent_name: str) -> None:
        """Learn from the turn result immediately"""
        reward = PAYOFF_MATRIX[(my_action, opponent_action)][0]
        self.agent.update_q_value(
            opponent_name,
            state=self.last_state,
            action=my_action,
            reward=reward,
            next_state=opponent_action
        )
        self.last_state = opponent_action