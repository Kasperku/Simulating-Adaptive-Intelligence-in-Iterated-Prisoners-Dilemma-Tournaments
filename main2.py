from model.QLearningAgent import QLearningAgent
from model.bots.TFTBot import TFTBot
from model.bots.DefectBot import DefectBot
from model.bots.CooperateBot import CooperateBot
from model.bots.GrimBot import GrimBot
from model.constants import PAYOFF_MATRIX, DISCOUNT_FACTOR, COOPERATE, DECAY_RATE

def play_game(agent, opponent, discount_factor):
    """
    Simulates a game between the agent and the opponent over multiple iterations.
    """
    opponent_name = type(opponent).__name__
    
    # Initialize Q-table for this opponent
    agent.initialize_q_table_for_opponent(opponent_name)
    agent.initialize_exploration_rate(opponent_name)
    
    agent_last_action = None
    opponent_last_action = None

    for iteration in range(100):  # Number of iterations in the game
        # Both bots choose their actions
        agent_action = agent.choose_action(opponent_name, opponent_last_action)
        opponent_action = opponent.choose_action(agent_last_action)
        
        # Handle None from opponent's first move
        if opponent_action is None:
            opponent_action = COOPERATE

        # Print out the actions
        print(f"Iteration {iteration + 1}:")
        print(f"  Agent Action: {agent_action}")
        print(f"  Opponent ({opponent_name}) Action: {opponent_action}")

        # Determine payoffs based on the payoff matrix
        agent_reward = PAYOFF_MATRIX[(agent_action, opponent_action)][0]

        # Update the agent's Q-table with the current state and action
        agent.update_q_value(
            opponent_name=opponent_name,
            state=opponent_last_action if opponent_last_action is not None else COOPERATE,
            action=agent_action,
            reward=agent_reward,
            next_state=opponent_action
        )

        # Update last actions for next iteration
        agent_last_action = agent_action
        opponent_last_action = opponent_action

def run_experiment():
    agent = QLearningAgent()
    opponents = [
        TFTBot()
    ]
    
    # Play against each opponent multiple times
    for opponent in opponents:
        opponent_name = type(opponent).__name__
        print(f"\nStarting matches against {opponent_name}")
        
        for game in range(1000):  # Play 1000 games against each opponent
            play_game(agent, opponent, DISCOUNT_FACTOR)
            agent.decay_exploration_rate(opponent_name, DECAY_RATE)
            
        # Print the Q-table for this opponent
        q_table = agent.get_qtable_for_opponent(opponent_name)
        print(f"\nFinal Q-table for {opponent_name}:")
        print(q_table.get_table())

if __name__ == "__main__":
    run_experiment()

def i_love_kasper():
    print("I love Kasper")