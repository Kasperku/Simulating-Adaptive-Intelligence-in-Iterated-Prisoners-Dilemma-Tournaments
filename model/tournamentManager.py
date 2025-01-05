from model.QLearningAgent import QLearningAgent
from model.bots.BaseBot import BaseBot
from model.bots.TFTBot import TFTBot
from model.bots.DefectBot import DefectBot
from model.bots.CooperateBot import CooperateBot
from model.bots.GrimBot import GrimBot
from model.bots.TFT90Bot import TFT90Bot
from model.constants import *
from model.logging.InteractionLogger import InteractionLogger
from model.logging.csv_export import export_tournament_stats


def play_game(bot1, bot2, discount_factor, logger, game_number, stats):
    """
    Simulates a game between two bots and returns the winner based on total payoff.
    """
    bot1_name = type(bot1).__name__
    bot2_name = type(bot2).__name__
    
    # Initialize stats for both bots
    initialize_bot_stats(stats, bot1_name)
    initialize_bot_stats(stats, bot2_name)
    
    # Initialize Q-table only if bot is QLearningAgent
    initialize_Q_table_for_agent(bot1, bot2_name)
    initialize_Q_table_for_agent(bot2, bot1_name)
    
    bot1_last_action = None
    bot2_last_action = None

    for iteration in range(ITERATIONS): 
        # Both bots choose their actions
        bot1_action = bot1.choose_action(bot2_name, bot2_last_action)
        bot2_action = bot2.choose_action(bot1_name, bot1_last_action)
        
        # Update statistics
        update_bot_stats(stats, bot1_name, bot1_action)
        update_bot_stats(stats, bot2_name, bot2_action)
        
        # Calculate and update payoffs
        bot1_reward, bot2_reward = calculate_and_update_payoffs(
            stats, bot1_name, bot2_name, bot1_action, bot2_action)
        
        # Get current Q-values for logging
        if isinstance(bot1, QLearningAgent):
            q_table = bot1.get_qtable_for_opponent(bot2_name)
            current_q_values = get_current_q_values(q_table, bot2_last_action)
            
            # Log the interaction
            logger.log_interaction(
                tournament_num=1,
                round_num=game_number,
                turn_num=iteration,
                agent_name=bot1_name,
                opponent_name=bot2_name,
                state=str(bot2_last_action if bot2_last_action is not None else COOPERATE),
                action_taken=bot1_action,
                reward=bot1_reward,
                q_values=current_q_values,
                exploration_rate=bot1.get_exploration_rate(bot2_name)
            )

            # Update the agent's Q-table
            bot1.update_q_value(
                opponent_name=bot2_name,
                state=bot2_last_action if bot2_last_action is not None else COOPERATE,
                action=bot1_action,
                reward=bot1_reward,
                next_state=bot2_action
            )

        # Update last actions
        bot1_last_action = bot1_action
        bot2_last_action = bot2_action

def run_round_robin():
    """
    Runs a round-robin tournament where each bot plays against every other bot.
    """
    # Create all bots
    bots = [
        QLearningAgent(),
        TFTBot(),
        DefectBot(),
        CooperateBot(),
        GrimBot(),
        TFT90Bot()
    ]
    
    logger = InteractionLogger()
    tournament_stats = []
    aggregate_stats = {}
    game_number = 0
    
    # Each bot plays against every other bot
    for i in range(len(bots)):
        for j in range(i + 1, len(bots)):  # Start from i+1 to avoid playing against self
            bot1 = bots[i]
            bot2 = bots[j]
            
            print(f"\nMatch: {type(bot1).__name__} vs {type(bot2).__name__}")
            
            # Play multiple rounds between these two bots
            round_stats = {}
            for round in range(ROUNDS):
                play_game(bot1, bot2, DISCOUNT_FACTOR, logger, game_number, round_stats)
                game_number += 1
                
                # Decay exploration rates using helper function
                handle_exploration_decay(bot1, bot2, DECAY_RATE)
            
            # Add round stats to tournament stats
            tournament_stats.append(round_stats)
            
            # Update aggregate stats
            for bot_name, stats in round_stats.items():
                if bot_name not in aggregate_stats:
                    aggregate_stats[bot_name] = {
                        TOTAL_PAYOFF: 0,
                        MATCHES_PLAYED: 0,
                        COOPERATE_COUNT: 0,
                        DEFECT_COUNT: 0
                    }
                for key in [TOTAL_PAYOFF, MATCHES_PLAYED, COOPERATE_COUNT, DEFECT_COUNT]:
                    aggregate_stats[bot_name][key] += stats[key]
            
            # Reset bots at the end of each round
            reset_bots(bot1, bot2)
    
    # Export statistics
    export_tournament_stats(aggregate_stats, tournament_stats, 1)
    print("\nSummary statistics have been exported to tournament_stats.csv")
    
    # Export detailed log
    logger.export_to_csv('qlearning_detailed_log.csv')
    print("Detailed Q-learning interactions have been exported to qlearning_detailed_log.csv")

# HELPERS
def initialize_Q_table_for_agent(bot, opponent_name):
        if isinstance(bot, QLearningAgent):
            bot.initialize_q_table_for_opponent(opponent_name)
            bot.initialize_exploration_rate(opponent_name)

def initialize_bot_stats(stats: dict, bot_name: str) -> None:
    if bot_name not in stats:
        stats[bot_name] = {
            TOTAL_PAYOFF: 0,
            MATCHES_PLAYED: 0,
            COOPERATE_COUNT: 0,
            DEFECT_COUNT: 0
        }

def update_bot_stats(stats: dict, bot_name: str, action: str) -> None:
    stats[bot_name][MATCHES_PLAYED] += 1
    if action == COOPERATE:
        stats[bot_name][COOPERATE_COUNT] += 1
    else:
        stats[bot_name][DEFECT_COUNT] += 1

def calculate_and_update_payoffs(stats: dict, bot1_name: str, bot2_name: str, 
                               bot1_action: str, bot2_action: str) -> tuple[float, float]:
    """
    Calculate payoffs from the payoff matrix and update the stats for both bots.

    Returns: tuple[float, float]: The rewards for bot1 and bot2 respectively
    """
    payoffs = PAYOFF_MATRIX[(bot1_action, bot2_action)]
    bot1_reward, bot2_reward = payoffs
    
    # Update total payoffs in stats
    stats[bot1_name][TOTAL_PAYOFF] += bot1_reward
    stats[bot2_name][TOTAL_PAYOFF] += bot2_reward
    
    return bot1_reward, bot2_reward

def get_current_q_values(q_table, opponent_last_action: str) -> dict:
    """
    Get the current Q-values for both possible actions given the opponent's last action.
        
    Returns: dict: Dictionary containing Q-values for both COOPERATE and DEFECT actions
    """
    state = opponent_last_action if opponent_last_action is not None else COOPERATE
    return {
        'COOPERATE': q_table.get_q_value(state, COOPERATE),
        'DEFECT': q_table.get_q_value(state, DEFECT)
    }

def reset_bots(bot1: BaseBot, bot2: BaseBot) -> None:
    """
    Reset bots to their initial state if they are instances of BaseBot.
    """
    if isinstance(bot1, BaseBot):
        bot1.reset()
    if isinstance(bot2, BaseBot):
        bot2.reset()
        
def handle_exploration_decay(bot1: BaseBot, bot2: BaseBot, decay_rate: float) -> None:
    """
    Decay exploration rates for Q-learning bots.
    """
    if isinstance(bot1, QLearningAgent):
        bot1.decay_exploration_rate(type(bot2).__name__, decay_rate)
    if isinstance(bot2, QLearningAgent):
        bot2.decay_exploration_rate(type(bot1).__name__, decay_rate)

