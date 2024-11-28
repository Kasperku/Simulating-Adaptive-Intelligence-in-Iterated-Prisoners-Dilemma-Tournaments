from typing import Dict, List


class QTable:
    """
    Represents a Q-table for a single opponent in the Q-learning agent.

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
                                could be COOPERATE or DEFECT
            actions (List[str]): The possible actions, aka either COOPERATE or DEFECT
        """
        self.table: Dict[str, Dict[str, float]] = {
            state: {action: 0.0 for action in actions} for state in states
        }

    def get_q_value(self, state: str, action: str) -> float:
        """
        Retrieves the Q-value for a specific state-action pair.

        Args:
            state (str): The current state.
            action (str): The action taken.

        Returns:
            float: The Q-value for the state-action pair.
        """
        return self.table[state][action]
