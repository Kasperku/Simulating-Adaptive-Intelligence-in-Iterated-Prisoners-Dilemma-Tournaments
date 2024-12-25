# Strategies
COOPERATE = "Cooperate"
DEFECT = "Defect"

# bellman's equation
LEARNING_RATE = 0.1
DEFAULT_EXPLORATION_RATE = 1
DISCOUNT_FACTOR = 0.9
DECAY_RATE = 0.99

# Payoff matrix for the Prisoner's Dilemma
PAYOFF_MATRIX = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1),
}
