import random
from typing import Dict, List
from model.QTable import QTable
from model.constants import COOPERATE, DEFECT, LEARNING_RATE, DISCOUNT_FACTOR, DEFAULT_EXPLORATION_RATE


class QLearningAgent:
    """
    Represents a Q-learning agent for the Prisoner's Dilemma game.

    This agent learns an optimal strategy by interacting with opponents in repeated games.
    It uses a Q-table to map state-action pairs to expected rewards and updates its strategy
    over time using the Q-learning algorithm.

    Attributes:
        learning_rate (float): The rate at which the agent updates its Q-values (α).
        discount_factor (float): The factor by which future rewards are discounted (γ).
        exploration_rate (float): The probability of taking random actions for exploration (ε).
        QTables (Dict[str, Dict[str, Dict[str, float]]]): A dictionary containing a Q-table for
            each opponent. Each Q-table maps states to actions and their Q-values.
        actions (List[str]): The possible actions the agent can take ("Cooperate" or "Defect").
    """

    def __init__(self, learning_rate: float = LEARNING_RATE,
                 discount_factor: float = DISCOUNT_FACTOR,
                 exploration_rate: float = DEFAULT_EXPLORATION_RATE,
                 actions: List[str] = [COOPERATE, DEFECT]):

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.actions = actions

        # the key of the dictionary str is the NAME of the BOT
        # the value is the QTable for that specific opponent
        self.QTables: Dict[str, QTable] = {}
        self.exploration_rates = {}  

    # Getters
    def get_learning_rate(self):
        return self.learning_rate

    def get_discount_factor(self):
        return self.discount_factor

    def get_exploration_rate(self, opponent_name: str) -> float:
        return self.exploration_rates.get(opponent_name, DEFAULT_EXPLORATION_RATE)
    
    def get_qtables(self):
        return self.QTables

    def get_qtable_for_opponent(self, opponent_name: str):
        if opponent_name not in self.QTables:
            self.initialize_q_table_for_opponent(opponent_name)
        return self.QTables.get(opponent_name)
    
    def get_q_value(self, opponent_name: str, state: str, action: str) -> float:
        if opponent_name not in self.QTables:
            self.initialize_q_table_for_opponent(opponent_name)
        return self.get_qtable_for_opponent(opponent_name).get_q_value(state, action)
    
    # Setters
    def set_exploration_rate(self, opponent_name: str, rate: float) -> None:
        if not 0 <= rate <= 1:
            raise ValueError("Exploration rate must be between 0 and 1")
        self.exploration_rates[opponent_name] = rate
    
    def set_qtable_for_opponent(self, opponent_name: str, qtable: QTable):
        self.QTables[opponent_name] = qtable
    

    def decay_exploration_rate(self, opponent_name: str, decay_rate: float) -> None:
        """Decay exploration rate for specific opponent"""
        old_rate = self.get_exploration_rate(opponent_name)
        new_rate = old_rate * decay_rate
        self.set_exploration_rate(opponent_name, new_rate)

    def initialize_q_table_for_opponent(self, opponent_name: str):
        """Initialize Q-table for a new opponent"""
        if opponent_name not in self.QTables:
            self.set_qtable_for_opponent(opponent_name, QTable(states=self.actions, actions=self.actions))

    def initialize_exploration_rate(self, opponent_name: str):
        """Initialize exploration rate for a new opponent"""
        if opponent_name not in self.exploration_rates:
            self.exploration_rates[opponent_name] = DEFAULT_EXPLORATION_RATE


    def update_q_value(self, opponent_name: str, state: str, action: str,
                       reward: float, next_state: str):
        """
        Updates the Q-value for a state-action pair using the Q-learning formula.
        """
        
        if opponent_name not in self.QTables:
            self.initialize_q_table_for_opponent(opponent_name)

        table = self.get_qtable_for_opponent(opponent_name)

        table.update_q_value(state, action, self.get_learning_rate(), reward,
                             self.get_discount_factor(), next_state)


    def choose_action(self, opponent_name: str, state: str) -> str:
        """
        Selects an action for the agent using the ε-greedy policy.

        Args:
            opponent_name (str): The name of the opponent the agent is playing against.
            state (str): The current state (e.g., the opponent's last move).

        Returns:
            str: The action that yields the highest payoff
        """
        if random.random() < self.get_exploration_rate(opponent_name):
            return random.choice([COOPERATE, DEFECT])
        else:
            q_table = self.get_qtable_for_opponent(opponent_name)
            state_actions = q_table.get_table()[state]
            return max(state_actions, key=state_actions.get)


    # # HELPER FUNCTION
    # def _choose_best_action(self, opponent_name: str, state: str) -> List[str]:
    #     table = self.get_qtable_for_opponent(opponent_name)
    #     defect_payoff = table.get_q_value(state, DEFECT)
    #     cooperate_payoff = table.get_q_value(state, COOPERATE)
    #     best_actions = []

    #     if defect_payoff > cooperate_payoff:
    #         best_actions.append(DEFECT)
    #     elif defect_payoff < cooperate_payoff:
    #         best_actions.append(COOPERATE)
    #     else:  
    #         best_actions.extend([DEFECT, COOPERATE])

    #     return best_actions






