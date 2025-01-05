# Strategies
COOPERATE = "Cooperate"
DEFECT = "Defect"

# bellman's equation
LEARNING_RATE = 0.2
DEFAULT_EXPLORATION_RATE = 1.0
DISCOUNT_FACTOR = 0.99
DECAY_RATE = 0.99

# Payoff matrix for the Prisoner's Dilemma
PAYOFF_MATRIX = {
    (COOPERATE, COOPERATE): (3, 3),
    (COOPERATE, DEFECT): (0, 5),
    (DEFECT, COOPERATE): (5, 0),
    (DEFECT, DEFECT): (1, 1),
}
# tournament constants
ROUND_NUM = "round_number"
ACTIONS_SUFFIX = "_actions"
PAYOFF_SUFFIX = "_total_payoff"
TOTAL_PAYOFF = "total_payoff"  
MATCHES_PLAYED = "matches_played"
COOPERATE_COUNT = "cooperate_count"
DEFECT_COUNT = "defect_count"
COOPERATION_RATE = "cooperation_rate"
ITERATIONS = 200
ROUNDS = 1000
NUM_TOURNAMENTS = 10


