from model.bots.TFTBot import TFTBot
from model.bots.GrimBot import GrimBot
from model.bots.CooperateBot import CooperateBot
from model.bots.DefectBot import DefectBot
from model.tournament.tournament import Tournament
from model.tournament.MatchSimulator import MatchSimulator
from model.tournament.ResultManager import ResultManager
from model.constants import *
def print_match_result(result):
    """Helper function to print a single match result in a readable format"""
    round_num = result.get(ROUND_NUM, 'N/A')
    print(f"\nRound {round_num}:")
    
    # Get bot names from the result keys
    bot_names = set()
    for key in result.keys():
        if key.endswith(ACTIONS_SUFFIX):
            bot_name = key.replace(ACTIONS_SUFFIX, '')
            bot_names.add(bot_name)
    
    bot_names = list(bot_names)
    if len(bot_names) == 2:
        bot1, bot2 = bot_names
        
        # Get actions
        bot1_actions = result.get(f'{bot1}{ACTIONS_SUFFIX}', [])
        bot2_actions = result.get(f'{bot2}{ACTIONS_SUFFIX}', [])
        
        # Get payoffs
        bot1_payoff = result.get(f'{bot1}{PAYOFF_SUFFIX}', 0)
        bot2_payoff = result.get(f'{bot2}{PAYOFF_SUFFIX}', 0)
        
        print(f"{bot1} vs {bot2}")
        for i, (action1, action2) in enumerate(zip(bot1_actions, bot2_actions)):
            print(f"Turn {i+1}: {bot1} chose {action1}, {bot2} chose {action2}")
        print(f"Final score - {bot1}: {bot1_payoff}, {bot2}: {bot2_payoff}")
        print("-" * 50)

def main():
    # Create instances of different bots
    bots = [
        TFTBot(),
        GrimBot(),
        CooperateBot(),
        DefectBot()
    ]

    # Create tournament components
    match_simulator = MatchSimulator()
    result_manager = ResultManager()

    # Create and run tournament
    tournament = Tournament(
        participants=bots,
        rounds=3,
        match_simulator=match_simulator,
        result_manager=result_manager
    )

    # Run the tournament
    tournament.run_tournament()

    # Get and print results
    results = tournament.get_results()
    
    print("\nTournament Results:")
    print("=" * 50)
    
    for result in results:
        print_match_result(result)

if __name__ == "__main__":
    main()