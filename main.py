from model.bots.DefectBot import DefectBot
from model.bots.CooperateBot import CooperateBot
from model.bots.QLearningBot import QLearningBot
from model.bots.TFTBot import TFTBot
from model.bots.GrimBot import GrimBot
from model.bots.TFT90Bot import TFT90Bot
from model.tournament.tournament import Tournament
from model.tournament.MatchSimulator import MatchSimulator
from model.tournament.ResultManager import ResultManager
from model.constants import *

def main():
    NUM_TOURNAMENTS = 100
    aggregate_stats = {}

    for tournament_num in range(NUM_TOURNAMENTS):
        print(f"\nTournament {tournament_num + 1}/{NUM_TOURNAMENTS}")
        
        # Create two QLearningBots with different names
        qbot1 = QLearningBot()
        qbot1.name = "QLearningBot1"
        
        qbot2 = QLearningBot()
        qbot2.name = "QLearningBot2"
        
        # Create all bots
        bots = [
            qbot1,
            qbot2,
            TFTBot(),
            GrimBot(),
            TFT90Bot(),
            DefectBot(),
            CooperateBot()
        ]

        # Create tournament components
        match_simulator = MatchSimulator()
        result_manager = ResultManager()

        # Create and run tournament
        tournament = Tournament(
            participants=bots,
            rounds=10,
            match_simulator=match_simulator,
            result_manager=result_manager
        )

        # Run the tournament
        tournament.run_tournament()

        # Accumulate statistics
        results = result_manager.get_aggregate_results()
        for bot_name, stats in results.items():
            if bot_name not in aggregate_stats:
                aggregate_stats[bot_name] = {
                    TOTAL_PAYOFF: 0,
                    MATCHES_PLAYED: 0,
                    COOPERATE_COUNT: 0,
                    DEFECT_COUNT: 0
                }
            for key in [TOTAL_PAYOFF, MATCHES_PLAYED, COOPERATE_COUNT, DEFECT_COUNT]:
                aggregate_stats[bot_name][key] += stats[key]

    # Print averaged statistics
    print("\nAveraged Statistics over", NUM_TOURNAMENTS, "tournaments:")
    print("=" * 50)
    for bot_name, stats in aggregate_stats.items():
        avg_payoff = stats[TOTAL_PAYOFF] / NUM_TOURNAMENTS
        avg_matches = stats[MATCHES_PLAYED] / NUM_TOURNAMENTS
        total_actions = stats[COOPERATE_COUNT] + stats[DEFECT_COUNT]
        avg_coop_rate = stats[COOPERATE_COUNT] / total_actions if total_actions > 0 else 0
        
        print(f"\n{bot_name}:")
        print(f"Average Payoff per Tournament: {avg_payoff:.2f}")
        print(f"Average Matches per Tournament: {avg_matches:.2f}")
        print(f"Overall Cooperation Rate: {avg_coop_rate:.2%}")

if __name__ == "__main__":
    main()