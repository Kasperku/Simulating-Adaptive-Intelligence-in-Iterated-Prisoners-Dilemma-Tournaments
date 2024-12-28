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
                 actions: List[str] = []):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

        if actions:
            self.actions = actions
        else:
            self.actions = [COOPERATE, DEFECT]

        # the key of the dictionary str is the NAME of the BOT
        # the value is the QTable for that specific opponent
        self.QTables: Dict[str, QTable] = {}

    def get_learning_rate(self):
        return self.learning_rate

    def get_discount_factor(self):
        return self.discount_factor

    def get_exploration_rate(self):
        return self.exploration_rate

    def set_exploration_rate(self, exploration_rate):
        if not (0.0 <= exploration_rate <= 1.0):
            raise ValueError("Exploration rate must be between 0 and 1")
        self.exploration_rate = exploration_rate

    def get_qtables(self):
        return self.QTables

    def initialize_q_table_for_opponent(self, opponent_name: str):
        """
        Creates a QTable for the given opponent if it doesn't already exist.

        Args:
            opponent_name (str): The name of the opponent (e.g., "TFTBot").
        """
        if opponent_name not in self.QTables:
            # Create a new QTable with states and actions
            self.QTables[opponent_name] = QTable(states=self.actions, actions=self.actions)

    def initialize_qtable_for_opponent(self, opponent_name: str):
        """
        Creates a QTable for the given opponent if it doesn't already exist.

        Args:
            opponent_name (str): The name of the opponent (e.g., "TFTBot").
        """
        if opponent_name not in self.QTables:
            self.get_qtables()[opponent_name] = QTable(states=self.actions, actions=self.actions)

    def get_q_value(self, opponent_name: str, state: str, action: str) -> float:
        """
        Retrieves the Q-value for a specific opponent, state, and action.
        Initializes a QTable for the opponent if it does not exist.
        """

        if opponent_name not in self.QTables:
            self.initialize_q_table_for_opponent(opponent_name)

        # Retrieve the Q-value from the QTable
        return self.QTables[opponent_name].get_q_value(state, action)

    """
    Selects an action for the agent using the ε-greedy policy.

    Args:
        opponent_name (str): The name of the opponent the agent is playing against.
        state (str): The current state (e.g., the opponent's last move).

    Returns:
        str: The action that yields the highest payoff, either one if tie
    """

    def choose_action(self, opponent_name, state):
        table = self.get_qtables().get(opponent_name)

        if random.random() < self.get_exploration_rate():
            return random.choice([COOPERATE, DEFECT])
        else:
            best_actions = self.choose_best_action(opponent_name, state)
            return random.choice(best_actions)

    """
    HELPER FUNC for choose_best_action
    Returns:
        List[str]; List of actions that yield max payoff
    """

    def choose_best_action(self, opponent_name: str, state: str) -> List[str]:
        table = self.get_qtables().get(opponent_name)
        defect_payoff = table.get_q_value(state, DEFECT)
        cooperate_payoff = table.get_q_value(state, COOPERATE)
        best_actions = []

        if defect_payoff > cooperate_payoff:
            best_actions.append(DEFECT)
        elif defect_payoff < cooperate_payoff:
            best_actions.append(COOPERATE)
        else:  # equal payoffs
            best_actions.extend([DEFECT, COOPERATE])

        return best_actions

    """
    Updates the Q-value for a state-action pair using the Q-learning formula.

    Args:
        opponent_name (str): The name of the opponent.
        state (str): The current state.
        action (str): The action taken.
        reward (float): The immediate reward received.
        next_state (str): The state resulting from the action.
    returns:
        none
    """
    def update_q_value(self, opponent_name: str, state: str, action: str,
                       reward: float, next_state: str):

        table = self.get_qtables()[opponent_name]

        table.update_q_value(state, action, self.get_learning_rate(), reward,
                             self.get_discount_factor(), next_state)



    def decay_exploration_rate(self, decay_rate: float):
        self.set_exploration_rate(self.get_exploration_rate()*decay_rate)
