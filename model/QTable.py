from typing import Dict, List
from model.constants import COOPERATE, DEFECT

class QTable:
    """
    Represents a Q-table for a single opponent in the Q-learning agent

    Attributes:
        states (List[str]): The possible states (e.g., opponent's last action).
        actions (List[str]): The possible actions (e.g., "Cooperate" or "Defect").
        table (Dict[str, Dict[str, float]]): The Q-table mapping states to actions and Q-values.
    """

    def __init__(self, states: List[str], actions: List[str]):
        """
        Initializes the QTable with the given states and actions.

        Args:
            states (List[str]): The possible states, aka opponents last action, which
                                could be COOPERATE or DEFECT or None
            actions (List[str]): The possible actions, aka either COOPERATE or DEFECT or None
        """
        self.table = {
            None: {COOPERATE: 0.0, DEFECT: 0.0},  
            COOPERATE: {COOPERATE: 0.0, DEFECT: 0.0},
            DEFECT: {COOPERATE: 0.0, DEFECT: 0.0}
        }

    # Getters
    def get_table(self) -> dict: 
        return self.table
        
    def get_q_value(self, state: str, action: str) -> float:
        return self.table[state][action]

    # Setters
    def set_q_value(self, state: str, action: str, value: float):
        self.table[state][action] = value



    def update_q_value(self, state: str, action: str,
                       learning_rate: float, immediate_reward: float,
                       discount_factor: float, next_state: str):
        """
        Updates the Q-value for a specific state-action pair using the Bellman equation.
        𝑄(𝑠,𝑎)←𝑄(𝑠,𝑎)+𝛼[𝑟+𝛾max⁡𝑄(𝑠′,𝑎′)−𝑄(𝑠,𝑎)]

        Args:
            state (str): The current state.
            action (str): The action taken.
            learning_rate (float): The learning rate (alpha).
            immediate_reward (float): The immediate reward received.
            discount_factor (float): The discount factor (gamma).
            next_state (str): The next state observed after taking the action.

        Returns:
            None: Updates the Q-table in-place.
        """
        if state not in self.table:
            self.table[state] = {COOPERATE: 0.0, DEFECT: 0.0}
        if next_state not in self.table:
            self.table[next_state] = {COOPERATE: 0.0, DEFECT: 0.0}

        current_q_value = self.get_q_value(state, action)
        max_future_q_value = max(self.get_table()[next_state].values())

        # By the bellman equation
        new_q_value = current_q_value + learning_rate * (
                immediate_reward + (discount_factor * max_future_q_value) - current_q_value
        )

        # Update the QTable
        self.set_q_value(state, action, new_q_value)

